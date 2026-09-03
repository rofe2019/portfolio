#!/usr/bin/env python3
"""Generate index.html and the landingN.html project pages from tools/projects.json.

Usage:  python3 tools/build.py
Requires Pillow (pip install pillow) to read image sizes.
"""
import html
import json
import os
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = json.loads((ROOT / "tools" / "projects.json").read_text(encoding="utf-8"))

SITE_NAME = "Rafah Al Kassar"
EMAIL = "Rafah.ka-97@hotmail.com"
LOCATION = "Damascus, Syria"
SOCIAL = [
    ("LinkedIn", "fab fa-linkedin-in", "https://www.linkedin.com/in/rafah-alkassar-0546071b4"),
    ("GitHub", "fab fa-github", "https://github.com"),
    ("Instagram", "fab fa-instagram", "https://www.instagram.com/Rafah.alkassar"),
    ("Facebook", "fab fa-facebook-f", "https://www.facebook.com/profile.php?id=100001668728883"),
]

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E"
    "%3Cstop offset='0' stop-color='%2322d3ee'/%3E%3Cstop offset='.55' stop-color='%238b5cf6'/%3E"
    "%3Cstop offset='1' stop-color='%23f472b6'/%3E%3C/linearGradient%3E%3C/defs%3E"
    "%3Crect width='64' height='64' rx='16' fill='url(%23g)'/%3E"
    "%3Ctext x='32' y='43' text-anchor='middle' font-family='Menlo,monospace' font-weight='800' "
    "font-size='34' fill='%230a0d16'%3ER%3C/text%3E%3C/svg%3E"
)

LINK_META = {
    "apple": ("fab fa-apple", "App Store"),
    "play": ("fab fa-google-play", "Google Play"),
    "huawei": ("fas fa-store", "AppGallery"),
    "demo": ("fas fa-play-circle", "Watch Demo"),
    "youtube": ("fab fa-youtube", "Watch on YouTube"),
}

CAT_LABEL = {"mobile": "Mobile App", "web": "Web Platform", "ai": "AI / ML"}

MARQUEE = [
    "Flutter", "Dart", "Swift", "Kotlin", "React", "Angular", "TypeScript", "Java",
    "Spring Boot", "Supabase", "Firebase", "PostgreSQL", "REST APIs", "n8n", "LLM Agents", "WordPress",
]

SERVICES = [
    ("fas fa-mobile-alt", "Mobile Application Developer",
     "I craft beautiful, functional mobile experiences using Flutter, Swift, and modern technologies. "
     "With a passion for clean code and intuitive design, I bring ideas to life on iOS and Android.",
     ["Flutter", "Swift", "Kotlin", "Firebase", "App Store & Play"]),
    ("fas fa-layer-group", "Full Stack Web Developer",
     "I build modern, scalable, high-performance web applications: responsive frontends, secure backends, "
     "and databases, all designed as complete end-to-end solutions focused on performance and clean architecture.",
     ["React", "Angular", "Spring Boot", "Supabase", "REST APIs"]),
    ("fas fa-robot", "AI Agents & Automation",
     "I build intelligent AI agents and automation workflows using n8n, modern LLM technologies, and advanced "
     "AI development tools: automated business processes, AI-powered assistants, and smart integrations.",
     ["n8n", "LLM Agents", "Workflow Orchestration", "AI Integrations"]),
]

SKILLS = [
    ("fas fa-mobile-alt", "Mobile", ["Flutter", "Dart", "Swift / iOS", "Kotlin / Android", "Firebase", "Push Notifications", "In-App Payments"]),
    ("fas fa-code", "Frontend", ["React", "Angular", "TypeScript", "HTML5 / CSS3", "Responsive UI", "WordPress"]),
    ("fas fa-server", "Backend & Cloud", ["Java Spring Boot", "REST APIs", "Supabase", "PostgreSQL", "Firebase", "Auth & Security"]),
    ("fas fa-robot", "AI & Automation", ["n8n Workflows", "AI Agents", "LLM Integrations", "Prompt Engineering", "Deep Learning", "NLP"]),
]

AI_TOOLS = [
    ("Cursor", "assets/icons-ai/cursor.png"),
    ("Codex", "assets/icons-ai/codex.png"),
    ("ChatGPT", "assets/icons-ai/chatgpt.svg"),
    ("Gemini", "assets/icons-ai/gemini.svg"),
    ("Claude", "assets/icons-ai/claude.png"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def img_info(path: str):
    with Image.open(ROOT / path) as im:
        w, h = im.size
        alpha = im.mode in ("RGBA", "LA", "P")
    return w, h, alpha


def thumb_class(p) -> str:
    """How to render a project's icon inside a thumbnail."""
    if p["kind"] == "web":
        return "wide"
    w, h, _alpha = img_info(p["icon"])
    ratio = w / h
    if 0.9 <= ratio <= 1.1:
        return "rounded"
    if ratio >= 1.5 and not _alpha:
        return "wide"
    return "logo"


def thumb_src(p) -> str:
    return p.get("hero", p["icon"]) if p["kind"] == "web" else p["icon"]


def hue(i: int) -> int:
    return (200 + i * 47) % 360


def head(title: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title>{esc(title)}</title>
	<meta name="description" content="{esc(description)}" />
	<meta name="theme-color" content="#070a12" />
	<meta property="og:title" content="{esc(title)}" />
	<meta property="og:description" content="{esc(description)}" />
	<meta property="og:type" content="website" />
	<link rel="icon" href="{FAVICON}" />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />
	<link rel="stylesheet" href="assets/css/fontawesome-all.min.css" />
	<link rel="stylesheet" href="assets/css/site.css" />
</head>
<body>
"""


def nav(prefix: str = "") -> str:
    items = [("about", "About"), ("skills", "Skills"), ("projects", "Projects"), ("contact", "Contact")]
    links = "\n".join(f'\t\t\t<a href="{prefix}#{i}">{l}</a>' for i, l in items)
    return f"""	<header class="site-nav">
		<div class="container">
			<a class="brand" href="index.html" aria-label="{SITE_NAME} home">
				<span class="brand-mark">R</span>
				Rafah <span>Al Kassar</span>
			</a>
			<nav class="nav-links" aria-label="Primary">
{links}
				<a class="mobile-cta" href="mailto:{EMAIL}">Hire me</a>
			</nav>
			<div class="nav-cta">
				<a class="btn primary" href="mailto:{EMAIL}"><i class="fas fa-paper-plane"></i> Hire me</a>
				<button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span></button>
			</div>
		</div>
	</header>
"""


def social_links() -> str:
    return "\n".join(
        f'\t\t\t\t<a href="{href}" target="_blank" rel="noopener" aria-label="{name}" title="{name}"><i class="{icon}"></i></a>'
        for name, icon, href in SOCIAL
    )


def footer() -> str:
    return f"""	<footer class="site-footer">
		<div class="container">
			<a class="brand" href="index.html"><span class="brand-mark">R</span> Rafah <span>Al Kassar</span></a>
			<p>&copy; <span data-year>2026</span> {SITE_NAME}. Full Stack Developer &amp; AI Solutions.</p>
			<div class="social">
{social_links()}
			</div>
		</div>
	</footer>
	<a class="to-top" href="#top" aria-label="Back to top"><i class="fas fa-arrow-up"></i></a>
	<script src="assets/js/site.js"></script>
</body>
</html>
"""


def tags(items, cls="tag") -> str:
    return '<div class="tags">' + "".join(f'<span class="{cls}">{esc(t)}</span>' for t in items) + "</div>"


def project_card(p, i: int) -> str:
    cls = thumb_class(p)
    src = thumb_src(p)
    badge = CAT_LABEL["ai"] if "ai" in p["cats"] else CAT_LABEL[p["cats"][0]]
    return f"""				<a class="card project-card reveal" href="landing{p['n']}.html" data-cat="{' '.join(p['cats'])}" style="--h:{hue(i)};--d:{(i % 6) * 0.06:.2f}s">
					<div class="project-thumb">
						<img class="blur" src="{src}" alt="" aria-hidden="true" loading="lazy" />
						<img class="logo {cls}" src="{src}" alt="{esc(p['title'])}" loading="lazy" />
						<span class="badge">{badge}</span>
						<span class="open"><i class="fas fa-arrow-right"></i></span>
					</div>
					<div class="project-body">
						<h3>{esc(p['title'])}</h3>
						<p>{esc(p['tagline'])}</p>
						{tags(p['tech'][:3])}
					</div>
				</a>"""


def build_index() -> str:
    marquee = "".join(f"<span>{esc(t)}</span>" for t in MARQUEE)
    services = "\n".join(
        f"""				<div class="card service reveal" style="--d:{i * 0.1:.1f}s">
					<div class="service-icon"><i class="{icon}"></i></div>
					<h3>{esc(title)}</h3>
					<p>{esc(text)}</p>
					{tags(tg)}
				</div>"""
        for i, (icon, title, text, tg) in enumerate(SERVICES)
    )
    skills = "\n".join(
        f"""				<div class="card skill-group reveal" style="--d:{i * 0.08:.2f}s">
					<h3><i class="{icon}"></i> {esc(title)}</h3>
					<div class="chips">{''.join(f'<span class="chip">{esc(c)}</span>' for c in chips)}</div>
				</div>"""
        for i, (icon, title, chips) in enumerate(SKILLS)
    )
    ai_tools = "".join(f'<li><img src="{src}" alt="" loading="lazy" />{esc(name)}</li>' for name, src in AI_TOOLS)
    cards = "\n".join(project_card(p, i) for i, p in enumerate(PROJECTS))
    published = sum(1 for p in PROJECTS if any(k in ("apple", "play", "huawei") for k, _ in p["links"]))

    return head(
        f"{SITE_NAME} | Full Stack Developer & AI Solutions",
        "Portfolio of Rafah Al Kassar: Flutter & native mobile apps, full stack web platforms with React, Angular and Spring Boot, and AI agents & automation.",
    ) + nav() + f"""
	<main id="top">
		<section class="hero" id="home">
			<div class="hero-orb one"></div>
			<div class="hero-orb two"></div>
			<div class="container">
				<div>
					<div class="status-pill reveal in"><i></i> Available for freelance &middot; Remote</div>
					<h1>
						<span class="line">Full Stack Developer</span>
						<span class="line">crafting <span class="gradient-text">mobile, web</span></span>
						<span class="line"><span class="gradient-text">&amp; AI</span> products.</span>
					</h1>
					<p class="hero-lede">I'm Rafah Al Kassar. I design and build complete digital products: Flutter and native mobile apps, scalable web platforms with React, Angular and Spring Boot, and intelligent automation powered by AI agents.</p>
					<div class="hero-actions">
						<a class="btn primary" href="#projects">View projects <i class="fas fa-arrow-right"></i></a>
						<a class="btn ghost" href="#contact"><i class="far fa-envelope"></i> Get in touch</a>
					</div>
					<div class="hero-stats">
						<div><strong>{len(PROJECTS)}+</strong><span>Projects delivered</span></div>
						<div><strong>{published}+</strong><span>Apps on stores</span></div>
						<div><strong>3</strong><span>Platforms: iOS, Android, Web</span></div>
					</div>
				</div>
				<div class="hero-visual" aria-hidden="true">
				<div class="code-card">
					<header><i></i><i></i><i></i><span>developer.ts</span></header>
<pre><span class="k">const</span> <span class="v">developer</span> = {{
  name: <span class="s">"Rafah Al Kassar"</span>,
  role: <span class="s">"Full Stack Developer"</span>,
  mobile: [<span class="s">"Flutter"</span>, <span class="s">"Swift"</span>, <span class="s">"Kotlin"</span>],
  web: [<span class="s">"React"</span>, <span class="s">"Angular"</span>, <span class="s">"Spring Boot"</span>],
  cloud: [<span class="s">"Supabase"</span>, <span class="s">"Firebase"</span>],
  ai: [<span class="s">"n8n"</span>, <span class="s">"LLM Agents"</span>],
  remote: <span class="b">true</span>,
  available: <span class="b">true</span>, <span class="c">// let's talk</span>
}};<span class="cursor"></span></pre>
				</div>
				<span class="floating a"><i class="fas fa-mobile-alt"></i> Mobile</span>
				<span class="floating b"><i class="fas fa-robot"></i> AI Agents</span>
				<span class="floating c"><i class="fas fa-layer-group"></i> Full Stack</span>
				</div>
			</div>
		</section>

		<div class="marquee" aria-hidden="true">
			<div class="marquee-track">{marquee}{marquee}</div>
		</div>

		<section class="section" id="about">
			<div class="container">
				<div class="section-head reveal">
					<span class="eyebrow">What I do</span>
					<h2>Three specialties, <span class="gradient-text">one developer</span></h2>
					<p>From the first screen to the last API call, I own the whole stack. Here's where I spend my time.</p>
				</div>
				<div class="services">
{services}
				</div>
			</div>
		</section>

		<section class="section" id="skills">
			<div class="container">
				<div class="section-head reveal">
					<span class="eyebrow">Technical skills</span>
					<h2>Tools I <span class="gradient-text">build with</span></h2>
					<p>A modern, production-tested stack across mobile, frontend, backend, cloud, and AI.</p>
				</div>
				<div class="skills-layout">
{skills}
				</div>
				<div class="card ai-tools reveal">
					<div class="ai-tools-intro">
						<img src="assets/icons-ai/ai-brain.png" alt="" />
						<div>
							<h3>AI-accelerated workflow</h3>
							<p>I use advanced AI tools daily to build faster, smarter, and more reliable solutions.</p>
						</div>
					</div>
					<ul class="ai-tools-list">{ai_tools}<li><i class="fas fa-plus" style="color:var(--dim)"></i>and more</li></ul>
				</div>
			</div>
		</section>

		<section class="section" id="projects">
			<div class="container">
				<div class="section-head center reveal">
					<span class="eyebrow">Featured work</span>
					<h2>Selected <span class="gradient-text">projects</span></h2>
					<p>A collection of mobile apps, web platforms, and AI-driven products I've designed and developed.</p>
				</div>
				<div class="filters reveal" role="tablist" aria-label="Filter projects">
					<button class="filter-btn active" data-filter="all">All</button>
					<button class="filter-btn" data-filter="mobile"><i class="fas fa-mobile-alt"></i> Mobile</button>
					<button class="filter-btn" data-filter="web"><i class="fas fa-globe"></i> Web</button>
					<button class="filter-btn" data-filter="ai"><i class="fas fa-robot"></i> AI</button>
				</div>
				<div class="projects-grid">
{cards}
				</div>
			</div>
		</section>

		<section class="section" id="contact">
			<div class="container">
				<div class="contact-panel reveal">
					<span class="eyebrow">Let's work together</span>
					<h2>Have a project in mind?</h2>
					<p>I'm open to freelance work and remote collaborations. Tell me about your idea and let's turn it into a product people love.</p>
					<div class="actions">
						<a class="btn primary" href="mailto:{EMAIL}"><i class="far fa-envelope"></i> {EMAIL}</a>
						<a class="btn" href="{SOCIAL[0][2]}" target="_blank" rel="noopener"><i class="fab fa-linkedin-in"></i> Connect on LinkedIn</a>
					</div>
					<div class="contact-grid">
						<div class="contact-item"><span class="ic"><i class="far fa-envelope"></i></span><div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
						<div class="contact-item"><span class="ic"><i class="fas fa-map-marker-alt"></i></span><div><strong>Location</strong><span>{LOCATION}</span></div></div>
						<div class="contact-item"><span class="ic"><i class="fas fa-briefcase"></i></span><div><strong>Availability</strong><span>Freelance projects &middot; Remote only</span></div></div>
					</div>
				</div>
			</div>
		</section>
	</main>
""" + footer()


def build_project(p, idx: int) -> str:
    prev_p = PROJECTS[idx - 1] if idx > 0 else PROJECTS[-1]
    next_p = PROJECTS[idx + 1] if idx < len(PROJECTS) - 1 else PROJECTS[0]
    is_web = p["kind"] == "web"
    cat = CAT_LABEL["ai"] if "ai" in p["cats"] else CAT_LABEL[p["cats"][0]]

    actions = "".join(
        f'<a class="btn{" primary" if j == 0 else ""}" href="{esc(href)}" target="_blank" rel="noopener"><i class="{LINK_META[k][0]}"></i> {LINK_META[k][1]}</a>'
        for j, (k, href) in enumerate(p["links"])
    )
    actions += f'<a class="btn ghost" href="#gallery"><i class="fas fa-images"></i> Screens <i class="fas fa-arrow-down"></i></a>'

    if is_web:
        hero_src = p.get("hero", p["gallery"][0])
        visual = f"""				<div class="browser-frame reveal in">
					<header><i></i><i></i><i></i><span>{esc(p['name'].lower().replace(' ', ''))}.com</span></header>
					<img src="{hero_src}" alt="{esc(p['title'])} preview" />
				</div>"""
    else:
        cls = thumb_class(p)
        visual = f"""				<div class="app-visual" style="--h:{hue(idx)}">
					<img class="blur" src="{p['icon']}" alt="" aria-hidden="true" />
					<img class="logo {cls}" src="{p['icon']}" alt="{esc(p['title'])} icon" />
				</div>"""

    w, h, _ = img_info(p["gallery"][0])
    portrait = h > w
    gallery_cls = "phones" if portrait else "wide"
    style = f' style="--ratio:{w} / {h}"' if portrait else ""
    shots = "\n".join(
        f'\t\t\t\t<a class="shot reveal" href="{src}" style="--d:{(i % 8) * 0.05:.2f}s"><img src="{src}" alt="{esc(p["title"])} screen {i + 1}" loading="lazy" /></a>'
        for i, src in enumerate(p["gallery"])
    )

    highlights = ""
    if p.get("highlights"):
        items = "\n".join(
            f"""				<div class="card highlight reveal" style="--d:{(j % 4) * 0.08:.2f}s">
					<div class="service-icon"><i class="{icon}"></i></div>
					<h3>{esc(title)}</h3>
					<p>{esc(text)}</p>
				</div>"""
            for j, (icon, title, text) in enumerate(p["highlights"])
        )
        highlights = f"""
		<section class="section" id="features">
			<div class="container">
				<div class="section-head reveal">
					<span class="eyebrow">Key features</span>
					<h2>What the app <span class="gradient-text">does</span></h2>
				</div>
				<div class="highlights">
{items}
				</div>
			</div>
		</section>
"""

    return head(f"{p['title']} | {SITE_NAME}", p["desc"][:155]) + nav("index.html") + f"""
	<main id="top">
		<section class="project-hero{' web' if is_web else ''}">
			<div class="hero-orb one"></div>
			<div class="container">
				<div>
					<div class="crumbs"><a href="index.html">Home</a> <i class="fas fa-chevron-right"></i> <a href="index.html#projects">Projects</a> <i class="fas fa-chevron-right"></i> <span>{esc(p['name'])}</span></div>
					<span class="eyebrow">{cat}</span>
					<h1>{esc(p['title'])}</h1>
					<p class="lede">{esc(p['desc'])}</p>
					{tags(p['tech'])}
					<div class="actions">{actions}</div>
				</div>
{visual}
			</div>
		</section>
{highlights}
		<section class="section" id="gallery">
			<div class="container">
				<div class="gallery-head reveal">
					<div>
						<span class="eyebrow">Gallery</span>
						<h2>Project screens</h2>
					</div>
					<p>{len(p['gallery'])} screenshots &middot; click any to enlarge</p>
				</div>
				<div class="gallery {gallery_cls}"{style}>
{shots}
				</div>
			</div>
		</section>

		<section class="section">
			<div class="container">
				<div class="pager reveal">
					<a class="card prev" href="landing{prev_p['n']}.html"><i class="fas fa-arrow-left"></i><span><small>Previous</small><strong>{esc(prev_p['title'])}</strong></span></a>
					<a class="all" href="index.html#projects" aria-label="All projects" title="All projects"><i class="fas fa-th"></i></a>
					<a class="card next" href="landing{next_p['n']}.html"><span><small>Next</small><strong>{esc(next_p['title'])}</strong></span><i class="fas fa-arrow-right"></i></a>
				</div>
			</div>
		</section>

		<section class="section" id="contact">
			<div class="container">
				<div class="contact-panel reveal">
					<span class="eyebrow">Let's work together</span>
					<h2>Want something like this?</h2>
					<p>I'm open to freelance work and remote collaborations. Tell me about your idea and let's build it.</p>
					<div class="actions">
						<a class="btn primary" href="mailto:{EMAIL}"><i class="far fa-envelope"></i> {EMAIL}</a>
						<a class="btn" href="index.html#projects"><i class="fas fa-th"></i> More projects</a>
					</div>
				</div>
			</div>
		</section>
	</main>
""" + footer()


def main():
    (ROOT / "index.html").write_text(build_index(), encoding="utf-8")
    for i, p in enumerate(PROJECTS):
        (ROOT / f"landing{p['n']}.html").write_text(build_project(p, i), encoding="utf-8")
    print(f"Built index.html and {len(PROJECTS)} project pages.")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
