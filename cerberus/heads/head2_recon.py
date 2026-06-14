import ssl
import socket
import datetime
import importlib
import requests
from core.utils import R, D, G, Y, X, get_headers, get_proxies
from core.grimoire import grimoire_salvar

WORDLIST = [
    "www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "portal", "vpn",
    "smtp", "pop", "imap", "webmail", "dashboard", "blog", "shop", "store", "app",
    "mobile", "cdn", "static", "assets", "media", "images", "img", "video", "docs",
    "support", "help", "forum", "community", "status", "monitor", "git", "gitlab",
    "github", "jenkins", "ci", "build", "deploy", "beta", "alpha", "old", "new",
    "secure", "login", "auth", "oauth", "sso", "id", "account", "panel", "cpanel",
    "whm", "plesk", "ns1", "ns2", "mx", "mx1", "mx2", "remote", "ssh", "db",
    "database", "mysql", "postgres", "redis", "s3", "bucket", "backup", "archive",
    "internal", "intranet", "corp",
]

PORTAS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}


def dns_lookup(target):
    resultados = []
    for tipo in ["A", "MX", "TXT", "NS", "AAAA"]:
        try:
            r = requests.get(
                "https://dns.google/resolve?name=" + target + "&type=" + tipo,
                timeout=5
            )
            for answer in r.json().get("Answer", []):
                resultados.append((tipo, answer.get("data", "")))
        except:
            pass
    return resultados


def formatar_data(d):
    if isinstance(d, list):
        d = d[0]
    try:
        return d.strftime("%d/%m/%Y")
    except:
        return str(d)


def domain_curse(target):
    try:
        whois_lib = importlib.import_module("whois")
    except ModuleNotFoundError:
        whois_lib = None

    print("\n" + R + "  === DOMAIN CURSE: " + target + " ===" + X + "\n")
    saida = ""

    if whois_lib:
        try:
            w     = whois_lib.whois(target)
            bloco = "[WHOIS]\n"
            bloco += "  Registrar : " + str(w.registrar) + "\n"
            bloco += "  Created   : " + formatar_data(w.creation_date) + "\n"
            bloco += "  Expires   : " + formatar_data(w.expiration_date) + "\n"
            bloco += "  Owner     : " + str(w.org) + "\n\n"
            print(R + "  [WHOIS]" + X)
            for linha in bloco.splitlines()[1:]:
                print(D + linha + X)
            saida += bloco
        except Exception as e:
            print(R + "  [WHOIS] Error: " + str(e) + X + "\n")
    else:
        print(R + "  [WHOIS] Not installed. Run: pip install python-whois" + X + "\n")

    try:
        print("\n" + R + "  [DNS]" + X)
        resultados = dns_lookup(target)
        bloco      = "[DNS]\n"
        if resultados:
            for tipo, val in resultados:
                linha = "  " + tipo.ljust(6) + ": " + val
                print(D + linha + X)
                bloco += linha + "\n"
        else:
            print(D + "  No records found" + X)
            bloco += "  No records found\n"
        saida += bloco + "\n"
    except Exception as e:
        print(R + "  [DNS] Error: " + str(e) + X + "\n")

    try:
        print("\n" + R + "  [HEADERS]" + X)
        bloco = "[HEADERS]\n"
        res   = requests.get("https://" + target, timeout=5,
                             headers=get_headers(), proxies=get_proxies())
        for h in ["Server", "X-Powered-By", "Content-Type",
                  "X-Frame-Options", "Strict-Transport-Security"]:
            val  = res.headers.get(h, "not found")
            linha = "  " + h.ljust(30) + ": " + val
            print(D + linha + X)
            bloco += linha + "\n"
        saida += bloco + "\n"
    except Exception as e:
        print(R + "  [HEADERS] Error: " + str(e) + X + "\n")

    caminho = grimoire_salvar(target, "domain_curse", saida)
    print("\n" + R + "  Report saved: " + X + caminho + "\n")


def ip_recon(target):
    try:
        ip = socket.gethostbyname(target)
    except:
        ip = target

    print("\n" + R + "  === IP RECON: " + ip + " ===" + X + "\n")
    saida  = ""
    campos = None

    try:
        r = requests.get("https://ipwho.is/" + ip, timeout=6, proxies=get_proxies())
        d = r.json()
        if d.get("success"):
            campos = [
                ("IP",        d.get("ip")),
                ("Country",   d.get("country")),
                ("Region",    d.get("region")),
                ("City",      d.get("city")),
                ("ZIP",       d.get("postal")),
                ("Latitude",  d.get("latitude")),
                ("Longitude", d.get("longitude")),
                ("Timezone",  (d.get("timezone") or {}).get("id")),
                ("ISP",       (d.get("connection") or {}).get("isp")),
                ("ASN",       (d.get("connection") or {}).get("asn")),
            ]
    except:
        pass

    if not campos:
        try:
            r = requests.get(
                "http://ip-api.com/json/" + ip +
                "?fields=status,country,regionName,city,zip,lat,lon,timezone,org,as,query",
                timeout=6, proxies=get_proxies()
            )
            d = r.json()
            if d.get("status") == "success":
                campos = [
                    ("IP",        d.get("query")),
                    ("Country",   d.get("country")),
                    ("Region",    d.get("regionName")),
                    ("City",      d.get("city")),
                    ("ZIP",       d.get("zip")),
                    ("Latitude",  d.get("lat")),
                    ("Longitude", d.get("lon")),
                    ("Timezone",  d.get("timezone")),
                    ("ISP",       d.get("org")),
                    ("ASN",       d.get("as")),
                ]
        except:
            pass

    if not campos:
        try:
            r = requests.get("https://ipapi.co/" + ip + "/json/",
                             timeout=6, proxies=get_proxies())
            d = r.json()
            if d.get("ip"):
                campos = [
                    ("IP",        d.get("ip")),
                    ("Country",   d.get("country_name")),
                    ("Region",    d.get("region")),
                    ("City",      d.get("city")),
                    ("ZIP",       d.get("postal")),
                    ("Latitude",  d.get("latitude")),
                    ("Longitude", d.get("longitude")),
                    ("Timezone",  d.get("timezone")),
                    ("ISP",       d.get("org")),
                    ("ASN",       d.get("asn")),
                ]
        except:
            pass

    if not campos:
        print(R + "  No data returned for this IP." + X + "\n")
        return

    for chave, val in campos:
        linha = "  " + chave.ljust(12) + ": " + str(val)
        print(D + linha + X)
        saida += linha + "\n"

    print()
    caminho = grimoire_salvar(target, "ip_recon", saida)
    print(R + "  Report saved: " + X + caminho + "\n")


def hellscan(target):
    print("\n" + R + "  === HELLSCAN: " + target + " ===" + X + "\n")
    saida = "[HELLSCAN] " + target + "\n\n"

    try:
        ip    = socket.gethostbyname(target)
        linha = "  IP resolved: " + ip
        print(D + linha + X + "\n")
        saida += linha + "\n\n"
    except:
        print(R + "  Could not resolve host." + X + "\n")
        return 0

    abertos = []
    for porta, servico in PORTAS.items():
        try:
            s = socket.socket()
            s.settimeout(1)
            if s.connect_ex((ip, porta)) == 0:
                linha = "  [OPEN] " + str(porta).ljust(5) + " -> " + servico
                print(R + linha + X)
                abertos.append(linha)
                saida += linha + "\n"
            else:
                print(D + "  [----] " + str(porta).ljust(5) + " -> " + servico + X)
            s.close()
        except:
            pass

    print()
    print(R + "  " + str(len(abertos)) + " open port(s)" + X + "\n")
    caminho = grimoire_salvar(target, "hellscan", saida)
    print(R + "  Report saved: " + X + caminho + "\n")
    return len(abertos)


def ssl_checker(target):
    host = target.replace("https://", "").replace("http://", "").split("/")[0]
    print("\n" + R + "  === SSL/TLS CHECKER: " + host + " ===" + X + "\n")
    saida = "[SSL CHECKER] " + host + "\n\n"
    dias  = None

    print(R + "  [CERTIFICATE]" + X)
    try:
        ctx  = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(), server_hostname=host)
        conn.settimeout(6)
        conn.connect((host, 443))
        cert    = conn.getpeercert()
        conn.close()
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer", []))
        expiry  = cert.get("notAfter", "")
        issued  = cert.get("notBefore", "")
        try:
            exp  = datetime.datetime.strptime(expiry, "%b %d %H:%M:%S %Y %Z")
            dias = (exp - datetime.datetime.utcnow()).days
        except:
            pass
        for chave, val in [
            ("CN",        subject.get("commonName", "N/A")),
            ("Issued by", issuer.get("organizationName", "N/A")),
            ("Valid from",issued),
            ("Expires on",expiry),
            ("SANs",      str([x[1] for x in cert.get("subjectAltName", [])[:5]])),
        ]:
            linha = "  " + chave.ljust(14) + ": " + str(val)
            print(D + linha + X)
            saida += linha + "\n"
        if dias is not None:
            cor = G if dias > 30 else R
            print(cor + "  Expiration   : " + str(dias) + " days remaining" + X)
            saida += "  Expiration: " + str(dias) + " days\n"
    except ssl.SSLCertVerificationError as e:
        print(R + "  [VULN] Invalid certificate: " + str(e) + X)
        saida += "  [VULN] Invalid certificate\n"
    except Exception as e:
        print(R + "  Error: " + str(e) + X)

    print("\n" + R + "  [TLS VERSIONS]" + X)
    saida += "\n[TLS]\n"
    versoes = [
        ("TLSv1.0", getattr(ssl.TLSVersion, "TLSv1",   None), True),
        ("TLSv1.1", getattr(ssl.TLSVersion, "TLSv1_1", None), True),
        ("TLSv1.2", ssl.TLSVersion.TLSv1_2,                   False),
        ("TLSv1.3", getattr(ssl.TLSVersion, "TLSv1_3", None), False),
    ]
    for nome_v, versao_enum, obsoleta in versoes:
        if versao_enum is None:
            continue
        try:
            ctx2 = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx2.minimum_version = versao_enum
            ctx2.maximum_version = versao_enum
            ctx2.check_hostname  = False
            ctx2.verify_mode     = ssl.CERT_NONE
            s  = socket.socket()
            s.settimeout(3)
            ws = ctx2.wrap_socket(s, server_hostname=host)
            ws.connect((host, 443))
            ws.close()
            if obsoleta:
                print(R + "  [VULN] " + nome_v + " supported (obsolete!)" + X)
                saida += "  [VULN] " + nome_v + "\n"
            else:
                print(G + "  [OK]   " + nome_v + " supported" + X)
                saida += "  [OK] " + nome_v + "\n"
        except:
            print(D + "  [---]  " + nome_v + " not supported" + X)
            saida += "  [---] " + nome_v + "\n"

    print("\n" + R + "  [HSTS]" + X)
    try:
        r    = requests.get("https://" + host, timeout=5,
                            headers=get_headers(), proxies=get_proxies())
        hsts = r.headers.get("Strict-Transport-Security", "")
        if hsts:
            print(G + "  [OK] " + hsts + X)
            saida += "  [OK] HSTS: " + hsts + "\n"
        else:
            print(R + "  [!] HSTS absent" + X)
            saida += "  [!] HSTS absent\n"
    except Exception as e:
        print(D + "  Error: " + str(e) + X)

    print()
    caminho = grimoire_salvar(host, "ssl_checker", saida)
    print(R + "  Report saved: " + X + caminho + "\n")
    return dias


def tech_fingerprint(target):
    base = target if target.startswith("http") else "https://" + target
    print("\n" + R + "  === TECH FINGERPRINT: " + base + " ===" + X + "\n")
    saida      = "[TECH FINGERPRINT] " + base + "\n\n"
    encontrados = []

    try:
        r       = requests.get(base, timeout=8,
                               headers=get_headers(), proxies=get_proxies())
        html    = r.text.lower()
        headers = {k.lower(): v for k, v in r.headers.items()}
        cookies = [c.name.lower() for c in r.cookies]
    except Exception as e:
        print(R + "  Error accessing: " + str(e) + X + "\n")
        return 0

    assinaturas = {
        "WordPress"         : [("html", "wp-content"), ("html", "wp-includes")],
        "Joomla"            : [("html", "joomla"), ("html", "/components/com_")],
        "Drupal"            : [("html", "drupal"), ("cookie", "drupal")],
        "Magento"           : [("html", "magento"), ("cookie", "frontend")],
        "Shopify"           : [("html", "shopify"), ("html", "cdn.shopify.com")],
        "Wix"               : [("html", "wixsite"), ("html", "wix.com")],
        "Ghost"             : [("html", "ghost.io")],
        "React"             : [("html", "__react"), ("html", "react.production")],
        "Vue.js"            : [("html", "vue.js"), ("html", "__vue__")],
        "Angular"           : [("html", "ng-version"), ("html", "ng-app")],
        "Next.js"           : [("html", "_next/static")],
        "jQuery"            : [("html", "jquery.min.js"), ("html", "jquery.js")],
        "Bootstrap"         : [("html", "bootstrap.min.css"), ("html", "bootstrap.min.js")],
        "Tailwind"          : [("html", "tailwindcss"), ("html", "tailwind")],
        "Apache"            : [("header_server", "apache")],
        "Nginx"             : [("header_server", "nginx")],
        "IIS"               : [("header_server", "iis")],
        "Cloudflare"        : [("header", "cf-ray")],
        "AWS CloudFront"    : [("header", "x-amz-cf-id")],
        "Vercel"            : [("header", "x-vercel-id")],
        "Netlify"           : [("header", "x-nf-request-id")],
        "PHP"               : [("header_x-powered-by", "php"), ("html", ".php")],
        "ASP.NET"           : [("header_x-powered-by", "asp.net")],
        "Python/Django"     : [("cookie", "csrftoken"), ("cookie", "sessionid")],
        "Node.js/Express"   : [("header_x-powered-by", "express")],
        "Google Analytics"  : [("html", "google-analytics.com"), ("html", "gtag(")],
        "Google Tag Manager": [("html", "googletagmanager.com")],
        "Hotjar"            : [("html", "hotjar")],
        "Facebook Pixel"    : [("html", "fbevents.js")],
        "reCAPTCHA"         : [("html", "recaptcha")],
        "hCaptcha"          : [("html", "hcaptcha.com")],
    }

    for tech, checks in assinaturas.items():
        achado = False
        for tipo, valor in checks:
            if tipo == "html" and valor in html:
                achado = True; break
            elif tipo == "header" and valor in headers:
                achado = True; break
            elif tipo == "cookie" and valor in cookies:
                achado = True; break
            elif tipo.startswith("header_"):
                k = tipo.replace("header_", "")
                if k in headers and valor in headers[k].lower():
                    achado = True; break
        if achado:
            encontrados.append(tech)
            print(G + "  [FOUND] " + tech + X)
            saida += "  [FOUND] " + tech + "\n"

    print("\n" + R + "  [RELEVANT HEADERS]" + X)
    saida += "\n[HEADERS]\n"
    for h in ["server", "x-powered-by", "x-generator", "content-type"]:
        if h in headers:
            linha = "  " + h.ljust(20) + ": " + headers[h]
            print(D + linha + X)
            saida += linha + "\n"

    print("\n" + R + "  " + str(len(encontrados)) + " technology(ies) detected" + X + "\n")
    caminho = grimoire_salvar(target, "tech_fingerprint", saida)
    print(R + "  Report saved: " + X + caminho + "\n")
    return len(encontrados)


def subdomain_finder(target):
    import threading

    print("\n" + R + "  === SUBDOMAIN FINDER: " + target + " ===" + X + "\n")
    print(D + "  Checking " + str(len(WORDLIST)) + " subdomains..." + X + "\n")

    founds  = []
    saida   = "[SUBDOMAIN FINDER] " + target + "\n\n"
    lock    = threading.Lock()

    def check(word):
        host = word + "." + target
        try:
            r       = requests.get(
                "https://dns.google/resolve?name=" + host + "&type=A",
                timeout=4
            )
            answers = r.json().get("Answer", [])
            if not answers:
                print(D + "  [----]  " + host + X)
                return

            ip = answers[0].get("data", "")

            status   = "-"
            titulo   = "-"
            https_ok = False
            asn      = "-"
            tech     = "-"

            for scheme in ["https", "http"]:
                try:
                    res = requests.get(
                        scheme + "://" + host,
                        timeout=4, headers=get_headers(),
                        proxies=get_proxies(), allow_redirects=True
                    )
                    status   = str(res.status_code)
                    https_ok = scheme == "https"
                    html     = res.text
                    if "<title" in html.lower():
                        t      = html.lower().split("<title")[1].split(">")[1].split("</title")[0].strip()
                        titulo = t[:40] if t else "-"
                    srv = res.headers.get("Server", "")
                    xpb = res.headers.get("X-Powered-By", "")
                    if srv or xpb:
                        tech = (srv + " " + xpb).strip()
                    break
                except:
                    continue

            try:
                geo = requests.get("https://ipwho.is/" + ip, timeout=4).json()
                asn = (geo.get("connection") or {}).get("asn", "-")
                isp = (geo.get("connection") or {}).get("isp", "")
                if isp:
                    asn = str(asn) + " / " + isp
            except:
                pass

            linha_log = (
                "  [FOUND] " + host + "\n"
                "    IP: " + ip + " | Status: " + status +
                " | HTTPS: " + ("Sim" if https_ok else "Não") +
                " | Título: " + titulo +
                " | Tech: " + tech +
                " | ASN: " + asn
            )

            with lock:
                print(G + "  [FOUND] " + host + X)
                print(D + "  ├─ IP     : " + ip + X)
                print(D + "  ├─ Status : " + status + X)
                print(D + "  ├─ HTTPS  : " + ("Sim" if https_ok else "Não") + X)
                print(D + "  ├─ Título : " + titulo + X)
                print(D + "  ├─ Tech   : " + tech + X)
                print(D + "  └─ ASN    : " + asn + X)
                print()
                founds.append(linha_log)

        except:
            print(D + "  [----]  " + host + X)

    threads = []
    for word in WORDLIST:
        t = threading.Thread(target=check, args=(word,))
        threads.append(t)
        t.start()
        if len(threads) % 10 == 0:
            for t in threads[-10:]:
                t.join()

    for t in threads:
        t.join()

    for linha in founds:
        saida += linha + "\n"

    print()
    print(R + "  " + str(len(founds)) + " subdomain(s) found" + X + "\n")
    caminho = grimoire_salvar(target, "subdomains", saida)
    print(R + "  Report saved: " + X + caminho + "\n")

    if founds:
        print(R + "  [DISCOVERY TREE]" + X + "\n")
        print(D + "  " + target + X)
        for i, linha in enumerate(founds):
            host_part = linha.strip().split("[FOUND]")[-1].strip().split("\n")[0].strip()
            prefixo   = "  └── " if i == len(founds) - 1 else "  ├── "
            print(G + prefixo + host_part + X)
        print()

    return len(founds)