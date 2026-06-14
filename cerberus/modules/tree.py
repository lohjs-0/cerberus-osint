import os
import re
import glob
from core.utils import R, D, G, Y, X
from core.grimoire import LOG_DIR


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