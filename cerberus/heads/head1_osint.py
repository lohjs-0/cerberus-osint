import re
import requests
import datetime
from core.utils import R, D, G, Y, X, get_headers, get_proxies, progress, head_wake, head_done
from core.grimoire import grimoire_salvar
from core.config import config_load

SITES = {
    "GitHub"     : ("https://github.com/{}", "Not Found"),
    "Reddit"     : ("https://www.reddit.com/user/{}", "page not found"),
    "Twitter"    : ("https://twitter.com/{}", "this account doesn't exist"),
    "Instagram"  : ("https://www.instagram.com/{}/", "Page Not Found"),
    "TikTok"     : ("https://www.tiktok.com/@{}", "couldn't find this account"),
    "Pinterest"  : ("https://www.pinterest.com/{}/", "User not found"),
    "Twitch"     : ("https://www.twitch.tv/{}", "Sorry. Unless you"),
    "YouTube"    : ("https://www.youtube.com/@{}", "404"),
    "LinkedIn"   : ("https://www.linkedin.com/in/{}", "Page not found"),
    "Telegram"   : ("https://t.me/{}", "If you have Telegram"),
    "Medium"     : ("https://medium.com/@{}", "Page not found"),
    "GitLab"     : ("https://gitlab.com/{}", "404"),
    "Pastebin"   : ("https://pastebin.com/u/{}", "Not Found"),
    "HackerNews" : ("https://news.ycombinator.com/user?id={}", "No such user"),
    "Keybase"    : ("https://keybase.io/{}", "404"),
    "DevTo"      : ("https://dev.to/{}", "404"),
    "Replit"     : ("https://replit.com/@{}", "not found"),
    "Steam"      : ("https://steamcommunity.com/id/{}", "The specified profile could not be found"),
    "Spotify"    : ("https://open.spotify.com/user/{}", "Page not found"),
}


def soul_search(username):
    print("\n" + R + "  === SOUL SEARCH: " + username + " ===" + X + "\n")
    encontrados = []
    for site, (url, not_found_str) in SITES.items():
        try:
            link = url.format(username)
            r = requests.get(link, timeout=6, headers=get_headers(),
                             proxies=get_proxies(), allow_redirects=True)
            if r.status_code == 200 and not_found_str.lower() not in r.text.lower():
                print(G + "  [FOUND]     " + X + site.ljust(12) + " -> " + link)
                encontrados.append(link)
            else:
                print(D + "  [NOT FOUND] " + site + X)
        except:
            print(D + "  [ERROR]     " + site + X)
    print()
    print(R + "  " + str(len(encontrados)) + " profile(s) found" + X + "\n")
    return len(encontrados)


def correlate(username, target):
    print("\n" + R + "  === AUTO CORRELATION: " + username + " ===" + X + "\n")
    found = {}

    print(D + "  [1/5] GitHub profile..." + X)
    try:
        r = requests.get("https://api.github.com/users/" + username,
                         timeout=6, headers=get_headers(), proxies=get_proxies())
        if r.status_code == 200:
            data = r.json()
            fields = [
                ("email",    "Email",     data.get("email", "")),
                ("name",     "Name",      data.get("name", "")),
                ("blog",     "Blog/URL",  data.get("blog", "")),
                ("company",  "Company",   data.get("company", "")),
                ("location", "Location",  data.get("location", "")),
                ("bio",      "Bio",       data.get("bio", "")),
                ("repos",    "Repos",     str(data.get("public_repos", 0))),
                ("followers","Followers", str(data.get("followers", 0))),
                ("following","Following", str(data.get("following", 0))),
                ("created",  "Created",   str(data.get("created_at", ""))[:10]),
                ("updated",  "Updated",   str(data.get("updated_at", ""))[:10]),
                ("twitter",  "Twitter",   data.get("twitter_username", "")),
                ("url",      "Profile",   data.get("html_url", "")),
            ]
            for key, label, val in fields:
                if val and val not in ["None", "False", "0", ""]:
                    cor = G if key in ["email", "name", "blog", "twitter"] else D
                    print(cor + "  [" + label.ljust(10) + "] " + str(val)[:80] + X)
                    found[key] = val
        else:
            print(D + "  GitHub profile not found." + X)
    except Exception as e:
        print(D + "  [ERROR] " + str(e) + X)

    print("\n" + D + "  [2/5] Counting stars..." + X)
    try:
        stars = 0
        page  = 1
        while True:
            r = requests.get(
                "https://api.github.com/users/" + username + "/repos",
                params={"per_page": 100, "page": page},
                timeout=6, headers=get_headers(), proxies=get_proxies()
            )
            if r.status_code != 200:
                break
            repos_data = r.json()
            if not repos_data:
                break
            for repo in repos_data:
                stars += repo.get("stargazers_count", 0)
            if len(repos_data) < 100:
                break
            page += 1
        print(G + "  [Stars     ] " + str(stars) + " total across all repos" + X)
        found["stars"] = str(stars)
    except Exception as e:
        print(D + "  [ERROR] " + str(e) + X)

    print("\n" + D + "  [3/5] Checking recent commits for email..." + X)
    try:
        r = requests.get(
            "https://api.github.com/users/" + username + "/events/public",
            timeout=6, headers=get_headers(), proxies=get_proxies()
        )
        if r.status_code == 200:
            events       = r.json()
            commit_count = 0
            for event in events:
                if event.get("type") == "PushEvent":
                    payload = event.get("payload", {})
                    commits = payload.get("commits", [])
                    commit_count += len(commits)
                    for commit in commits:
                        author = commit.get("author", {})
                        email  = author.get("email", "")
                        if email and "noreply" not in email and "email" not in found:
                            print(G + "  [Email     ] " + email + " (from commit)" + X)
                            found["email"] = email
            print(D + "  [Commits   ] " + str(commit_count) + " in recent events" + X)
            found["recent_commits"] = str(commit_count)
    except Exception as e:
        print(D + "  [ERROR] " + str(e) + X)

    print("\n" + D + "  [4/5] Reading profile README..." + X)
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/" + username + "/" + username + "/main/README.md",
            timeout=6, headers=get_headers(), proxies=get_proxies()
        )
        if r.status_code != 200:
            r = requests.get(
                "https://raw.githubusercontent.com/" + username + "/" + username + "/master/README.md",
                timeout=6, headers=get_headers(), proxies=get_proxies()
            )
        if r.status_code == 200:
            readme = r.text
            print(G + "  [README    ] Found (" + str(len(readme)) + " chars)" + X)
            found["readme"] = readme[:200]
            emails_readme = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", readme)
            for em in emails_readme:
                if "email" not in found or not found["email"]:
                    print(G + "  [Email     ] " + em + " (from README)" + X)
                    found["email"] = em
                else:
                    print(D + "  [Email alt ] " + em + X)
            links = re.findall(r"https?://[^\s\)\]]+", readme)
            for link in links[:5]:
                print(D + "  [Link      ] " + link + X)
        else:
            print(D + "  No profile README found." + X)
    except Exception as e:
        print(D + "  [ERROR] " + str(e) + X)

    print("\n" + D + "  [5/5] Correlating with domain/IP..." + X)
    domains_to_check = []

    if "email" in found:
        email_domain = found["email"].split("@")[-1]
        if email_domain not in ["gmail.com", "yahoo.com", "hotmail.com",
                                 "outlook.com", "proton.me", "icloud.com"]:
            domains_to_check.append(email_domain)
            print(D + "  -> Email domain: " + email_domain + X)

    if "blog" in found and found["blog"]:
        blog = found["blog"].replace("https://", "").replace("http://", "").rstrip("/")
        if blog and "." in blog:
            domains_to_check.append(blog)
            print(D + "  -> Blog domain: " + blog + X)

    for domain in list(set(domains_to_check)):
        from heads.head2_recon import domain_curse, ip_recon
        print("\n" + R + "  [AUTO] DOMAIN CURSE -> " + domain + X)
        try:
            domain_curse(domain)
        except Exception as e:
            print(D + "  [ERROR] " + str(e) + X)
        print("\n" + R + "  [AUTO] IP RECON -> " + domain + X)
        try:
            ip_recon(domain)
        except Exception as e:
            print(D + "  [ERROR] " + str(e) + X)

    if "email" in found:
        from heads.head3_security import paste_monitor
        print("\n" + R + "  [AUTO] PASTE MONITOR -> " + found["email"] + X)
        try:
            paste_monitor(found["email"])
        except Exception as e:
            print(D + "  [ERROR] " + str(e) + X)

    saida = "[CORRELATION] " + username + "\n\n"
    for k, v in found.items():
        if k != "readme":
            saida += "  " + k.ljust(15) + ": " + str(v) + "\n"
    if domains_to_check:
        saida += "\n  Domains correlated:\n"
        for d in domains_to_check:
            saida += "  -> " + d + "\n"

    caminho = grimoire_salvar(username, "correlation", saida)
    print("\n" + R + "  Report saved: " + X + caminho + "\n")
    return found


def email_lookup():
    print("\n" + R + "  === EMAIL LOOKUP ===" + X + "\n")
    email = input(R + "  Email: " + X).strip()
    if "@" not in email:
        print(R + "  Invalid email." + X + "\n")
        return
    domain = email.split("@")[1]
    saida  = "[EMAIL LOOKUP] " + email + "\n\n"

    print(R + "  [BREACH CHECK]" + X)
    try:
        r = requests.get(
            "https://leakcheck.io/api/public?check=" + email,
            timeout=8, headers={"User-Agent": "Cerberus-OSINT"}, proxies=get_proxies()
        )
        data = r.json()
        if data.get("success"):
            found = data.get("found", 0)
            if found > 0:
                print(Y + "  [!] Found in " + str(found) + " breach(es):" + X)
                for s in data.get("sources", []):
                    linha = "  -> " + s.get("name", "?") + " (" + s.get("date", "?") + ")"
                    print(Y + linha + X)
                    saida += linha + "\n"
            else:
                print(G + "  [OK] Not found in any known breach." + X)
        else:
            print(D + "  " + data.get("error", "Check failed.") + X)
    except Exception as e:
        print(D + "  [BREACH] Error: " + str(e) + X)

    print()
    print(R + "  [GRAVATAR]" + X)
    try:
        import hashlib
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        r = requests.get("https://www.gravatar.com/" + email_hash + ".json",
                         timeout=5, proxies=get_proxies())
        if r.status_code == 200:
            entry  = r.json()["entry"][0]
            nome   = entry.get("displayName", "N/A")
            perfil = entry.get("profileUrl", "N/A")
            print(G + "  [FOUND] Name    : " + nome + X)
            print(G + "  [FOUND] Profile : " + perfil + X)
            saida += "  Gravatar: " + nome + " -- " + perfil + "\n"
        else:
            print(D + "  No Gravatar profile found." + X)
    except Exception as e:
        print(D + "  [GRAVATAR] Error: " + str(e) + X)

    print()
    print(R + "  [DOMAIN MX]" + X)
    try:
        r = requests.get("https://dns.google/resolve?name=" + domain + "&type=MX", timeout=5)
        for a in r.json().get("Answer", []):
            linha = "  MX : " + a["data"]
            print(D + linha + X)
            saida += linha + "\n"
    except Exception as e:
        print(D + "  [MX] Error: " + str(e) + X)

    print()
    caminho = grimoire_salvar(email.replace("@", "_at_"), "email_lookup", saida)
    print(R + "  Report saved: " + X + caminho + "\n")