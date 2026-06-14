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

When you run **CHAIN RITUAL (4)**, all three heads analyze the target in sequence and produce a scored judgment:

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

## Install & Run

```bash
git clone https://github.com/lohjs-0/cerberus
cd cerberus
pip install requests python-whois
python3 cerberus.py
```

---

## Modules

### Core (1–9)

| # | Module | Description |
|---|---|---|
| 1 | SOUL SEARCH | Username lookup across social platforms |
| 2 | DOMAIN CURSE | WHOIS, DNS records, HTTP headers |
| 3 | HELLSCAN | Port scanner — 15 common ports |
| 4 | CHAIN RITUAL | Full pipeline across all three heads + Judgment |
| 5 | GRIMOIRE | Report manager — list and browse saved scans |
| 6 | DORKS | 9 preset Google dorks + custom input |
| 7 | UNDERWORLD | Subdomain finder + email OSINT |
| 8 | CONFIGURE | API keys and settings |
| 9 | VULNSCAN | Headers, SQLi, XSS, LFI, redirects, admin paths |

### Extended (10–16)

| # | Module | Description |
|---|---|---|
| 10 | PHONE OSINT | Phone number analysis — country, region, carrier |
| 11 | SHODAN | Device/service data via Shodan API |
| 12 | SSL CHECK | Certificate validity, TLS version audit, HSTS |
| 13 | TECH SCAN | Stack fingerprinting — CMS, frameworks, CDN, analytics |
| 14 | CVE LOOKUP | Real-time NVD query by product or CVE ID |
| 15 | PASTE MONITOR | Public paste and breach search |
| 16 | EXPORT HTML | Visual HTML report from all saved scans |

### Intelligence (17–22)

| # | Module | Description |
|---|---|---|
| 17 | ANALYZE | Reads saved reports and generates interpreted intelligence |
| 18 | TREE | Visual discovery tree — subdomains, ports, paths, stack |
| 19 | TIMELINE | Exposure timeline built from all scans on the target |
| 20 | SOCIAL GRAPH | Username connection mapping |
| 21 | CERBERUS WATCH | Monitoring daemon — continuous target surveillance |
| 22 | GRAPH | Interactive HTML graph (vis-network) of all findings |

### Utility (23–28)

| # | Module | Description |
|---|---|---|
| 23 | CLEAR LOGS | Delete all saved logs for a target |
| 24 | EXPORT MD | Markdown report — compatible with Obsidian |
| 25 | CORRELATE | Auto-correlation — username → domain pivot |
| 26 | DASHBOARD | Terminal intelligence summary across all targets |
| 27 | TOR | Anonymous mode — toggle Tor proxy, check IP |
| 28 | CLOUD SCAN | Exposed bucket/resource check — S3, Firebase, GCP, Azure |

---

## Intelligence Layer

Instead of listing raw findings, **ANALYZE (17)** interprets them:

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

## Discovery Tree

**TREE (18)** maps everything found into a structured view:

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

**TIMELINE (19)** builds a chronological history of everything found:

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

**DASHBOARD (26)** gives a terminal-based intelligence summary across all scanned targets:

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

**GRAPH (22)** generates an interactive HTML visualization (vis-network) linking targets to their subdomains, open ports, vulnerabilities, technologies, ISP, and SSL CA in a navigable node graph.

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

**TOR (27)** toggles routing through Tor (`socks5h://127.0.0.1:9050`) and verifies the exit IP via `check.torproject.org`. When active, `[TOR ON]` appears next to the target in the menu.

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
| Shodan | Module 11 | Yes (limited) | account.shodan.io |
| NumVerify | Module 10 | 100 req/month | numverify.com |

Configure via `(8) CONFIGURE`.

---

## Requirements

```bash
pip install requests python-whois
```

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
|   |-- analyze.py         # Intelligence report
|   |-- tree.py            # Discovery tree
|   `-- timeline.py        # Exposure timeline
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

**github.com/lohjs-0/cerberus**