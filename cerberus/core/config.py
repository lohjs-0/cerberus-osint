import os
import json

CONFIG_PATH = os.path.expanduser("~/cerberus/config/settings.json")

DEFAULT_CONFIG = {
    "author": "lohjs-0",
    "version": "1.3.0",
    "timeout": 5,
    "apis": {
        "shodan": "",
        "whoisxml": "",
        "numverify": ""
    }
}

def config_load():
    if not os.path.exists(CONFIG_PATH):
        config_save(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH) as f:
        return json.load(f)

def config_save(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def configure(get_input_fn, R, D, G, Y, X):
    cfg = config_load()
    print("\n" + R + "  === CONFIGURE ===" + X + "\n")
    while True:
        print(D + "  [1] Timeout   : " + X + str(cfg["timeout"]) + "s")
        print(D + "  [2] Shodan    : " + X + (cfg["apis"]["shodan"][:8] + "..." if cfg["apis"]["shodan"] else "not configured"))
        print(D + "  [3] WhoisXML  : " + X + (cfg["apis"]["whoisxml"][:8] + "..." if cfg["apis"]["whoisxml"] else "not configured"))
        print(D + "  [4] NumVerify : " + X + (cfg["apis"]["numverify"][:8] + "..." if cfg["apis"]["numverify"] else "not configured"))
        print(R + "  [9] Back" + X + "\n")
        op = input(R + "  Config: " + X).strip()
        if op == "9":
            break
        elif op == "1":
            val = input(R + "  New timeout (seconds): " + X)
            try:
                cfg["timeout"] = int(val)
                config_save(cfg)
                print(D + "  Saved." + X + "\n")
            except:
                print(R + "  Invalid value." + X + "\n")
        elif op == "2":
            cfg["apis"]["shodan"] = input(R + "  Shodan API key: " + X)
            config_save(cfg)
            print(D + "  Saved." + X + "\n")
        elif op == "3":
            cfg["apis"]["whoisxml"] = input(R + "  WhoisXML API key: " + X)
            config_save(cfg)
            print(D + "  Saved." + X + "\n")
        elif op == "4":
            cfg["apis"]["numverify"] = input(R + "  NumVerify API key: " + X)
            config_save(cfg)
            print(D + "  Saved." + X + "\n")
        else:
            print(R + "  Invalid option." + X + "\n")