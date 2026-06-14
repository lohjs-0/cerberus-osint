import os
import re
import glob
import datetime
from core.utils import R, D, G, Y, X
from core.grimoire import grimoire_salvar, LOG_DIR


# ─────────────────────────────────────────────
#  ANALYZE
# ─────────────────────────────────────────────

def analyze(target):
    base     = target.replace("http://", "").replace("https://", "").replace("/", "_")
    pattern  = os.path.join(LOG_DIR, base + "*.txt")
    arquivos = sorted(glob.glob(pattern))
    if not arquivos:
        print("\n" + R + "  No reports found for: " + target + X)
        print(D + "  Run CHAIN RITUAL first." + X + "\n")
        return

    print("\n" + R + "  === INTELLIGENCE ANALYSIS: " + target + " ===" + X + "\n")

    portas_abertas   = []
    vulns_high       = []
    headers_missing  = []
    subdomains_found = []
    techs_found      = []
    cves_found       = []
    ssl_issue        = False
    admin_paths      = []
    pastes_found     = []

    for arq in arquivos:
        with open(arq, "r") as f:
            conteudo = f.read()
            linhas   = conteudo.splitlines()
        for linha in linhas:
            l = linha.strip()
            if "[OPEN]" in l and "->" in l:
                portas_abertas.append(l.split("->")[-1].strip())
            if "[VULN] SQLi" in l:
                vulns_high.append("SQL Injection detected")
            if "[VULN] XSS" in l:
                vulns_high.append("Cross-Site Scripting (XSS) detected")
            if "[VULN] LFI" in l:
                vulns_high.append("Local File Inclusion (LFI) detected")
            if "[VULN] Open redirect" in l:
                vulns_high.append("Open Redirect detected")
            if "[MISSING]" in l:
                h = l.replace("[MISSING]", "").strip()
                headers_missing.append(h)
            if "[200]" in l and "/" in l:
                p = l.split("]")[-1].strip()
                if p not in admin_paths:
                    admin_paths.append(p)
            if "[FOUND]" in l and "->" in l and "subdomain" in arq:
                sub = l.split("[FOUND]")[-1].strip().split("->")[0].strip()
                subdomains_found.append(sub)
            if "[FOUND]" in l and "subdomain" not in arq and "soul" not in arq:
                tech = l.replace("[FOUND]", "").strip()
                techs_found.append(tech)
            if "CVE-" in l:
                found = re.findall(r"CVE-\d{4}-\d+", l)
                cves_found.extend(found)
            if "[VULN]" in l and ("TLSv1.0" in l or "TLSv1.1" in l):
                ssl_issue = True
            if "invalid" in l.lower() and "cert" in l.lower():
                ssl_issue = True
            if "[FOUND]" in l and "paste" in arq:
                pastes_found.append(l)

    vulns_high      = list(set(vulns_high))
    headers_missing = list(set(headers_missing))
    cves_found      = list(set(cves_found))
    techs_found     = list(set(techs_found))
    inteligencia    = []

    if admin_paths:
        msg  = "Possible administrative panel exposed.\n"
        msg += "  Reasons:\n"
        for p in admin_paths[:3]:
            msg += "    - Path " + p + " returned HTTP 200/401/403\n"
        if headers_missing:
            msg += "    - " + str(len(headers_missing)) + " security header(s) missing\n"
        msg += "  Severity: HIGH"
        inteligencia.append(("HIGH", "EXPOSED ADMIN SURFACE", msg))

    xss = [v for v in vulns_high if "XSS" in v]
    csp = [h for h in headers_missing if "Content-Security-Policy" in h]
    if xss and csp:
        msg  = "High XSS risk confirmed.\n"
        msg += "  Reasons:\n"
        msg += "    - Reflected XSS payload accepted by server\n"
        msg += "    - Content-Security-Policy header absent\n"
        msg += "  Severity: HIGH"
        inteligencia.append(("HIGH", "XSS ATTACK SURFACE", msg))

    sqli = [v for v in vulns_high if "SQL" in v]
    if sqli:
        msg  = "SQL Injection vector identified.\n"
        msg += "  Reasons:\n"
        msg += "    - Server returned SQL error on injected input\n"
        msg += "    - Database layer exposed to user input\n"
        msg += "  Impact: Data exfiltration, authentication bypass\n"
        msg += "  Severity: CRITICAL"
        inteligencia.append(("CRITICAL", "SQL INJECTION", msg))

    if ssl_issue:
        msg  = "Weak or broken SSL/TLS configuration.\n"
        msg += "  Reasons:\n"
        msg += "    - Obsolete TLS version (1.0/1.1) supported\n"
        msg += "    - Exposes users to MITM attacks\n"
        msg += "  Severity: MEDIUM"
        inteligencia.append(("MEDIUM", "WEAK TLS", msg))

    if len(subdomains_found) > 3 and techs_found:
        msg  = "Large attack surface detected.\n"
        msg += "  Reasons:\n"
        msg += "    - " + str(len(subdomains_found)) + " subdomain(s) exposed\n"
        msg += "    - Technology stack identified: " + ", ".join(techs_found[:4]) + "\n"
        msg += "    - Each subdomain is a potential entry point\n"
        msg += "  Severity: MEDIUM"
        inteligencia.append(("MEDIUM", "WIDE ATTACK SURFACE", msg))

    if cves_found:
        msg  = "Known vulnerabilities associated with this target.\n"
        msg += "  Reasons:\n"
        for c in cves_found[:5]:
            msg += "    - " + c + " on record\n"
        msg += "  Severity: HIGH"
        inteligencia.append(("HIGH", "KNOWN CVEs", msg))

    risky = [p for p in portas_abertas if any(x in p for x in ["Telnet", "FTP", "SMB", "RDP"])]
    if risky:
        msg  = "Risky services exposed to the internet.\n"
        msg += "  Reasons:\n"
        for s in risky:
            msg += "    - " + s + " is open and reachable\n"
        msg += "  Severity: HIGH"
        inteligencia.append(("HIGH", "RISKY SERVICES", msg))

    if pastes_found:
        msg  = "Target data found in public paste sites.\n"
        msg += "  Reasons:\n"
        msg += "    - " + str(len(pastes_found)) + " paste(s) reference this target\n"
        msg += "    - Possible credential or data leak\n"
        msg += "  Severity: HIGH"
        inteligencia.append(("HIGH", "DATA LEAK DETECTED", msg))

    if not inteligencia and headers_missing:
        msg  = "Security headers not configured.\n"
        msg += "  Missing: " + ", ".join(headers_missing[:3]) + "\n"
        msg += "  Severity: MEDIUM"
        inteligencia.append(("MEDIUM", "MISSING HEADERS", msg))

    if not inteligencia:
        print(G + "  No significant threats identified in saved reports." + X + "\n")
        return

    ordem = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    inteligencia.sort(key=lambda x: ordem.get(x[0], 9))

    for sev, titulo, msg in inteligencia:
        cor = R if sev in ["CRITICAL", "HIGH"] else Y
        print(cor + "  +--[" + sev + "] " + titulo + X)
        for linha in msg.split("\n"):
            print(D + "  |  " + linha + X)
        print(D + "  +" + "-" * 40 + X)
        print()

    saida = "[INTELLIGENCE] " + target + "\n\n"
    for sev, titulo, msg in inteligencia:
        saida += "[" + sev + "] " + titulo + "\n" + msg + "\n\n"

    caminho = grimoire_salvar(target, "intelligence", saida)
    print(R + "  Report saved: " + X + caminho + "\n")


# ─────────────────────────────────────────────
#  TREE VIEW
# ─────────────────────────────────────────────

def tree_view(target):
    base = target.replace("http://", "").replace("https://", "").replace("/", "_")
    print("\n" + R + "  === DISCOVERY TREE: " + target + " ===" + X + "\n")

    subdomains = {}
    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*subdomains*.txt"))):
        with open(arq) as f:
            for linha in f:
                if "[FOUND]" in linha and "->" in linha:
                    partes = linha.strip().split("[FOUND]")[-1].strip()
                    sub    = partes.split("->")[0].strip()
                    ip     = partes.split("->")[-1].strip() if "->" in partes else "?"
                    subdomains[sub] = ip

    portas = {}
    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*hellscan*.txt"))):
        with open(arq) as f:
            for linha in f:
                if "[OPEN]" in linha and "->" in linha:
                    l       = linha.strip().replace("[OPEN]", "").strip()
                    porta   = l.split("->")[0].strip()
                    servico = l.split("->")[-1].strip()
                    portas[porta] = servico

    paths = []
    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*vulnscan*.txt"))):
        with open(arq) as f:
            for linha in f:
                if "[200]" in linha or "[401]" in linha or "[403]" in linha:
                    found = re.findall(r"/\S+", linha)
                    if found:
                        paths.extend(found)

    techs = []
    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*tech_fingerprint*.txt"))):
        with open(arq) as f:
            for linha in f:
                if "[FOUND]" in linha:
                    t = linha.replace("[FOUND]", "").strip()
                    if t:
                        techs.append(t)
    techs = list(set(techs))

    total = len(subdomains) + len(portas) + len(paths) + len(techs)
    if total == 0:
        print(D + "  No data found. Run CHAIN RITUAL first." + X + "\n")
        return

    print(D + "  " + target + X)

    if subdomains:
        items = list(subdomains.items())
        print(D + "  +-- [SUBDOMAINS] " + str(len(items)) + " found" + X)
        for i, (sub, ip) in enumerate(items):
            prefixo = "  |   +-- " if i < len(items) - 1 else "  |   `-- "
            print(G + prefixo + sub + X + D + " -> " + ip + X)

    if portas:
        items         = list(portas.items())
        ultimo_branch = not paths and not techs
        print(D + ("  `-- " if ultimo_branch else "  +-- ") + "[OPEN PORTS] " + str(len(items)) + " found" + X)
        for i, (porta, servico) in enumerate(items):
            p       = "      " if ultimo_branch else "  |   "
            prefixo = p + ("`-- " if i == len(items) - 1 else "+-- ")
            print(R + prefixo + porta + X + D + " -> " + servico + X)

    if paths:
        paths         = list(set(paths))
        ultimo_branch = not techs
        print(D + ("  `-- " if ultimo_branch else "  +-- ") + "[ADMIN PATHS] " + str(len(paths)) + " found" + X)
        for i, p in enumerate(paths):
            pr      = "      " if ultimo_branch else "  |   "
            prefixo = pr + ("`-- " if i == len(paths) - 1 else "+-- ")
            print(Y + prefixo + p + X)

    if techs:
        print(D + "  `-- [TECH STACK] " + str(len(techs)) + " detected" + X)
        for i, t in enumerate(techs):
            prefixo = "      `-- " if i == len(techs) - 1 else "      +-- "
            print(R + prefixo + t + X)

    print()


# ─────────────────────────────────────────────
#  TIMELINE
# ─────────────────────────────────────────────

def timeline(target):
    base    = target.replace("http://", "").replace("https://", "").replace("/", "_")
    print("\n" + R + "  === EXPOSURE TIMELINE: " + target + " ===" + X + "\n")
    eventos = []

    try:
        for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*domain_curse*.txt")))[:1]:
            with open(arq) as f:
                conteudo = f.read()
            m = re.search(r"Created\s*:\s*(\d{2}/\d{2}/\d{4})", conteudo)
            if m:
                partes = m.group(1).split("/")
                eventos.append((partes[2], partes[1], "Domain registered", "INFO"))
            m = re.search(r"Expires\s*:\s*(\d{2}/\d{2}/\d{4})", conteudo)
            if m:
                partes = m.group(1).split("/")
                eventos.append((partes[2], partes[1], "Domain expires", "INFO"))
            m = re.search(r"Registrar\s*:\s*(.+)", conteudo)
            if m:
                eventos.append(("----", "--", "Registrar: " + m.group(1).strip(), "INFO"))
    except:
        pass

    scans_vistos = set()
    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*.txt"))):
        nome = os.path.basename(arq)
        m    = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})", nome)
        if m:
            ano    = m.group(1); mes = m.group(2); dia = m.group(3)
            hora   = m.group(4) + ":" + m.group(5)
            modulo = nome.replace(base + "_", "").split("_" + m.group(0))[0]
            if modulo not in scans_vistos:
                scans_vistos.add(modulo)
                eventos.append((ano, mes, "[" + dia + "/" + mes + "/" + ano + " " + hora + "] Scan: " + modulo.upper(), "SCAN"))

    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*vulnscan*.txt")))[-1:]:
        m_arq = re.search(r"(\d{4})(\d{2})(\d{2})", os.path.basename(arq))
        ano   = m_arq.group(1) if m_arq else "????"; mes = m_arq.group(2) if m_arq else "??"; dia = m_arq.group(3) if m_arq else "??"
        with open(arq) as f:
            conteudo = f.read()
        high = len(re.findall(r"\[VULN\]", conteudo))
        med  = len(re.findall(r"\[MISSING\]", conteudo))
        if high or med:
            eventos.append((ano, mes, "[" + dia + "/" + mes + "/" + ano + "] VulnScan: HIGH=" + str(high) + " MEDIUM=" + str(med), "HIGH" if high else "MEDIUM"))

    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*ssl_checker*.txt")))[-1:]:
        m_arq = re.search(r"(\d{4})(\d{2})(\d{2})", os.path.basename(arq))
        ano   = m_arq.group(1) if m_arq else "????"; mes = m_arq.group(2) if m_arq else "??"; dia = m_arq.group(3) if m_arq else "??"
        with open(arq) as f:
            conteudo = f.read()
        m = re.search(r"Expiration.*?:\s*(.+)", conteudo)
        if m:
            eventos.append((ano, mes, "[" + dia + "/" + mes + "/" + ano + "] SSL expires in: " + m.group(1).strip(), "INFO"))
        if "[VULN]" in conteudo:
            eventos.append((ano, mes, "[" + dia + "/" + mes + "/" + ano + "] Weak TLS detected", "MEDIUM"))

    for arq in sorted(glob.glob(os.path.join(LOG_DIR, base + "*subdomains*.txt")))[-1:]:
        m_arq = re.search(r"(\d{4})(\d{2})(\d{2})", os.path.basename(arq))
        ano   = m_arq.group(1) if m_arq else "????"; mes = m_arq.group(2) if m_arq else "??"; dia = m_arq.group(3) if m_arq else "??"
        with open(arq) as f:
            linhas = f.readlines()
        subs = [l for l in linhas if "[FOUND]" in l]
        if subs:
            eventos.append((ano, mes, "[" + dia + "/" + mes + "/" + ano + "] " + str(len(subs)) + " subdomain(s) mapped", "MEDIUM"))

    if not eventos:
        print(D + "  No timeline data. Run CHAIN RITUAL first." + X + "\n")
        return

    vistos         = set()
    eventos_unicos = []
    for e in eventos:
        if e[2] not in vistos:
            vistos.add(e[2])
            eventos_unicos.append(e)

    ordem_sev = {"HIGH": 0, "MEDIUM": 1, "SCAN": 2, "INFO": 3}
    eventos_unicos.sort(key=lambda x: (x[0] + x[1], ordem_sev.get(x[3], 9)))

    ano_atual = ""
    for ano, mes, desc, sev in eventos_unicos:
        cor = R if sev == "HIGH" else Y if sev == "MEDIUM" else G if sev == "SCAN" else D
        if ano != ano_atual and ano != "----":
            ano_atual = ano
            print(R + "  -- " + ano + " " + "-" * 30 + X)
        print(cor + "  |  " + desc + X)
    print(D + "  `" + "-" * 38 + X)
    print()

    saida = "[TIMELINE] " + target + "\n\n"
    for ano, mes, desc, sev in eventos_unicos:
        saida += "[" + sev + "] " + desc + "\n"

    caminho = grimoire_salvar(target, "timeline", saida)
    print(R + "  Report saved: " + X + caminho + "\n")