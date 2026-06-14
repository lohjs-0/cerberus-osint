import os
import sys
import random
import time
import requests

R = "\033[31m"
D = "\033[2;31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
X = "\033[0m"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 Chrome/114.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

TOR_PROXY  = {"http": "socks5h://127.0.0.1:9150", "https": "socks5h://127.0.0.1:9150"}
TOR_MODE   = False

QUOTES = [
    "The gates of hell open.",
    "Three heads. One purpose.",
    "No one leaves unseen.",
    "The underworld watches.",
    "All souls pass through here.",
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def get_proxies():
    return TOR_PROXY if TOR_MODE else {}

def set_tor(enabled):
    global TOR_MODE
    TOR_MODE = enabled

def is_tor():
    return TOR_MODE

def get_input(prompt="[CERBERUS]---> "):
    return input(R + prompt + X).strip().lower()

def cerberus_say(msg, delay=0.04):
    for ch in msg:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def progress(label, duration=1.5, head=None):
    steps = 20
    head_labels = {1: "HEAD I  ", 2: "HEAD II ", 3: "HEAD III"}
    head_str = D + "  [" + head_labels.get(head, "") + "] " + X if head else "  "
    for i in range(steps + 1):
        filled = "▓" * i
        empty  = "░" * (steps - i)
        pct    = int((i / steps) * 100)
        sys.stdout.write("\r" + head_str + R + label.ljust(15) + " [" + filled + empty + "] " + str(pct) + "%" + X)
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def head_wake(head):
    msgs = {
        1: "The first head opens its eyes...",
        2: "The second head sniffs the network...",
        3: "The third head prepares the judgment...",
    }
    labels = {1: "HEAD I", 2: "HEAD II", 3: "HEAD III"}
    label = labels.get(head, "HEAD")
    msg   = msgs.get(head, "")
    print()
    print(R + "  ┌─────────────────────────────────────┐" + X)
    sys.stdout.write(R + "  │ [" + label + "] " + X)
    for ch in msg:
        sys.stdout.write(D + ch + X)
        sys.stdout.flush()
        time.sleep(0.03)
    padding = 35 - len("[" + label + "] " + msg)
    print(" " * max(0, padding) + R + "│" + X)
    print(R + "  └─────────────────────────────────────┘" + X)
    print()

def head_done(head):
    done = {
        1: "First head satisfied.",
        2: "Second head on the trail.",
        3: "All heads have spoken.",
    }
    print(D + "  [✓] " + done.get(head, "Done.") + X)
    print()

def tor_request(method, url, **kwargs):
    kwargs.setdefault("proxies", get_proxies())
    kwargs.setdefault("headers", get_headers())
    return requests.request(method, url, **kwargs)