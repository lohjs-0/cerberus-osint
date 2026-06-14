import os
import re
import glob
import datetime
from core.utils import R, D, G, Y, X
from core.grimoire import grimoire_salvar, LOG_DIR


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