```
                    .-@W=                                             
                    #WWWW-                                            
                    *WWWWW*-.                              -++-       
            :       -WWWWWWW%.                           .#WW%-       
            **:     .WWWWWWWW%.                          +WWW=        
            :WW#-    *WWWWWWWW*                          :%WW:        
           .-#WWW#=.  %WWWWWW=#.                          .*@*-..     
          -@WWWWWWWW#:=WWWWWW: .                            .-++**+.  
       .-#WWWWWWWWWWWW%WWWWWW%--..                 .....         :*@: 
     .+WWWWWWWWWWWWWWWWWWWWWWWWWWW#*=-:::....-=+*#%@WW%#*+-.       @* 
      .=#%###++*%WWWWWWWWWWWWWWWWWWWWWWWW@@@WWWWWWWWWW@*==*#*-:::=##. 
                .-*WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW*..-++*++-   
 ..    .-+==-+#%+. =WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%:          
 =W@@@%WWWWWWWWW%%%@WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW@:         
 .+WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%@WWWWWWWWWWWWWW@:        
   .:..+WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%::%WWWWW@+%WWWWWWW+:      
     .:@WWWW@#*#%@@WWWWWWWWWWWWWWWWWWWWWWW%.   =%WWWW+ .-+*%@WWW%.    
    .*W%+:...     ..::=#WWWWWWWWWWWWWWWWWW#     .=%WWW*     .=@WW*    
     .:                *WWW##=#%%@@@#+@WWW:       .@WW*       -WWW:   
                     .#WW%- .  .....  @WW*         %WW:        +WW*   
                    :%WW=            -WW@.         #WW.        .@W@.  
                 ..+WW%=             #WW*       .:-@W#         =WW@.  
               +@@WWW+            .-*WWW-       *@W@#.       :%WWW*   
               :=+=-.            .#@WWW*.       ....         .:-::    
                                  ..:-.                               

    ___          _                         
  / __\___ _ __| |__   ___ _ __ _   _ ___ 
 / /  / _ \ '__| '_ \ / _ \ '__| | | / __|
/ /__|  __/ |  | |_) |  __/ |  | |_| \__ \
\____/\___|_|  |_.__/ \___|_|   \__,_|___/

        OSINT & SECURITY ANALYSIS — v1.3.0
```

> Use Cerberus only on systems you own or have explicit permission to test. Unauthorized scanning is illegal.

---

## What is Cerberus?

Cerberus is a modular OSINT, recon, and security analysis tool built in Python.

Inspired by the three-headed guardian of the underworld, it watches a target from three angles simultaneously — **OSINT**, **RECON**, and **SECURITY** — and delivers a final judgment on exposure risk.

Most tools dump raw data. Cerberus turns that data into intelligence: it interprets findings, explains their impact, maps the attack surface visually, tracks exposure over time, and scores the target across three dimensions before issuing a verdict.

---

## The Three Heads

```
HEAD I   -> OSINT      social footprint, subdomains, leaks, geolocation
HEAD II  -> RECON      ports, SSL/TLS, tech stack, fingerprinting
HEAD III -> SECURITY   vulnerabilities, CVEs, injection vectors, exposed paths
```

When you run **CHAIN RITUAL (12)**, all three heads analyze the target in sequence and produce a scored judgment:

```
======================================
         CERBERUS  JUDGMENT
======================================

HEAD I   (OSINT)     [####..............] 20/100
HEAD II  (RECON)     [######............] 30/100
HEAD III (SECURITY)  [#############.....] 65/100

OVERALL RISK         [#######...........] 38/100

[EVIDENCE]
-> IP resolved: 4.228.31.150
-> 2 open port(s) detected
-> 6 MEDIUM severity issue(s) found
-> 5 CVE(s) associated with target

VERDICT : MINOR SINS
Some weaknesses found. Low but not negligible risk.

======================================
```

Verdicts scale with risk: `SOUL IS CLEAN` → `MINOR SINS` → `WATCH CLOSELY` → `CONDEMNED`.

---

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/lohjs-0/cerberus-osint/main/install.sh | bash
```

## Run

```bash
cerberus
```

> **Note:** The installer places Cerberus in `~/.cerberus/` and creates the `cerberus` command in `~/.local/bin/`. If the command is not found after install, run it directly:
> ```bash
> cd ~/.cerberus && python3 cerberus.py
> ```

---

## Troubleshooting

### `pip3: command not found`

The installer requires `pip3` to install Python dependencies. If it's missing:

```bash
sudo apt update && sudo apt install -y python3-pip
bash install.sh
```

### `cerberus: command not found`

`~/.local/bin` may not be in your `PATH`. Either run directly:

```bash
cd ~/.cerberus && python3 cerberus.py
```

Or add it to your PATH permanently:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

### `can't open file '/path/to/cerberus.py'`

You're running `python3 cerberus.py` from the wrong directory. The installer puts the files in `~/.cerberus/`, not the folder you cloned manually. Navigate there first:

```bash
cd ~/.cerberus && python3 cerberus.py
```

### WSL / Windows users

If you're running Cerberus under WSL, make sure you're working inside the Linux filesystem (`~`) and not a Windows path (`/mnt/c/...`). Running from `/mnt/c/` can cause permission and path resolution issues.

```bash
# Recommended: copy to Linux home first
cp -r /mnt/c/Users/<you>/cerberus ~/.cerberus
cd ~/.cerberus && python3 cerberus.py
```

---

## Menu

```
  ┌─ COLLECTION / RECON ───────────────────────────────────┐
  │  (1) SOUL SEARCH    -> username / socials              │
  │  (2) DOMAIN CURSE   -> domain / IP / DNS               │
  │  (3) HELLSCAN       -> ports / services                │
  │  (4) DORKS          -> google dorks                    │
  │  (5) UNDERWORLD     -> subdomains / email              │
  │  (6) SSL CHECK      -> certificate / TLS               │
  │  (7) TECH SCAN      -> stack / frameworks / CMS        │
  ├─ ANALYSIS / SECURITY ──────────────────────────────────┤
  │  (8)  VULNSCAN      -> web vulnerabilities             │
  │  (9)  CVE LOOKUP    -> search NVD by product           │
  │  (10) PASTE MONITOR -> leaks / public pastes           │
  │  (11) CLOUD SCAN    -> S3 / Firebase / GCP / Azure     │
  ├─ AUTOMATION ───────────────────────────────────────────┤
  │  (12) CHAIN RITUAL  -> full pipeline                   │
  ├─ REPORTS / VISUALIZATION ──────────────────────────────┤
  │  (13) GRIMOIRE      -> reports / list / export         │
  │  (14) VISUALIZE     -> analyze / graph / tree /timeline│
  │  (15) DASHBOARD     -> terminal intelligence summary   │
  ├─ SYSTEM ───────────────────────────────────────────────┤
  │  (C)  CONFIGURE     -> APIs / settings                 │
  │  (X)  TOR           -> anonymous mode / proxy          │
  │  (L)  CLEAR LOGS    -> delete target logs              │
  └────────────────────────────────────────────────────────┘

  (T) SET TARGET   -> change target
  (0) DESCEND      -> exit
```

---

## Modules

### Collection / Recon (1–7)

| # | Module | Description |
|---|---|---|
| 1 | SOUL SEARCH | Username lookup across social platforms |
| 2 | DOMAIN CURSE | `[a]` WHOIS, DNS records, HTTP headers — `[b]` IP geolocation |
| 3 | HELLSCAN | Port scanner — 15 common ports |
| 4 | DORKS | 9 preset Google dorks + custom input |
| 5 | UNDERWORLD | `[a]` Subdomain finder (enriched: IP, status, HTTPS, title, tech, ASN) — `[b]` Email OSINT |
| 6 | SSL CHECK | Certificate validity, TLS version audit, HSTS |
| 7 | TECH SCAN | Stack fingerprinting — CMS, frameworks, CDN, analytics |

### Analysis / Security (8–11)

| # | Module | Description |
|---|---|---|
| 8 | VULNSCAN | Headers, SQLi, XSS, LFI, redirects, admin paths |
| 9 | CVE LOOKUP | Real-time NVD query by product or CVE ID |
| 10 | PASTE MONITOR | Public paste and breach search |
| 11 | CLOUD SCAN | Exposed bucket/resource check — S3, Firebase, GCP, Azure |

### Automation (12)

| # | Module | Description |
|---|---|---|
| 12 | CHAIN RITUAL | Full pipeline across all three heads + Judgment |

### Reports / Visualization (13–15)

| # | Module | Description |
|---|---|---|
| 13 | GRIMOIRE | Report manager — list and browse saved scans |
| 14 | VISUALIZE | Unified intelligence view — analyze, tree, timeline, HTML graph |
| 15 | DASHBOARD | Terminal intelligence summary across all targets |

### System (C / X / L)

| Key | Module | Description |
|---|---|---|
| C | CONFIGURE | API keys and settings |
| X | TOR | Anonymous mode — toggle Tor proxy, check IP |
| L | CLEAR LOGS | Delete all saved logs for a target |

---

## VISUALIZE — Submenu (14)

All intelligence and visualization features are unified under a single menu:

```
=== VISUALIZE ===

[1] ANALYZE       -> intelligence report
[2] TREE          -> discovery tree
[3] TIMELINE      -> exposure timeline
[4] INTEL GRAPH   -> visual HTML graph
[9] Back
```

---

## Intelligence Layer

Instead of listing raw findings, **VISUALIZE → ANALYZE** interprets them:

```
[HIGH] EXPOSED ADMIN SURFACE
  Possible administrative panel exposed.
  Reasons:
    - /wp-admin returned HTTP 200/401/403
    - /phpmyadmin returned HTTP 200/401/403
    - Content-Security-Policy header absent
  Severity: HIGH

[MEDIUM] WIDE ATTACK SURFACE
  Large attack surface detected.
  Reasons:
    - 36 subdomain(s) exposed
    - Technology stack identified: Shopify
    - Each subdomain is a potential entry point
  Severity: MEDIUM
```

---

## Subdomain Finder — Enriched Output

Each discovered subdomain is enriched with live data:

```
[FOUND] api.github.com
├─ IP     : 20.201.28.148
├─ Status : 200
├─ HTTPS  : Sim
├─ Título : github · build and ship software on a single, c
├─ Tech   : github.com
└─ ASN    : 8075 / Microsoft Corporation

[FOUND] ssh.github.com
├─ IP     : 20.201.28.152
├─ Status : 200
├─ HTTPS  : Não
├─ Título : github - change is constant. github keep
├─ Tech   : github.com
└─ ASN    : 8075 / Microsoft Corporation
```

Runs in parallel (10 threads) across DNS resolution, HTTP probing, and ASN lookup via ipwho.is.

---

## Discovery Tree

**VISUALIZE → TREE** maps everything found into a structured view:

```
example.com
|-- [SUBDOMAINS] 18 found
|   |-- api.example.com -> 4.228.31.149
|   |-- admin.example.com -> 185.199.110.133
|   `-- ssh.example.com -> 20.201.28.152
|-- [OPEN PORTS] 2 found
|   |-- 22 -> SSH
|   `-- 443 -> HTTPS
|-- [ADMIN PATHS] 6 found
|   |-- /wp-admin
|   |-- /dashboard
|   `-- /login
`-- [TECH STACK] 1 detected
    `-- Shopify
```

---

## Exposure Timeline

**VISUALIZE → TIMELINE** builds a chronological history of everything found:

```
-- 2007 ------------------------------------
|  Domain registered
|  Registrar: MarkMonitor, Inc.

-- 2026 ------------------------------------
|  [06/06/2026] VulnScan: HIGH=1 MEDIUM=1
|  [06/06/2026] 18 subdomain(s) mapped
|  [06/06/2026] Scan: HELLSCAN
|  [06/06/2026] Scan: SSL_CHECKER
|  [06/06/2026] SSL expires in: 57 days
`-------------------------------------------
```

---

## Dashboard

**DASHBOARD (15)** gives a terminal-based intelligence summary across all scanned targets:

```
  ┌─────────────────────────────────────┐
  │          INTELLIGENCE SUMMARY        │
  ├──────────────┬──────────────────────┤
  │ Targets      │ 3                    │
  │ Reports      │ 17                   │
  │ Vulns        │ 4                    │
  │ Open Ports   │ 9                    │
  │ Subdomains   │ 36                   │
  │ Leaks        │ 0                    │
  └──────────────┴──────────────────────┘
```

---

## Graph Export

**VISUALIZE → INTEL GRAPH** generates an interactive HTML visualization (vis-network) linking targets to their subdomains, open ports, vulnerabilities, technologies, ISP, and SSL CA in a navigable node graph.

Serve locally:
```bash
cd ~/cerberus/reports && python -m http.server 8080
```

---

## VULNSCAN Checks

| Check | Method |
|---|---|
| Security Headers | 6 critical response headers |
| SQL Injection | `?id=` with common payloads |
| Open Redirect | `?redirect=`, `?url=`, `?next=`, etc. |
| Admin Paths | `/admin`, `/dashboard`, `/login`, etc. |
| Reflected XSS | `?q=` with script/img/svg payloads |
| LFI | `?file=` with path traversal payloads |
| Directory Listing | `/uploads/`, `/backup/`, `/static/`, etc. |

---

## Tech Fingerprint — What It Detects

**CMS:** WordPress, Joomla, Drupal, Magento, Shopify, Wix, Ghost

**Frameworks:** React, Vue.js, Angular, Next.js, jQuery, Bootstrap, Tailwind

**Servers:** Apache, Nginx, IIS

**CDN/Infra:** Cloudflare, AWS CloudFront, Vercel, Netlify

**Languages:** PHP, ASP.NET, Python/Django, Node.js/Express

**Analytics:** Google Analytics, Google Tag Manager, Hotjar, Facebook Pixel

**Security:** reCAPTCHA, hCaptcha

---

## IP Recon — Fallback Cascade

```
1. ipwho.is     -> primary
2. ip-api.com   -> fallback
3. ipapi.co     -> last resort
```

---

## Tor / Anonymous Mode

**TOR (X)** toggles routing through Tor (`socks5h://127.0.0.1:9150`) and verifies the exit IP via `check.torproject.org`. When active, `[TOR ON]` appears next to the target in the menu.

```
[1] Enable Tor
[2] Disable Tor
[3] Check Tor IP
[4] Start Tor daemon
```

---

## Optional APIs

| API | Used in | Free tier | Link |
|---|---|---|---|
| Shodan | CHAIN RITUAL / internals | Yes (limited) | account.shodan.io |
| NumVerify | CHAIN RITUAL / internals | 100 req/month | numverify.com |

Configure via **(C) CONFIGURE**.

---

## Requirements

```bash
pip install requests[socks] python-whois
```

`requests[socks]` is required for Tor support.

---

## Project Structure

```
cerberus/
|-- cerberus.py            # Main entrypoint — menu, chain ritual, scoring
|-- README.md
|-- core/
|   |-- utils.py           # Colors, helpers, progress, quotes
|   |-- config.py          # Config load/save/configure
|   `-- grimoire.py        # Report save/list/export (HTML, Markdown)
|-- heads/
|   |-- head1_osint.py     # Soul search, correlate, email lookup
|   |-- head2_recon.py     # Domain, IP, hellscan, SSL, tech, subdomains
|   `-- head3_security.py  # Vulnscan, CVE, paste monitor, Shodan, cloud, phone
|-- modules/
|   `-- visualize.py       # Analyze, tree, timeline (unified intelligence module)
|-- logs/                  # Auto-created — scan reports (.txt)
|-- reports/               # Auto-created — HTML/MD exports
`-- config/
    `-- settings.json      # API keys and preferences
```

---

## Legal

This tool is for educational purposes and authorized security testing only.
The author is not responsible for misuse.

---

**github.com/lohjs-0/cerberu-osint**