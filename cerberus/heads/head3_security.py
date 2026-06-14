import re
import socket
import requests
import urllib.parse as _up
from core.utils import R, D, G, Y, X, get_headers, get_proxies
from core.grimoire import grimoire_salvar
from core.config import config_load


def vulnscan(target):
    base = target if target.startswith("http") else "https://" + target
    print("\n" + R + "  === VULNSCAN: " + base + " ===" + X + "\n")
    saida  = "[VULNSCAN] " + base + "\n\n"
    issues = []

    print(D + "  [1/7] Security headers..." + X)
    try:
        r = requests.get(base, timeout=6, headers=get_headers(), proxies=get_proxies())
        for h in ["X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security",
                  "Content-Security-Policy", "X-XSS-Protection", "Referrer-Policy"]:
            if h not in r.headers:
                print(Y + "  [MISSING] " + h + X)
                saida += "  [MISSING] " + h + "\n"
                issues.append(("medium", "Missing header: " + h))
            else:
                print(D + "  [OK]      " + h + X)
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [2/7] SQL injection..." + X)
    sqli_found = False
    try:
        test_url = base.rstrip("/") + ("&" if "?" in base else "?") + "id="
        for p in ["'", '"', "' OR 1=1--"]:
            r = requests.get(test_url + _up.quote(p), timeout=5,
                             headers=get_headers(), proxies=get_proxies())
            for err in ["sql syntax", "mysql_fetch", "ORA-", "syntax error"]:
                if err.lower() in r.text.lower():
                    print(R + "  [VULN] SQLi: " + p + X)
                    saida += "  [VULN] SQLi: " + p + "\n"
                    issues.append(("high", "SQLi: " + p))
                    sqli_found = True
        if not sqli_found:
            print(G + "  No obvious SQLi." + X)
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [3/7] Open redirect..." + X)
    redirect_found = False
    try:
        for param in ["redirect", "url", "next", "return", "goto"]:
            test = base.rstrip("/") + ("&" if "?" in base else "?") + param + "=https://evil.com"
            r = requests.get(test, timeout=5, headers=get_headers(),
                             proxies=get_proxies(), allow_redirects=False)
            if "evil.com" in r.headers.get("Location", ""):
                print(R + "  [VULN] Open redirect: ?" + param + X)
                saida += "  [VULN] Open redirect: ?" + param + "\n"
                issues.append(("high", "Open redirect: ?" + param))
                redirect_found = True
        if not redirect_found:
            print(G + "  No open redirect." + X)
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [4/7] Exposed admin paths..." + X)
    try:
        for path in ["/admin", "/admin/login", "/wp-admin", "/phpmyadmin",
                     "/dashboard", "/panel", "/cpanel", "/login", "/api/admin"]:
            r = requests.get(base.rstrip("/") + path, timeout=4,
                             headers=get_headers(), proxies=get_proxies())
            if r.status_code in [200, 401, 403]:
                print(Y + "  [" + str(r.status_code) + "] " + path + X)
                saida += "  [" + str(r.status_code) + "] " + path + "\n"
                issues.append(("medium", "Exposed: " + path))
            else:
                print(D + "  [---] " + path + X)
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [5/7] Reflected XSS..." + X)
    xss_found = False
    try:
        test_url = base.rstrip("/") + ("&" if "?" in base else "?") + "q="
        for p in ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
                  "'><svg onload=alert(1)>"]:
            r = requests.get(test_url + _up.quote(p), timeout=5,
                             headers=get_headers(), proxies=get_proxies())
            if p.lower() in r.text.lower():
                print(R + "  [VULN] XSS: " + p[:40] + X)
                saida += "  [VULN] XSS: " + p[:40] + "\n"
                issues.append(("high", "XSS: " + p[:40]))
                xss_found = True
                break
        if not xss_found:
            print(G + "  No reflected XSS." + X)
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [6/7] LFI + Directory listing..." + X)
    lfi_found = False
    try:
        test_url = base.rstrip("/") + ("&" if "?" in base else "?") + "file="
        for p in ["../../etc/passwd", "../../../../etc/passwd"]:
            r = requests.get(test_url + _up.quote(p), timeout=5,
                             headers=get_headers(), proxies=get_proxies())
            if "root:x:" in r.text or "daemon:" in r.text:
                print(R + "  [VULN] LFI: " + p + X)
                saida += "  [VULN] LFI: " + p + "\n"
                issues.append(("high", "LFI: " + p))
                lfi_found = True
                break
        if not lfi_found:
            print(G + "  No LFI detected." + X)
        for path in ["/images/", "/uploads/", "/files/", "/backup/", "/static/"]:
            r = requests.get(base.rstrip("/") + path, timeout=4,
                             headers=get_headers(), proxies=get_proxies())
            if r.status_code == 200 and (
                "index of" in r.text.lower() or "parent directory" in r.text.lower()
            ):
                print(Y + "  [OPEN] Directory listing: " + path + X)
                saida += "  [OPEN] Directory listing: " + path + "\n"
                issues.append(("medium", "Directory listing: " + path))
    except Exception as e:
        print(R + "  [ERROR] " + str(e) + X)
    print()

    print(D + "  [7/7] Exposed sensitive files..." + X)
    sensitive = [
        "/.env", "/.env.backup", "/.env.local", "/.git/config", "/.git/HEAD",
        "/wp-config.php", "/wp-config.php.bak", "/config.php", "/config.yml",
        "/config.yaml", "/database.yml", "/settings.py", "/local_settings.py",
        "/.htpasswd", "/.htaccess", "/composer.json", "/package.json",
        "/Dockerfile", "/docker-compose.yml", "/id_rsa", "/id_rsa.pub",
        "/server.key", "/backup.sql", "/dump.sql", "/db.sql",
    ]
    sensitive_found = False
    for path in sensitive:
        try:
            r = requests.get(base.rstrip("/") + path, timeout=4,
                             headers=get_headers(), proxies=get_proxies())
            if r.status_code == 200 and len(r.text) > 10:
                indicators = ["DB_", "SECRET", "PASSWORD", "API_KEY", "TOKEN",
                              "mysql", "postgres", "redis", "[core]", "<?php",
                              "private", "BEGIN RSA", "PRIVATE KEY"]
                matched = any(ind.lower() in r.text.lower() for ind in indicators)
                if matched:
                    print(R + "  [CRITICAL] " + path + " EXPOSED with sensitive content!" + X)
                    saida += "  [CRITICAL] " + path + " exposed\n"
                    issues.append(("critical", "Sensitive file exposed: " + path))
                    sensitive_found = True
                else:
                    print(Y + "  [FOUND] " + path + " accessible (status 200)" + X)
                    saida += "  [FOUND] " + path + "\n"
                    issues.append(("medium", "File accessible: " + path))
                    sensitive_found = True
            else:
                print(D + "  [---] " + path + X)
        except:
            print(D + "  [---] " + path + X)
    if not sensitive_found:
        print(G + "  No sensitive files exposed." + X)

    print()
    print(R + "  === SUMMARY ===" + X)
    critical = [i for i in issues if i[0] == "critical"]
    high     = [i for i in issues if i[0] == "high"]
    medium   = [i for i in issues if i[0] == "medium"]
    if not issues:
        print(G + "  No vulnerabilities found." + X)
    else:
        print(R + "  CRITICAL : " + str(len(critical)) + X)
        print(R + "  HIGH     : " + str(len(high)) + X)
        print(Y + "  MEDIUM   : " + str(len(medium)) + X)
    saida += "\nSUMMARY\nCRITICAL: " + str(len(critical)) + \
             "  HIGH: " + str(len(high)) + \
             "  MEDIUM: " + str(len(medium)) + "\n"
    print()
    caminho = grimoire_salvar(target, "vulnscan", saida)
    print(R + "  Report saved: " + X + caminho + "\n")
    return len(critical), len(high), len(medium)


def cve_lookup():
    print("\n" + R + "  === CVE LOOKUP ===" + X + "\n")
    print(D + "  [1] Search by product/version" + X)
    print(D + "  [2] Specific CVE (ex: CVE-2021-44228)" + X + "\n")
    op    = input(R + "  Choose: " + X).strip()
    saida = ""

    if op == "1":
        produto = input(R + "  Product (ex: apache 2.4.49): " + X).strip()
        print("\n" + D + "  Querying NVD..." + X + "\n")
        try:
            r     = requests.get(
                "https://services.nvd.nist.gov/rest/json/cves/2.0",
                params={"keywordSearch": produto, "resultsPerPage": 10},
                headers=get_headers(), timeout=10
            )
            items = r.json().get("vulnerabilities", [])
            saida = "[CVE] " + produto + "\n\n"
            if not items:
                print(D + "  No CVEs found." + X + "\n")
                return
            for item in items:
                cve    = item["cve"]
                cve_id = cve.get("id", "?")
                desc   = cve.get("descriptions", [{}])[0].get("value", "N/A")[:100]
                score  = sev = "N/A"
                for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                    if key in cve.get("metrics", {}):
                        m     = cve["metrics"][key][0].get("cvssData", {})
                        score = str(m.get("baseScore", "N/A"))
                        sev   = m.get("baseSeverity", m.get("severity", "N/A"))
                        break
                cor = R if sev in ["CRITICAL", "HIGH"] else Y if sev == "MEDIUM" else D
                print(cor + "  [" + cve_id + "] " + score + " (" + sev + ")" + X)
                print(D + "  " + desc + X + "\n")
                saida += "[" + cve_id + "] " + score + " " + sev + "\n" + desc + "\n\n"
        except Exception as e:
            print(R + "  Error: " + str(e) + X)

    elif op == "2":
        cve_id = input(R + "  CVE ID: " + X).strip().upper()
        print("\n" + D + "  Querying NVD..." + X + "\n")
        try:
            r     = requests.get(
                "https://services.nvd.nist.gov/rest/json/cves/2.0",
                params={"cveId": cve_id}, headers=get_headers(), timeout=10
            )
            items = r.json().get("vulnerabilities", [])
            saida = "[CVE] " + cve_id + "\n\n"
            if not items:
                print(D + "  CVE not found." + X + "\n")
                return
            cve    = items[0]["cve"]
            desc   = cve.get("descriptions", [{}])[0].get("value", "N/A")
            score  = sev = vector = "N/A"
            for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                if key in cve.get("metrics", {}):
                    m      = cve["metrics"][key][0].get("cvssData", {})
                    score  = str(m.get("baseScore", "N/A"))
                    sev    = m.get("baseSeverity", m.get("severity", "N/A"))
                    vector = m.get("vectorString", "N/A")
                    break
            cor = R if sev in ["CRITICAL", "HIGH"] else Y if sev == "MEDIUM" else G
            for chave, val in [("ID", cve_id), ("Score", score + " (" + sev + ")"), ("Vector", vector)]:
                print(cor + "  " + chave.ljust(8) + ": " + val + X)
            print(D + "\n  " + desc[:300] + X)
            refs = cve.get("references", [])
            if refs:
                print("\n" + R + "  [REFERENCES]" + X)
                for ref in refs[:5]:
                    print(D + "  -> " + ref.get("url", "") + X)
                    saida += "  -> " + ref.get("url", "") + "\n"
        except Exception as e:
            print(R + "  Error: " + str(e) + X)

    print()
    if saida:
        caminho = grimoire_salvar("cve", "lookup", saida)
        print(R + "  Report saved: " + X + caminho + "\n")


def paste_monitor(target):
    print("\n" + R + "  === PASTE / LEAK MONITOR: " + target + " ===" + X + "\n")
    saida      = "[PASTE MONITOR] " + target + "\n\n"
    encontrados = []

    print(D + "  Searching public sources..." + X + "\n")
    dorks_paste = [
        'site:pastebin.com "' + target + '"',
        '"' + target + '" password leaked',
        '"' + target + '" dump site:paste.ee',
    ]
    for dork in dorks_paste:
        try:
            r = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": dork, "format": "json", "no_html": 1},
                headers=get_headers(), proxies=get_proxies(), timeout=8
            )
            for item in r.json().get("RelatedTopics", []):
                if "FirstURL" in item and target.lower() in item.get("Text", "").lower():
                    url = item["FirstURL"]
                    encontrados.append(url)
                    print(R + "  [FOUND] " + url + X)
                    saida += "  [FOUND] " + url + "\n"
        except:
            pass

    if "@" in target:
        print(R + "  [HAVEIBEENPWNED]" + X)
        try:
            r = requests.get(
                "https://haveibeenpwned.com/api/v3/breachedaccount/" + target,
                headers={**get_headers(), "hibp-api-key": ""},
                proxies=get_proxies(), timeout=6
            )
            if r.status_code == 200:
                breaches = r.json()
                print(R + "  [!] " + str(len(breaches)) + " breach(es) found!" + X)
                for b in breaches[:5]:
                    linha = "  -> " + b.get("Name", "?") + " (" + b.get("BreachDate", "?") + ")"
                    print(Y + linha + X)
                    saida += linha + "\n"
            elif r.status_code == 404:
                print(G + "  [OK] Not found in known breaches." + X)
            elif r.status_code == 401:
                print(D + "  [HIBP] API key required." + X)
        except Exception as e:
            print(D + "  [HIBP] Error: " + str(e) + X)

    if not encontrados:
        print(D + "  No public pastes found." + X)

    print("\n" + R + "  " + str(len(encontrados)) + " result(s)" + X + "\n")
    caminho = grimoire_salvar(target, "paste_monitor", saida)
    print(R + "  Report saved: " + X + caminho + "\n")


def shodan_search(target):
    print("\n" + R + "  === SHODAN: " + target + " ===" + X + "\n")
    cfg     = config_load()
    api_key = cfg.get("apis", {}).get("shodan", "")
    if not api_key:
        print(R + "  [!] Shodan API key not configured." + X)
        print(D + "  Configure at: menu (8) -> [2] Shodan" + X + "\n")
        return
    saida = "[SHODAN] " + target + "\n\n"
    try:
        ip = socket.gethostbyname(target)
    except:
        ip = target
    print(D + "  IP: " + ip + X + "\n")
    try:
        r = requests.get(
            "https://api.shodan.io/shodan/host/" + ip,
            params={"key": api_key}, timeout=8
        )
        if r.status_code == 404:
            print(D + "  No Shodan data for this IP." + X + "\n")
            return
        if r.status_code == 401:
            print(R + "  Invalid API key." + X + "\n")
            return
        d = r.json()
        print(R + "  [GENERAL INFO]" + X)
        for chave, val in [
            ("IP",        d.get("ip_str")),
            ("Org",       d.get("org")),
            ("ISP",       d.get("isp")),
            ("Country",   d.get("country_name")),
            ("City",      d.get("city")),
            ("OS",        d.get("os", "N/A")),
            ("Hostnames", ", ".join(d.get("hostnames", []))),
            ("Tags",      ", ".join(d.get("tags", []))),
        ]:
            if val:
                linha = "  " + chave.ljust(12) + ": " + str(val)
                print(D + linha + X)
                saida += linha + "\n"
        print("\n" + R + "  [PORTS / SERVICES]" + X)
        saida += "\n[PORTS]\n"
        todos_vulns = []
        for item in d.get("data", []):
            porta   = item.get("port", "?")
            transp  = item.get("transport", "tcp")
            produto = item.get("product", "")
            versao  = item.get("version", "")
            vulns   = list(item.get("vulns", {}).keys())
            todos_vulns.extend(vulns)
            linha = "  [" + str(porta) + "/" + transp + "] " + produto + " " + versao
            print(G + linha + X)
            saida += linha + "\n"
            for v in vulns:
                print(R + "    [VULN] " + v + X)
                saida += "    [VULN] " + v + "\n"
        if todos_vulns:
            print("\n" + R + "  [CVEs: " + str(len(set(todos_vulns))) + "]" + X)
            for v in set(todos_vulns):
                print(R + "  -> " + v + X)
    except Exception as e:
        print(R + "  Error: " + str(e) + X)
    print()
    caminho = grimoire_salvar(target, "shodan", saida)
    print(R + "  Report saved: " + X + caminho + "\n")


def cloud_scan(target):
    base = target.replace("http://", "").replace("https://", "").rstrip("/")
    name = base.replace("www.", "").split(".")[0]
    print("\n" + R + "  === CLOUD SCAN: " + base + " ===" + X + "\n")
    saida = "[CLOUD SCAN] " + base + "\n\n"
    found = []

    print(D + "  [1/3] S3 Buckets..." + X)
    s3_candidates = [
        name, name + "-backup", name + "-dev", name + "-prod",
        name + "-staging", name + "-assets", name + "-static",
        name + "-media", name + "-files", name + "-data",
        name + "-public", name + "-private", name + "-uploads",
        name + "-logs", name + "-config",
    ]
    for bucket in s3_candidates:
        url = "https://" + bucket + ".s3.amazonaws.com"
        try:
            r = requests.get(url, timeout=5, headers=get_headers(), proxies=get_proxies())
            if r.status_code == 200:
                print(R + "  [CRITICAL] S3 PUBLIC: " + url + X)
                saida += "  [CRITICAL] S3 PUBLIC: " + url + "\n"
                found.append(("CRITICAL", "S3 public: " + url))
                if "<ListBucketResult" in r.text:
                    print(R + "  [CRITICAL] Bucket listing ENABLED!" + X)
            elif r.status_code == 403:
                print(Y + "  [EXISTS]   S3 private: " + url + X)
                saida += "  [EXISTS] S3 private: " + url + "\n"
                found.append(("MEDIUM", "S3 exists (private): " + url))
            else:
                print(D + "  [---] " + bucket + X)
        except:
            print(D + "  [---] " + bucket + X)

    print("\n" + D + "  [2/3] Firebase..." + X)
    firebase_candidates = [
        name, name + "-default-rtdb", name + "-prod",
        name + "-dev", name + "-app", name + "-db",
    ]
    for fb in firebase_candidates:
        url = "https://" + fb + ".firebaseio.com/.json"
        try:
            r = requests.get(url, timeout=5, headers=get_headers(), proxies=get_proxies())
            if r.status_code == 200:
                print(R + "  [CRITICAL] Firebase OPEN: " + url + X)
                print(R + "  [CRITICAL] Data size: " + str(len(r.text)) + " bytes" + X)
                saida += "  [CRITICAL] Firebase open: " + url + "\n"
                found.append(("CRITICAL", "Firebase open: " + url))
            elif r.status_code in [401, 403]:
                print(Y + "  [EXISTS]   Firebase protected: " + fb + ".firebaseio.com" + X)
                saida += "  [EXISTS] Firebase protected: " + fb + "\n"
                found.append(("LOW", "Firebase exists: " + fb))
            else:
                print(D + "  [---] " + fb + X)
        except:
            print(D + "  [---] " + fb + X)

    print("\n" + D + "  [3/3] GCP Storage / Azure Blob..." + X)
    gcp_url = "https://storage.googleapis.com/" + name
    try:
        r = requests.get(gcp_url, timeout=5, headers=get_headers(), proxies=get_proxies())
        if r.status_code == 200:
            print(R + "  [CRITICAL] GCP Storage PUBLIC: " + gcp_url + X)
            saida += "  [CRITICAL] GCP public: " + gcp_url + "\n"
            found.append(("CRITICAL", "GCP public: " + gcp_url))
        elif r.status_code == 403:
            print(Y + "  [EXISTS]   GCP bucket exists: " + name + X)
            saida += "  [EXISTS] GCP: " + name + "\n"
        else:
            print(D + "  [---] GCP: " + name + X)
    except:
        print(D + "  [---] GCP: " + name + X)

    azure_url = "https://" + name + ".blob.core.windows.net"
    try:
        r = requests.get(azure_url, timeout=5, headers=get_headers(), proxies=get_proxies())
        if r.status_code == 200 or "BlobServiceProperties" in r.text:
            print(R + "  [CRITICAL] Azure Blob PUBLIC: " + azure_url + X)
            saida += "  [CRITICAL] Azure public: " + azure_url + "\n"
            found.append(("CRITICAL", "Azure public: " + azure_url))
        elif r.status_code in [400, 403]:
            print(Y + "  [EXISTS]   Azure blob exists: " + name + X)
            saida += "  [EXISTS] Azure: " + name + "\n"
        else:
            print(D + "  [---] Azure: " + name + X)
    except:
        print(D + "  [---] Azure: " + name + X)

    print()
    print(R + "  === SUMMARY ===" + X)
    critical = [f for f in found if f[0] == "CRITICAL"]
    medium   = [f for f in found if f[0] == "MEDIUM"]
    low      = [f for f in found if f[0] == "LOW"]
    if not found:
        print(G + "  No exposed cloud storage found." + X)
    else:
        if critical: print(R + "  CRITICAL : " + str(len(critical)) + X)
        if medium:   print(Y + "  MEDIUM   : " + str(len(medium)) + X)
        if low:      print(D + "  LOW      : " + str(len(low)) + X)

    saida += "\nSUMMARY\nCRITICAL: " + str(len(critical)) + \
             "  MEDIUM: " + str(len(medium)) + "\n"
    print()
    caminho = grimoire_salvar(target, "cloud_scan", saida)
    print(R + "  Report saved: " + X + caminho + "\n")
    return len(critical)


def phone_osint():
    print("\n" + R + "  === PHONE OSINT ===" + X + "\n")
    numero = input(R + "  Phone (ex: +5511999999999): " + X).strip()
    if not numero.startswith("+"):
        print(R + "  Use international format: +55..." + X + "\n")
        return
    saida  = "[PHONE OSINT] " + numero + "\n\n"
    paises = {
        "+55": "Brasil", "+1": "USA/Canada", "+44": "UK",
        "+351": "Portugal", "+54": "Argentina", "+34": "Spain",
        "+49": "Germany", "+33": "France", "+81": "Japan",
        "+86": "China", "+91": "India", "+7": "Russia",
    }
    pais = "Unknown"
    for prefixo, nome in sorted(paises.items(), key=lambda x: -len(x[0])):
        if numero.startswith(prefixo):
            pais = nome
            break
    print(R + "  [BASIC INFO]" + X)
    for chave, val in [("Number", numero), ("Country", pais)]:
        linha = "  " + chave.ljust(12) + ": " + val
        print(D + linha + X)
        saida += linha + "\n"
    if numero.startswith("+55") and len(numero) >= 5:
        ddd  = numero[3:5]
        ddds = {
            "11": "Sao Paulo", "19": "Campinas", "21": "Rio de Janeiro",
            "31": "Belo Horizonte", "41": "Curitiba", "51": "Porto Alegre",
            "61": "Brasilia", "71": "Salvador", "81": "Recife",
            "85": "Fortaleza", "92": "Manaus",
        }
        regiao = ddds.get(ddd, "Unknown DDD")
        tipo   = "Mobile" if len(numero) == 14 else "Landline" if len(numero) == 13 else "Unknown"
        for chave, val in [("DDD", ddd + " -> " + regiao), ("Type", tipo)]:
            linha = "  " + chave.ljust(12) + ": " + val
            print(D + linha + X)
            saida += linha + "\n"
    cfg     = config_load()
    api_key = cfg.get("apis", {}).get("numverify", "")
    if api_key:
        print("\n" + R + "  [NUMVERIFY API]" + X)
        try:
            r = requests.get(
                "http://apilayer.net/api/validate",
                params={"access_key": api_key, "number": numero, "format": 1},
                timeout=6
            )
            d = r.json()
            if d.get("valid"):
                for k, v in [("Carrier", "carrier"), ("Type", "line_type"),
                              ("Country", "country_name")]:
                    val  = str(d.get(v, "N/A"))
                    linha = "  " + k.ljust(15) + ": " + val
                    print(D + linha + X)
                    saida += linha + "\n"
        except Exception as e:
            print(D + "  Error: " + str(e) + X)
    else:
        print("\n" + Y + "  [!] Set up NumVerify API in menu (8) for carrier data." + X)
    print()
    caminho = grimoire_salvar(numero.replace("+", ""), "phone_osint", saida)
    print(R + "  Report saved: " + X + caminho + "\n")