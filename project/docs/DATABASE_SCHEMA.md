# NexForge - Full Database Schema (live dump)

Generated from the live PostgreSQL (Supabase) database.

```
TOTAL TABLES: 36
auth_group, auth_group_permissions, auth_permission, auth_user, auth_user_groups, auth_user_user_permissions, authtoken_token, blog_blogcategory, blog_blogpost, careers_jobapplication, careers_jobopening, contact_enquiry, content_award, content_download, content_faq, content_galleryitem, content_testimonial, core_client, core_industry, core_technology, django_admin_log, django_content_type, django_migrations, django_session, projects_beforeaftergallery, projects_project, projects_project_technologies, projects_projectdeliverable, projects_projectgallery, projects_projectmilestone, projects_projectvideo, services_service, services_service_industries, services_service_technologies, services_servicebenefit, services_servicedeliverable

==================================================================
TABLE: auth_group
------------------------------------------------------------------
  id                         integer                  NOT NULL
  name                       character varying(150)   NOT NULL
  PK: id

==================================================================
TABLE: auth_group_permissions
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  group_id                   integer                  NOT NULL
  permission_id              integer                  NOT NULL
  FK: permission_id -> auth_permission.id
  FK: group_id -> auth_group.id
  PK: id

==================================================================
TABLE: auth_permission
------------------------------------------------------------------
  id                         integer                  NOT NULL
  name                       character varying(255)   NOT NULL
  content_type_id            integer                  NOT NULL
  codename                   character varying(100)   NOT NULL
  FK: content_type_id -> django_content_type.id
  PK: id

==================================================================
TABLE: auth_user
------------------------------------------------------------------
  id                         integer                  NOT NULL
  password                   character varying(128)   NOT NULL
  last_login                 timestamp with time zone NULL
  is_superuser               boolean                  NOT NULL
  username                   character varying(150)   NOT NULL
  first_name                 character varying(150)   NOT NULL
  last_name                  character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  is_staff                   boolean                  NOT NULL
  is_active                  boolean                  NOT NULL
  date_joined                timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: auth_user_groups
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  user_id                    integer                  NOT NULL
  group_id                   integer                  NOT NULL
  FK: group_id -> auth_group.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: auth_user_user_permissions
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  user_id                    integer                  NOT NULL
  permission_id              integer                  NOT NULL
  FK: permission_id -> auth_permission.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: authtoken_token
------------------------------------------------------------------
  key                        character varying(40)    NOT NULL
  created                    timestamp with time zone NOT NULL
  user_id                    integer                  NOT NULL
  FK: user_id -> auth_user.id
  PK: key

==================================================================
TABLE: blog_blogcategory
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  slug                       character varying(50)    NOT NULL
  PK: id

==================================================================
TABLE: blog_blogpost
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  created_at                 timestamp with time zone NOT NULL
  updated_at                 timestamp with time zone NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  summary                    text                     NOT NULL
  body                       text                     NOT NULL
  featured_image             character varying(100)   NULL
  is_featured                boolean                  NOT NULL
  published_at               timestamp with time zone NULL
  author_id                  integer                  NULL
  category_id                bigint                   NOT NULL
  FK: author_id -> auth_user.id
  FK: category_id -> blog_blogcategory.id
  PK: id

==================================================================
TABLE: careers_jobapplication
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  phone                      character varying(20)    NOT NULL
  resume                     character varying(100)   NOT NULL
  cover_letter               text                     NOT NULL
  status                     character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  reviewed_by_id             integer                  NULL
  opening_id                 bigint                   NOT NULL
  FK: opening_id -> careers_jobopening.id
  FK: reviewed_by_id -> auth_user.id
  PK: id

==================================================================
TABLE: careers_jobopening
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  department                 character varying(120)   NOT NULL
  location                   character varying(150)   NOT NULL
  employment_type            character varying(20)    NOT NULL
  experience                 character varying(80)    NOT NULL
  description                text                     NOT NULL
  responsibilities           text                     NOT NULL
  requirements               text                     NOT NULL
  is_open                    boolean                  NOT NULL
  posted_at                  timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: contact_enquiry
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  phone                      character varying(20)    NOT NULL
  message                    text                     NOT NULL
  status                     character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  assigned_to_id             integer                  NULL
  FK: assigned_to_id -> auth_user.id
  PK: id

==================================================================
TABLE: content_award
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  year                       integer                  NOT NULL
  description                text                     NOT NULL
  image                      character varying(100)   NULL
  PK: id

==================================================================
TABLE: content_download
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  file                       character varying(100)   NOT NULL
  type                       character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: content_faq
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  question                   character varying(255)   NOT NULL
  answer                     text                     NOT NULL
  category                   character varying(20)    NOT NULL
  order                      integer                  NOT NULL
  is_active                  boolean                  NOT NULL
  PK: id

==================================================================
TABLE: content_galleryitem
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  category                   character varying(80)    NOT NULL
  image                      character varying(100)   NOT NULL
  order                      integer                  NOT NULL
  PK: id

==================================================================
TABLE: content_testimonial
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  author_name                character varying(120)   NOT NULL
  designation                character varying(120)   NOT NULL
  quote                      text                     NOT NULL
  is_active                  boolean                  NOT NULL
  client_id                  bigint                   NULL
  FK: client_id -> core_client.id
  PK: id

==================================================================
TABLE: core_client
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(180)   NOT NULL
  slug                       character varying(50)    NOT NULL
  logo                       character varying(100)   NULL
  website                    character varying(200)   NOT NULL
  industry_id                bigint                   NULL
  FK: industry_id -> core_industry.id
  PK: id

==================================================================
TABLE: core_industry
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  slug                       character varying(50)    NOT NULL
  icon                       character varying(100)   NULL
  PK: id

==================================================================
TABLE: core_technology
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  category                   character varying(80)    NOT NULL
  icon                       character varying(100)   NULL
  PK: id

==================================================================
TABLE: django_admin_log
------------------------------------------------------------------
  id                         integer                  NOT NULL
  action_time                timestamp with time zone NOT NULL
  object_id                  text                     NULL
  object_repr                character varying(200)   NOT NULL
  action_flag                smallint                 NOT NULL
  change_message             text                     NOT NULL
  content_type_id            integer                  NULL
  user_id                    integer                  NOT NULL
  FK: content_type_id -> django_content_type.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: django_content_type
------------------------------------------------------------------
  id                         integer                  NOT NULL
  app_label                  character varying(100)   NOT NULL
  model                      character varying(100)   NOT NULL
  PK: id

==================================================================
TABLE: django_migrations
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  app                        character varying(255)   NOT NULL
  name                       character varying(255)   NOT NULL
  applied                    timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: django_session
------------------------------------------------------------------
  session_key                character varying(40)    NOT NULL
  session_data               text                     NOT NULL
  expire_date                timestamp with time zone NOT NULL
  PK: session_key

==================================================================
TABLE: projects_beforeaftergallery
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  before_image               character varying(100)   NOT NULL
  after_image                character varying(100)   NOT NULL
  caption                    character varying(180)   NOT NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_project
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  created_at                 timestamp with time zone NOT NULL
  updated_at                 timestamp with time zone NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  status                     character varying(20)    NOT NULL
  location                   character varying(150)   NOT NULL
  project_value              character varying(80)    NOT NULL
  duration                   character varying(60)    NOT NULL
  team_size                  integer                  NULL
  overview                   text                     NOT NULL
  challenges                 text                     NOT NULL
  solution                   text                     NOT NULL
  thumbnail                  character varying(100)   NULL
  is_featured                boolean                  NOT NULL
  order                      integer                  NOT NULL
  client_id                  bigint                   NULL
  industry_id                bigint                   NOT NULL
  FK: client_id -> core_client.id
  FK: industry_id -> core_industry.id
  PK: id

==================================================================
TABLE: projects_project_technologies
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  project_id                 bigint                   NOT NULL
  technology_id              bigint                   NOT NULL
  FK: project_id -> projects_project.id
  FK: technology_id -> core_technology.id
  PK: id

==================================================================
TABLE: projects_projectdeliverable
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectgallery
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  image                      character varying(100)   NOT NULL
  caption                    character varying(180)   NOT NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectmilestone
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  description                text                     NOT NULL
  date                       date                     NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectvideo
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  video_url                  character varying(200)   NOT NULL
  title                      character varying(150)   NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: services_service
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  short_description          text                     NOT NULL
  detailed_description       text                     NOT NULL
  icon                       character varying(100)   NULL
  is_active                  boolean                  NOT NULL
  order                      integer                  NOT NULL
  PK: id

==================================================================
TABLE: services_service_industries
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  service_id                 bigint                   NOT NULL
  industry_id                bigint                   NOT NULL
  FK: industry_id -> core_industry.id
  FK: service_id -> services_service.id
  PK: id

==================================================================
TABLE: services_service_technologies
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  service_id                 bigint                   NOT NULL
  technology_id              bigint                   NOT NULL
  FK: service_id -> services_service.id
  FK: technology_id -> core_technology.id
  PK: id

==================================================================
TABLE: services_servicebenefit
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  text                       character varying(200)   NOT NULL
  service_id                 bigint                   NOT NULL
  FK: service_id -> services_service.id
  PK: id

==================================================================
TABLE: services_servicedeliverable
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  service_id                 bigint                   NOT NULL
  FK: service_id -> services_service.id
  PK: id
```
