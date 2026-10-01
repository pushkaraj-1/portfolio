#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emits the static site using the ported al-folio-free layout
(structure and class names follow the reference two-column design).

Run:  python3 tools/build_site.py
"""
import os, sys, json, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import (SITE, QUICK_FACTS, EXPERIENCE, EDUCATION, SKILLS,
                     RESEARCH, TALKS, ACTIVITIES, AWARDS, NEWS)
from projects_data import PROJECTS

def rel(d): return "../" * d

def asset_ver(name):
    """Content hash appended to CSS/JS links, so browsers refetch them after a change."""
    import hashlib
    return hashlib.md5(open(os.path.join(ROOT, name), "rb").read()).hexdigest()[:8]

# ------------------------------------------------------------------ icons
I_CODE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 19c-5 '
          '1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 '
          '0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 '
          '5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 '
          '7A3.37 3.37 0 0 0 9 18.13V22"/></svg>')
I_LIVE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 '
          '2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/>'
          '<line x1="10" y1="14" x2="21" y2="3"/></svg>')
I_DOC  = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 '
          '0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
          '</svg>')
LINK_ICON = {"Code": I_CODE, "GitHub": I_CODE, "Live demo": I_LIVE, "Live site": I_LIVE,
             "Paper": I_DOC, "Writeup": I_DOC}

SOC = {
 "mail": ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#EA4335" d="M22 6c0-1.1-.9-2-2-2H4c-1.1 '
          '0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0l-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z"/></svg>'),
 "github": ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 0C5.37 0 0 5.37 0 '
            '12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015'
            '.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 '
            '1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335'
            '-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 '
            '1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 '
            '1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 '
            '3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'),
 "linkedin": ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0'
              '-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 '
              '1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063'
              '-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 '
              '13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 '
              '24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'),
 "scholar": ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M12 24a7 7 0 110-14 7 7 0 010 '
             '14zm0-24L0 9.5l4.838 3.94A8 8 0 0112 9a8 8 0 017.162 4.44L24 9.5z"/></svg>'),
}

NAV = [("index.html", "About"), ("news.html", "News"), ("experience.html", "Experience"),
       ("projects.html", "Projects"), ("skills.html", "Skills"),
       ("education.html", "Education"), ("activities.html", "Service")]

def esc(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ shell
def resume_ctas(r=""):
    v = SITE["resume_view_url"]
    view = (f'<a class="btn btn-solid btn-small" href="{v}" target="_blank" rel="noopener">View resume</a>'
            if v else '<a class="btn btn-solid btn-small is-disabled" href="#" aria-disabled="true" '
                      'title="Set resume_view_url in tools/content.py">View resume</a>')
    return (f'{view}<a class="btn btn-outline btn-small" '
            f'href="{r}{SITE["resume_download_url"]}" download>Download resume</a>')

def shell(title, body, depth=0, desc="", active="", footer_links=True):
    r = rel(depth)
    nav = "".join(f'<li><a href="{r}{h}" class="nav-link{" active" if h==active else ""}">{n}</a></li>'
                  for h, n in NAV)
    flinks = "".join(f'<a href="{r}{h}">{n}</a>' for h, n in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc or SITE['tagline'])}">
<meta name="theme-color" content="#1e3a8a">
<link rel="stylesheet" href="{r}styles.css?v={asset_ver('styles.css')}">
<link rel="icon" href="{r}{SITE['photo']}">
<script>
(function(){{try{{var t=localStorage.getItem('theme');
if(t!=='light'&&t!=='dark'){{t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}}
document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();
</script>
</head>
<body>
<header class="site-header">
  <nav class="container nav">
    <div class="nav-left">
      <a class="nav-brand" href="{r}index.html">{esc(SITE['name'])}</a>
      <div class="nav-cta">{resume_ctas(r)}</div>
    </div>
    <div class="nav-right">
      <ul class="nav-links" id="primary-navigation">{nav}
        <li class="nav-search"><div class="search-wrap">
          <input id="site-search" type="search" placeholder="Search…" autocomplete="off"
                 aria-label="Search the site" data-base="{r}">
          <div id="search-results" class="search-results" hidden></div>
        </div></li>
      </ul>
      <button class="theme-toggle" type="button" aria-label="Switch to dark theme" aria-pressed="false" title="Toggle theme">
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
      </button>
      <button class="nav-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="primary-navigation" title="Menu">&#9776;</button>
    </div>
  </nav>
</header>
{body}
<footer class="site-footer">
  <div class="container footer-inner">
    <div>&copy; <span id="year"></span> {esc(SITE['name'])}</div>
    <div class="footer-links">{flinks if footer_links else ''}</div>
  </div>
</footer>
<script src="{r}script.js?v={asset_ver('script.js')}" defer></script>
</body>
</html>
"""

# -------------------------------------------------------------- components
# logos that carry their own background and should fill the logo box edge to edge
FULL_BLEED_LOGOS = {"assets/img/logos/usc-shield.png"}

def logo(src, alt, r=""):
    if not src:  # no logo file: show the org's initials instead of an empty slot
        initials = "".join(w[0] for w in re.sub(r"[^A-Za-z ]", " ", alt).split()[:2]).upper()
        return f'<span class="company-logo logo-mono" aria-hidden="true">{initials}</span>'
    fill = " logo-fill" if src in FULL_BLEED_LOGOS else ""
    return (f'<img src="{r}{src}" alt="{esc(alt)}" class="company-logo{fill} lazy-img" loading="lazy" '
            f'decoding="async" width="48" height="48" onerror="this.remove()">')

def exp_li(e, r="", full=True):
    adv = f' &middot; under {e["advisor"]}' if e.get("advisor") else ""
    org = (f'<a href="{e["org_url"]}" target="_blank" rel="noopener">{e["org"]}</a>'
           if e["org_url"] else e["org"])
    if full:
        detail = "<ul class='exp-points'>" + "".join(f"<li>{p}</li>" for p in e["points"]) + "</ul>"
        detail += '<div class="tag-row">' + "".join(f'<span class="tag">{t}</span>' for t in e["tags"]) + '</div>'
    else:
        detail = f'<p class="item-desc">{e["summary"]}</p>'
    return f"""<li>
  <div class="exp-header">
    {logo(e["logo"], e["org"], r)}
    <div class="exp-title-group">
      <div class="item-title">{e["role"]} | {org}</div>
      <div class="item-meta">{e["location"]} &middot; {e["dates"]}{adv}</div>
    </div>
  </div>
  {detail}
</li>"""

def proj_li(p, r=""):
    links = "".join(
        f'<a href="{r}projects/{p["slug"]}.html" aria-label="Details" title="Details">{I_DOC}</a>')
    for n, u in p["links"]:
        links += f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">{LINK_ICON.get(n, I_LIVE)}</a>'
    return f"""<li>
  <div class="item-header">
    <span class="item-title"><a href="{r}projects/{p['slug']}.html">{p['title']}</a></span>
    <div class="item-links">{links}</div>
  </div>
  <p class="item-desc">{p['short']}</p>
</li>"""

def pub_article(rp, r=""):
    acts = "".join(f'<a class="btn-chip" href="{u}" target="_blank" rel="noopener">{n}</a>'
                   for n, u in rp["links"])
    badge = f'<span class="pub-badge">{rp["note"]}</span>' if rp.get("note") else ""
    return f"""<article class="pub-card">
  <a class="pub-thumb" href="{rp['links'][0][1]}" target="_blank" rel="noopener">
    <img src="{r}{rp['image']}" alt="{esc(rp['title'])} figure" class="lazy-img" loading="lazy" decoding="async">
  </a>
  <div class="pub-body">
    <h4 class="pub-title">{rp['title']} {badge}</h4>
    <div class="pub-meta">{rp['authors']} &middot; <span class="pub-venue">{rp['venue']}</span></div>
    <p class="item-desc">{rp['abstract']}</p>
    <div class="pub-actions">{acts}</div>
  </div>
</article>"""

def talk_article(t, r=""):
    acts = f'<a class="btn-chip" href="{r}talks/{t["slug"]}.html">Write-up</a>' + "".join(
        f'<a class="btn-chip" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in t["links"])
    return f"""<article class="pub-card">
  <a class="pub-thumb" href="{r}talks/{t['slug']}.html">
    <img src="{r}{t['image']}" alt="{esc(t['title'])} figure" class="lazy-img" loading="lazy" decoding="async">
  </a>
  <div class="pub-body">
    <h4 class="pub-title">{t['title']} <span class="pub-badge">Talk</span></h4>
    <div class="pub-meta">{t['paper_authors']} &middot; <span class="pub-venue">{t['paper_venue']}</span></div>
    <div class="pub-meta">Presented in {t['context']}</div>
    <p class="item-desc">{t['abstract']}</p>
    <div class="pub-actions">{acts}</div>
  </div>
</article>"""

def activity_li(a, r=""):
    dates = f'<div class="item-meta">{a["dates"]}</div>' if a.get("dates") else ""
    return f"""<li>
  <div class="exp-header">
    {logo(a["logo"], a["title"], r)}
    <div class="exp-title-group">
      <div class="item-title">{a['role']} | {a['title']}</div>
      {dates}
    </div>
  </div>
  <p class="item-desc">{a['desc']}</p>
</li>"""

def sec(id_, title, inner, cls="section", more=None, r=""):
    # h2 must stay a direct child of .container: the panel legend style targets it
    m = (f'<div class="section-more-wrap"><a class="section-more" href="{r}{more[0]}">'
         f'{more[1]} &rarr;</a></div>') if more else ""
    return f"""<section id="{id_}" class="{cls}">
  <div class="container">
    <h2>{title}</h2>
    <div class="section-divider"></div>
    {inner}
    {m}
  </div>
</section>"""

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

def news_date(d):
    """'2026-09' -> 'Sep 2026'; '2026-09-24' -> 'Sep 24, 2026'."""
    parts = d.split("-")
    mon = MONTHS[int(parts[1]) - 1]
    return f"{mon} {int(parts[2])}, {parts[0]}" if len(parts) == 3 else f"{mon} {parts[0]}"

def news_table(extra_cls=""):
    rows = "".join(f'<tr><th scope="row"><time datetime="{d}">{news_date(d)}</time></th><td>{txt}</td></tr>'
                   for d, _lbl, txt in NEWS)
    return f'<table class="news-table {extra_cls}"><tbody>{rows}</tbody></table>'

def scroll_card(inner_ul, extra=""):
    return (f'<div class="scroll-card {extra}" data-scroll>'
            f'<span class="scroll-hint">Scroll</span>{inner_ul}</div>')

def skills_block():
    return '<div class="skills-grid">' + "".join(
        f'<div class="skill-group"><h3>{g}</h3><div class="tag-row">'
        + "".join(f'<span class="tag">{k}</span>' for k in ks) + '</div></div>'
        for g, ks in SKILLS) + '</div>'

def edu_block(r="", full=True):
    out = []
    for e in EDUCATION:
        school = (f'<a href="{e["url"]}" target="_blank" rel="noopener">{e["school"]}</a>'
                  if e["url"] else e["school"])
        courses = (f'<p class="item-desc"><span class="courses-label">Coursework</span> '
                   f'{", ".join(e["courses"])}</p>' if full else "")
        out.append(f"""<li>
  <div class="exp-header">
    {logo(e["logo"], e["school"], r)}
    <div class="exp-title-group">
      <div class="item-title">{school}</div>
      <div class="item-meta">{e["degree"]} &middot; {e["dates"]} &middot; {e["location"]}</div>
      <div class="item-meta">{e["score"]}</div>
    </div>
  </div>
  {courses}
</li>""")
    return '<ul class="clean-list awards-list">' + "".join(out) + '</ul>'

# ------------------------------------------------------------------ pages
def page_index():
    facts = "".join(f'<div class="fact"><dt class="fact-k">{k}</dt><dd class="fact-v">{v}</dd></div>'
                    for k, v in QUICK_FACTS)
    soc_items = [("mail", "mailto:" + SITE["email"], "Email"),
                 ("github", SITE["github"], "GitHub"),
                 ("linkedin", SITE["linkedin"], "LinkedIn")]
    if SITE.get("scholar"):
        soc_items.append(("scholar", SITE["scholar"], "Google Scholar"))
    parts = []
    for k, u, lbl in soc_items:
        tgt = "" if u.startswith("mailto") else ' target="_blank" rel="me noopener"'
        parts.append('<a href="%s" class="social-icon %s" aria-label="%s"%s>%s</a>'
                     % (u, k, lbl, tgt, SOC[k]))
    socials = "".join(parts)

    about = f"""<section id="about" class="section profile">
  <div class="hero-left">
    <img src="{SITE['photo']}" alt="{esc(SITE['name'])}" class="headshot round" loading="eager"
         decoding="async" width="800" height="800"
         onerror="this.onerror=null;this.src='assets/img/profile-placeholder.svg'">
    <h1 class="hero-title">{esc(SITE['name'])}</h1>
    <div class="hero-subline">
      <p class="hero-subtitle">{SITE['role']}</p>
      <div class="social-text" aria-label="Profiles and contact">{socials}</div>
    </div>
    <p>{SITE['blurb']}</p>
    <p>{SITE['tagline']}</p>
    {f'<p class="status-line">{SITE["status"]}</p>' if SITE.get("status") else ""}
    <div class="nav-cta hero-cta">{resume_ctas()}</div>
    <dl class="facts">{facts}</dl>
  </div>
</section>"""

    news = sec("news", "News",
        scroll_card(f'<div class="scroll-body">{news_table()}</div>'),
        more=("news.html", "All news"))

    service = sec("service", "Service &amp; Activities",
        '<ul class="clean-list awards-list">' + "".join(activity_li(a) for a in ACTIVITIES) + '</ul>',
        more=("activities.html", "All"))

    # projects split into two columns by category grouping
    groups = {}
    for p in PROJECTS:
        groups.setdefault(p["category"], []).append(p)
    keys = list(groups)
    half = (len(keys) + 1) // 2
    cols = []
    for chunk in (keys[:half], keys[half:]):
        inner = ""
        for k in chunk:
            inner += (f'<h3>{k}</h3><ul class="clean-list">'
                      + "".join(proj_li(p) for p in groups[k]) + '</ul>')
        cols.append(f'<div class="projects-column">{inner}</div>')
    projects = sec("projects", "Selected Projects",
        f'<div class="projects-grid">{"".join(cols)}</div>',
        cls="section projects-section", more=("projects.html", "All projects"))

    experience = sec("experience", "Experience",
        scroll_card('<ul class="clean-list experience-list scroll-body">'
                    + "".join(exp_li(e, "", full=False) for e in EXPERIENCE) + '</ul>',
                    "experience-scroll"),
        more=("experience.html", "Full detail"))

    talks = ('<h3 class="sub-h3">Paper presentations</h3><div class="pub-list">'
             + "".join(talk_article(t) for t in TALKS) + '</div>') if TALKS else ""
    pubs = sec("publications", "Research &amp; Publications",
        '<div class="pub-list">' + "".join(pub_article(r) for r in RESEARCH) + '</div>' + talks)

    skills = sec("skills", "Skills", skills_block(), more=("skills.html", "All"))
    edu = sec("education", "Education", edu_block(full=False), more=("education.html", "Details"))

    body = f"""<main class="container page-layout">
  <div class="sidebar">
    {about}
    {news}
    {service}
    {projects}
  </div>
  <div class="content">
    {experience}
    {pubs}
    {skills}
    {edu}
  </div>
</main>"""
    return shell(f"{SITE['name']} | {SITE['role']}", body, 0, SITE["tagline"], "index.html")

def simple_page(title, lede, inner, active, depth=0):
    body = f"""<main class="container inner-page">
  <section class="section">
    <div class="container">
      <h1 class="page-title">{title}</h1>
      <div class="section-divider"></div>
      {f'<p class="page-lede">{lede}</p>' if lede else ""}
      {inner}
    </div>
  </section>
</main>"""
    return shell(f"{re.sub('<[^>]+>', '', title)} | {SITE['name']}", body, depth, strip(lede), active)

def page_experience():
    inner = ('<ul class="clean-list experience-list detailed">'
             + "".join(exp_li(e, "", full=True) for e in EXPERIENCE) + '</ul>')
    inner += ('<h2 class="sub-h2">Awards &amp; Recognition</h2><div class="section-divider"></div>'
              '<ul class="clean-list awards-list">'
              + "".join(f'<li><div class="item-header"><span class="item-title">{t}</span>'
                        f'<span class="item-meta">{d}</span></div></li>' for t, d in AWARDS)
              + '</ul>')
    return simple_page("Experience",
        "Industry, research, and teaching roles across search &amp; recommendation, real-time "
        "computer vision, edge ML, and backend engineering.",
        inner, "experience.html")

def page_projects():
    groups = {}
    for p in PROJECTS:
        groups.setdefault(p["category"], []).append(p)
    inner = ""
    for k, ps in groups.items():
        inner += (f'<h2 class="sub-h2">{k}</h2><div class="section-divider"></div>'
                  f'<ul class="clean-list">' + "".join(proj_li(p) for p in ps) + '</ul>')
    return simple_page("Projects", "", inner, "projects.html")

def page_news():
    return simple_page("News", "Degrees, roles, projects, talks, hackathons, and service, newest first.",
                       news_table("news-full"), "news.html")

def page_skills():
    return simple_page("Skills", "Languages, frameworks, and the areas I have shipped in.",
                       skills_block(), "skills.html")

def page_education():
    return simple_page("Education", "Degrees and coursework.", edu_block(full=True), "education.html")

def page_activities():
    return simple_page("Service &amp; Activities",
        "Community, mentorship, and the things outside the code.",
        '<ul class="clean-list awards-list">' + "".join(activity_li(a) for a in ACTIVITIES) + '</ul>',
        "activities.html")

def page_project(p):
    body_html = (p["body"].replace('src="assets/', 'src="../assets/')
                          .replace('href="assets/', 'href="../assets/'))
    links = "".join(f'<a class="btn-chip" href="{u}" target="_blank" rel="noopener">{n}</a>'
                    for n, u in p["links"])
    tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    body = f"""<main class="container inner-page">
  <section class="section">
    <div class="container">
      <a class="back-link" href="../projects.html">&larr; All projects</a>
      <div class="item-meta">{p['category']} &middot; {p['dates']}</div>
      <h1 class="page-title">{p['title']}</h1>
      <div class="section-divider"></div>
      <p class="page-lede">{p['tagline']}</p>
      <div class="tag-row">{tags}</div>
      <div class="pub-actions">{links}</div>
      <div class="prose">{body_html}</div>
    </div>
  </section>
</main>"""
    return shell(f"{p['title']} | {SITE['name']}", body, 1, p["tagline"], "projects.html")

def page_talk(t):
    links = "".join(f'<a class="btn-chip" href="{u}" target="_blank" rel="noopener">{n}</a>'
                    for n, u in t["links"])
    body_html = (t["body"].replace('src="assets/', 'src="../assets/')
                          .replace('href="assets/', 'href="../assets/'))
    body = f"""<main class="container inner-page">
  <section class="section">
    <div class="container">
      <a class="back-link" href="../index.html#publications">&larr; Research &amp; Publications</a>
      <div class="item-meta">Paper presentation &middot; {t['context']}</div>
      <h1 class="page-title">{t['title']}</h1>
      <div class="section-divider"></div>
      <p class="page-lede">{t['paper_authors']} &middot; {t['paper_venue']}</p>
      <div class="pub-actions">{links}</div>
      <div class="prose">{body_html}</div>
    </div>
  </section>
</main>"""
    return shell(f"{strip(t['title'])} | {SITE['name']}", body, 1, strip(t["abstract"]), "index.html")

# --------------------------------------------------------------- search idx
def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def build_index():
    idx = []
    for p in PROJECTS:
        idx.append({"t": p["title"], "k": "Project", "u": f"projects/{p['slug']}.html",
                    "d": strip(p["tagline"]),
                    "s": strip(p["title"] + " " + p["tagline"] + " " + " ".join(p["tags"]) + " " + p["body"])[:1800]})
    for e in EXPERIENCE:
        idx.append({"t": f'{strip(e["role"])} at {e["org"]}', "k": "Experience", "u": "experience.html",
                    "d": strip(e["summary"]),
                    "s": strip(" ".join([e["role"], e["org"], e["summary"], *e["points"], *e["tags"]]))})
    for e in EDUCATION:
        idx.append({"t": e["school"], "k": "Education", "u": "education.html",
                    "d": f'{e["degree"]} · {e["score"]}',
                    "s": strip(" ".join([e["school"], e["degree"], *e["courses"]]))})
    for g, ks in SKILLS:
        idx.append({"t": g, "k": "Skills", "u": "skills.html", "d": ", ".join(ks),
                    "s": g + " " + " ".join(ks)})
    for r in RESEARCH:
        idx.append({"t": r["title"], "k": "Research", "u": "index.html#publications",
                    "d": f'{r["authors"]} · {r["venue"]}',
                    "s": strip(" ".join([r["title"], r["venue"], r["abstract"]]))})
    for t in TALKS:
        idx.append({"t": t["title"], "k": "Talk", "u": f"talks/{t['slug']}.html",
                    "d": strip(t["abstract"]),
                    "s": strip(" ".join([t["title"], t["paper_venue"], t["abstract"], t["body"]]))[:1800]})
    for a in ACTIVITIES:
        idx.append({"t": a["title"], "k": "Service", "u": "activities.html",
                    "d": strip(a["desc"]), "s": strip(" ".join([a["title"], a["role"], a["desc"]]))})
    return idx

def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)
    return path

def main():
    out = [write("index.html", page_index()),
           write("news.html", page_news()),
           write("experience.html", page_experience()),
           write("projects.html", page_projects()),
           write("skills.html", page_skills()),
           write("education.html", page_education()),
           write("activities.html", page_activities())]
    for p in PROJECTS:
        out.append(write(f"projects/{p['slug']}.html", page_project(p)))
    for t in TALKS:
        out.append(write(f"talks/{t['slug']}.html", page_talk(t)))
    idx = build_index()
    write("search-index.json", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))
    print(f"built {len(out)+1} files, search index: {len(idx)} entries")

if __name__ == "__main__":
    main()
