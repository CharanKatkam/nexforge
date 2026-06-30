# NexForge Automation — Project Delivery & Workflow Guide

A plain-language reference for explaining the NexForge website: how it works end to
end, what was built **from the client content pack**, and what was **added by us**
on top. Use this to brief the team and management.

---

## 1. Project at a glance

| Item | Detail |
|------|--------|
| What it is | Enterprise marketing website + enquiry-to-lead CRM |
| Stack | Python / Django 6, Django REST Framework, PostgreSQL (Supabase), Bootstrap 5, vanilla JS |
| Surfaces | Public website (`/`), REST API (`/api/v1/`), Admin/CRM (`/admin/`) |
| Pages | 14 public pages, all responsive |
| Content | 14 services, 9 projects, 7 blog posts, 13 FAQs, 4 awards, 7 downloads, testimonials |
| Quality | 55 automated tests passing, 0 browser console errors, security-hardened |

---

## 2. How the whole site works (paragraph summary)

The site is **one Django application talking to one PostgreSQL database**, exposed
through three doors. The **public website** is for anonymous visitors — they read
content (services, projects, blog, etc.) and can submit the **contact form**. They
never log in. When a visitor submits the form, the data is sent to the **REST API**,
which saves it as an **Enquiry (a sales lead)** in the database and emails the sales
inbox. Staff use the **Admin panel** (the back door) to manage every piece of content
and to work the leads (change their status: New → In progress → Converted → Closed).
That is the complete business loop: *visitor browses → submits enquiry → lead is
created → sales follows up.* There is no visitor login or signup; individual visitors
are anonymous, and only the people who fill the form become trackable leads.

### 2.1 Request lifecycle (what happens on every click)
```
Browser ─▶ (prod: Cloudflare ─▶ Nginx) ─▶ Gunicorn ─▶ Django middleware
        ─▶ URL router ─▶ View ─▶ Models (ORM) ─▶ PostgreSQL
        ─▶ HTML page  OR  JSON  ─▶ back to Browser
```

### 2.2 The lead workflow (the only flow that writes data)
```
Visitor fills Contact form
        │  (JavaScript fetch)
        ▼
POST /api/v1/enquiries/        ← rate-limited 5/min, validated
        │
        ├─▶ Save Enquiry row   (status = New)   ← SOURCE OF TRUTH
        └─▶ Email the sales inbox (fail-safe: lead saved even if email fails)
        ▼
Admin ▶ Enquiries ▶ assign + change status ▶ follow up manually
```

### 2.3 Who can do what (roles)
```
Anonymous visitor   → browse, submit enquiry
Staff user (login)  → manage content + leads, scoped by their Role group:
   Administrator     → everything
   Content Manager   → projects, services, blog, content
   Sales Manager     → enquiries (leads)
   Technical Support → enquiries
   HR Manager        → (reserved for Careers — not built yet)
```
Roles are Django **Groups**. They exist in Admin → *Groups*. They only take effect
once you create staff users and assign each to a group. The current single login is a
**superuser**, which sees everything (that is why only "administrator" appears so far).

### 2.4 Content flow (how the site stays up to date)
```
Editor logs into /admin/ ─▶ adds/edits a Project (with images, timeline, etc.)
        ─▶ saved to database ─▶ instantly live on the website + API
```
No code change or redeploy needed to update content.

---

## 3. Implemented FROM the client content pack (the brief)

Everything the master content pack specified that is **built and working**:

| Area | Delivered |
|------|-----------|
| Company info, vision, mission, values | About page + footer |
| Brand (colours #0B2E59 / #F57C00 / #00BCD4, Poppins + Inter) | Applied site-wide |
| Homepage sections | Sticky nav, hero, about, business statistics, services, industries, process, featured projects |
| Hero banner | Exact heading + sub-heading + 4 CTAs |
| Business statistics | All 10 stats (animated counters) |
| Services | All 10 (14 delivered), list + detail pages |
| Projects | Portfolio with filters (status / industry / technology), search, grid-list toggle, lightbox; ongoing + completed; detail pages with value, status, duration, client, overview, challenges, solution, technologies, deliverables, timeline, related projects |
| Blog | Featured + recent posts, 8 categories, list + detail |
| FAQ | General + service questions, accordion |
| Contact | Form (saves lead + emails sales), contact info; map slot wired (needs maps key) |
| Gallery / Awards / Downloads | All three pages |
| Privacy Policy / Terms & Conditions | Full content pages |
| Admin panel | Django Admin: content management, user management, role-based access |
| User roles | All 5 roles as Groups |
| Database tables | Users, Projects, Services, Clients, Blog, Testimonials, Enquiries (+ more) |
| APIs | DRF endpoints: projects, services, blog, enquiries, content, auth |

---

## 4. Added BY US (beyond the brief — value engineering)

Things not explicitly in the content pack that we added for quality, security,
and a premium enterprise feel:

**Security & reliability**
- Content Security Policy (nonce-based) + HSTS, secure cookies, X-Frame-Options, no-sniff
- API rate-limiting (anti-spam on the contact form; brute-force guard on login)
- Server-side file-upload validation (type + size)
- Per-user data access on leads (prevents one staff user seeing another's, IDOR-safe)
- `.env`-based secrets, split dev/prod settings, dependency CVE scan (clean)
- Custom error pages (400 / 403 / 404 / 500)

**Developer & operations**
- Auto-generated API documentation (Swagger UI at `/api/docs/`)
- SEO: `sitemap.xml` + `robots.txt`
- Seed command (one command loads all demo content)
- `run.bat` one-click launcher, README, automated test suite (55 tests)
- Google Analytics hook (turns on by setting one env value)

**Premium UI / motion layer**
- Hero entrance animation, floating hero graphic, animated stat counters
- Scroll-reveal across the whole site (cards, sections, lists)
- Button shine-sweep, card hover glow, animated section underlines
- Technology-partner marquee (auto-scrolling logo strip)
- Custom admin dashboard with live count tiles + recent enquiries
- Branded gradient placeholders for items without photos
- Full accessibility: respects "reduced motion", keyboard focus rings

---

## 5. Not yet built (Phase 2 — honest scope)

These appear in the broader business-workflow vision but are **not in the current build**:

| Module | Status | Note |
|--------|--------|------|
| Careers / Recruitment (jobs, resume upload, HR review) | Not built | HR role exists; needs a `careers` app. Recommended placement: footer + `/careers/` |
| Support / Ticketing | Not built | No ticket system in the brief or build |
| Customer login / portal | Not built | Decision pending with management; visitors are anonymous today |
| Async notifications (Celery + Redis + signals) | Not built | Email is currently sent synchronously, sales-only |
| Customer auto-reply email | Not built | Submitter sees on-screen thanks only |
| JWT authentication | Not built | Uses DRF Token auth instead |
| Sales pipeline (stages, deal value, activity log) | Partial | Only 4 lead statuses today |
| Analytics charts / reports | Partial | Count tiles only; no graphs |
| Real photography | Pending | Gradient placeholders until real images supplied |

---

## 6. Operating notes

- **Run locally:** double-click `run.bat`, open `http://127.0.0.1:8000/`.
- **Admin login:** create one with `python manage.py createsuperuser`.
- **Before production:** rotate the database password, set `DEBUG=False` +
  `config.settings.prod`, configure real SMTP, add Google Maps + Analytics keys,
  run `collectstatic`, supply real images.

---

*Document generated as a delivery reference. Keep in sync with the codebase.*
