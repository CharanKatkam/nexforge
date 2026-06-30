# NexForge Automation — Complete Delivery Guidebook & User Manual

Everything needed to understand, run, operate, extend, and deploy the NexForge
Automation platform. Written for the project team, administrators (HR / Sales /
Content), and developers.

---

# 1. What this platform is

NexForge Automation is an **enterprise marketing website + lightweight CRM and
recruitment system** for an industrial-automation company. One Django application
serves three surfaces from one PostgreSQL database:

| Surface | URL | Audience |
|---------|-----|----------|
| Public website | `/` | anonymous visitors |
| REST API | `/api/v1/` | the site's JavaScript + integrations |
| Admin / CRM | `/admin/` | staff (Administrator, Content, Sales, HR, Support) |

Stack: **Python / Django 6, Django REST Framework, PostgreSQL (Supabase),
Bootstrap 5, vanilla JavaScript**, WhiteNoise, Gunicorn. No SPA framework.

---

# 2. Getting started

## 2.1 Run it locally (Windows)
```
cd project
.venv\Scripts\python.exe manage.py migrate        # set up DB
.venv\Scripts\python.exe manage.py seed            # demo content (optional)
.venv\Scripts\python.exe manage.py seed_careers    # demo job openings (optional)
.venv\Scripts\python.exe manage.py createsuperuser # your admin login
.venv\Scripts\python.exe manage.py runserver
```
Or just double-click **`run.bat`**. Then open **http://127.0.0.1:8000/**.

## 2.2 Configuration (.env)
Copy `.env.example` to `.env` and fill in. Key variables:

| Variable | Meaning |
|----------|---------|
| `SECRET_KEY` | Django crypto key (long random string) |
| `DEBUG` | `True` dev / `False` prod |
| `DATABASE_URL` | PostgreSQL connection string |
| `EMAIL_HOST*` | SMTP for sending mail (prod) |
| `SALES_INBOX` / `HR_INBOX` | where enquiry / application notifications go |
| `GOOGLE_MAPS_API_KEY` | enables the contact-page map |
| `GOOGLE_ANALYTICS_ID` | enables visitor analytics (e.g. `G-XXXX`) |
| `HERO_VIDEO_URL` | optional hero background video |
| `CORS_ALLOWED_ORIGINS` | prod allow-list |
| `CSP_REPORT_ONLY` | `False` to enforce Content-Security-Policy in prod |

**Never commit `.env`.** It is git-ignored.

---

# 3. Architecture

```
Browser ─▶ (prod: Cloudflare ─▶ Nginx) ─▶ Gunicorn ─▶ Django middleware chain
        ─▶ URL router ─▶ View ─▶ Models (ORM) ─▶ PostgreSQL (Supabase)
        ─▶ HTML page  OR  JSON  ─▶ back to Browser
```

Apps (one per business domain):

| App | Responsibility |
|-----|----------------|
| `core` | shared lookups, all template pages, sitemaps, admin dashboard, seed |
| `projects` | portfolio + gallery/videos/deliverables/milestones |
| `services` | service catalogue |
| `blog` | posts + categories |
| `contact` | enquiry (CRM) + email |
| `content` | FAQ, gallery, awards, downloads, testimonials |
| `careers` | job openings + applications (HR) |
| `accounts` | role groups + token login |

---

# 4. Public website — page by page

Navigation (top bar): Home · Projects · Services · About · Gallery · FAQ · Blog ·
Downloads · **Get a Quote**. Footer adds Careers, Privacy, Terms, resources.

| Page | URL | What it does |
|------|-----|--------------|
| Home | `/` | Animated hero (AI-network + optional video), business stats, services, industries, featured projects, technology marquee, testimonials |
| Projects | `/projects/` | Filter (status / industry / technology) + search + grid/list, cards load from the API |
| Project detail | `/projects/<slug>/` | Full case study: value, status, duration, client, overview, challenges, solution, technologies, timeline, related projects |
| Services | `/services/` + `/services/<slug>/` | Catalogue + detail (benefits, deliverables, technologies) |
| Blog | `/blog/` + `/blog/<slug>/` | Articles, categories |
| FAQ | `/faq/` | Accordion |
| Gallery / Awards / Downloads | `/gallery/` `/awards/` `/downloads/` | Media + files |
| Careers | `/careers/` + `/careers/<slug>/` | Open roles + online application with resume upload |
| Contact | `/contact/` | Enquiry form (+ map when key set) |
| Privacy / Terms | `/privacy/` `/terms/` | Legal |
| Admin | `/admin/` | Staff CRM/CMS |
| API docs | `/api/docs/` | Swagger UI |

---

# 5. The two live workflows (what happens on submit)

## 5.1 Contact → Lead
```
Visitor fills /contact/ ─▶ POST /api/v1/enquiries/ (throttled 5/min, validated)
  ─▶ Enquiry saved (status = New)            ← source of truth
  ─▶ Email to SALES_INBOX (sales notified)
  ─▶ Auto-reply email to the visitor
  ─▶ 201 → on-screen "thanks"
Staff ▶ Admin ▶ Enquiries ▶ assign + move status (New → In progress → Converted → Closed)
```

## 5.2 Careers → Application
```
Candidate opens /careers/<job>/ ─▶ fills form + uploads resume
  ─▶ POST /api/v1/applications/ (throttled, resume type+size validated)
  ─▶ JobApplication saved (status = New)
  ─▶ Email to HR_INBOX + auto-reply to candidate
  ─▶ 201 → "submitted"
HR ▶ Admin ▶ Job applications ▶ move status (New → Shortlisted → Interview → Hired/Rejected)
```

Both flows are **anonymous** (no login to apply or enquire). The DB record is the
source of truth, so a mail failure never loses a lead or application.

---

# 6. Admin / CRM guide (for staff)

Log in at `/admin/`. The dashboard shows live counts (projects, enquiries, blog,
etc.) and recent enquiries.

**Common tasks**
- **Add a project:** Projects → Add. Fill fields; add gallery images, videos,
  deliverables and timeline inline; save → live instantly.
- **Work a lead:** Contact → Enquiries → open → set status / assign.
- **Review an applicant:** Careers → Job applications → open → download resume →
  set status.
- **Publish a job:** Careers → Job openings → Add (tick "is open").
- **Edit content:** Services, Blog, FAQ, Gallery, Awards, Downloads, Testimonials.

---

# 7. Roles & permissions

Roles are Django **Groups** (Admin → Authentication → Groups). Assign each staff
user to a group (Users → Add → tick "Staff status" → pick group).

| Role | Can manage |
|------|-----------|
| Administrator | everything |
| Content Manager | projects, services, blog, content |
| Sales Manager | enquiries (leads) |
| Technical Support | enquiries |
| HR Manager | job openings + applications |

A **superuser** bypasses groups and sees all. There is **no public signup** —
visitors never have accounts.

---

# 8. Email & notifications

- Library: Django `send_mail` (synchronous). Dev backend prints to console; prod
  uses SMTP from `.env`.
- Triggers: **new enquiry** (→ sales + auto-reply to sender) and **new
  application** (→ HR + auto-reply to candidate). All fail-safe (`fail_silently`).
- No queue/Celery, no SMS/push. Adding a background queue is a future option.

---

# 9. REST API reference (`/api/v1/`)

Read-only public viewsets (GET): `projects`, `services`, `blog`, `faqs`,
`gallery`, `awards`, `downloads`, `testimonials`, `jobs`.

Write + staff-gated:
- `POST /enquiries/` — public create; staff list/update.
- `POST /applications/` — public create (multipart, resume); staff list/update.
- `POST /auth/login/` — token login (staff), throttled.

Filtering: `?status=`, `?industry__slug=`, `?category=`, `?search=`, etc.
Pagination: 9 per page. Full interactive docs at **`/api/docs/`**, schema at
`/api/schema/`.

---

# 10. Database schema (live, 36 tables)

The database is PostgreSQL on Supabase. Tables group into framework tables
(`auth_*`, `django_*`, `authtoken_token`) and application tables below. File
fields (`resume`, `image`, `file`, `thumbnail`) store the **path**; the actual
files live in `MEDIA`.

**Application (domain) tables**

| Table | Key columns | Links |
|-------|-------------|-------|
| `core_industry` | name, slug, icon | — |
| `core_technology` | name, category, icon | — |
| `core_client` | name, slug, logo, website | → industry |
| `projects_project` | title, slug, status, value, duration, team_size, overview, challenges, solution, is_featured | → industry, → client |
| `projects_project_technologies` | (join) | project ↔ technology |
| `projects_projectgallery` | image, caption, order | → project |
| `projects_projectvideo` | video_url, title | → project |
| `projects_projectdeliverable` | title | → project |
| `projects_projectmilestone` | title, description, date, order | → project |
| `projects_beforeaftergallery` | before_image, after_image, caption | → project |
| `services_service` | title, slug, short/detailed description, is_active | — |
| `services_servicebenefit` | text | → service |
| `services_servicedeliverable` | title | → service |
| `services_service_technologies` / `_industries` | (joins) | service ↔ tech / industry |
| `blog_blogcategory` | name, slug | — |
| `blog_blogpost` | title, slug, summary, body, published_at | → category, → author (user) |
| `content_faq` | question, answer, category, order, is_active | — |
| `content_galleryitem` | title, category, image, order | — |
| `content_award` | title, year, description, image | — |
| `content_download` | title, file, type | — |
| `content_testimonial` | author_name, designation, quote, is_active | → client |
| `contact_enquiry` | name, email, phone, message, status | → assigned_to (user) |
| `careers_jobopening` | title, slug, department, location, employment_type, experience, description | — |
| `careers_jobapplication` | name, email, phone, resume, cover_letter, status | → opening, → reviewed_by (user) |

**Framework tables:** `auth_user`, `auth_group`, `auth_permission`,
`auth_group_permissions`, `auth_user_groups`, `auth_user_user_permissions`,
`authtoken_token`, `django_admin_log`, `django_content_type`,
`django_migrations`, `django_session`.

The full column-level dump (types, PKs, FKs) is in `docs/DATABASE_SCHEMA.md`.

### Useful SQL (read-only)
```sql
-- New leads this month
SELECT name, email, created_at FROM contact_enquiry
WHERE created_at >= date_trunc('month', now()) ORDER BY created_at DESC;

-- Applications per job
SELECT o.title, count(a.id) FROM careers_jobopening o
LEFT JOIN careers_jobapplication a ON a.opening_id = o.id GROUP BY o.title;

-- Featured projects
SELECT title, status FROM projects_project WHERE is_featured = true;
```

---

# 11. Security, SEO, performance (built-in)

- **Security:** CSP (nonce-based), HSTS, secure cookies, X-Frame-Options,
  rate-limiting, server-side file validation, per-user lead access, secrets in
  env, custom error pages. `DEBUG=False` in prod.
- **SEO:** `sitemap.xml`, `robots.txt`, per-page titles/descriptions, slug URLs.
- **Performance:** image lazy-load, pagination, `select_related`/`prefetch_related`
  (no N+1), WhiteNoise compressed static, reduced-motion support.

---

# 12. Deployment

```
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 127.0.0.1:8000   # behind systemd
```
- Set `DJANGO_SETTINGS_MODULE=config.settings.prod` and all env vars.
- Nginx reverse-proxies to Gunicorn; serves `/static/` and `/media/`.
- SSL via Certbot. Set `CSP_REPORT_ONLY=False` once verified.
- Launch checklist: rotate DB password, real SMTP, maps + analytics keys, real
  images, `createsuperuser`, run `seed`/`seed_careers` if desired.

---

# 13. Maintenance & troubleshooting

| Symptom | Fix |
|---------|-----|
| UI looks old after deploy | Bump the `?v=` asset version / hard-refresh; prod uses hashed static |
| Page won't load (500) | Check server logs; in dev the traceback shows on screen |
| Emails not arriving | Dev prints to console; in prod check `EMAIL_HOST*`; leads are still saved |
| Tests can't create DB on Supabase | Run with a local engine: `DATABASE_URL=sqlite://:memory: ... test` |
| "port already in use" | A server is already running; open the URL or use another port |

Run tests: `python manage.py test` (62 tests).

---

# 14. Not yet built (future scope)

Customer login / portal, support/ticketing, async notification queue (Celery +
Redis), JWT auth, richer sales pipeline, analytics charts. Careers and customer
auto-reply emails are **now built**. The customer-portal decision is pending
business approval and does not block anything above.

---

*End of manual. Keep in sync with the codebase.*
