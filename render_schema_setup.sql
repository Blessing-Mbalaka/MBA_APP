-- ========================================
-- SAFE SCHEMA CREATION FOR DJANGO + MBA PHASE 2
-- ========================================
-- 1. Core Django tables
CREATE TABLE IF NOT EXISTS public.django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_uniq UNIQUE (app_label, model)
);

CREATE TABLE IF NOT EXISTS public.auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES public.django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    CONSTRAINT auth_permission_content_type_codename_uniq UNIQUE (content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS public.auth_group_permissions (
    id BIGSERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES public.auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES public.auth_permission(id),
    CONSTRAINT auth_group_permissions_group_permission_uniq UNIQUE (group_id, permission_id)
);

CREATE TABLE IF NOT EXISTS public.django_migrations (
    id BIGSERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS public.django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMPTZ NOT NULL
);

-- 2. Application user table
CREATE TABLE IF NOT EXISTS public.mbamain_auser (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMPTZ NOT NULL,
    user_type INTEGER NOT NULL,
    role_type INTEGER,
    has_profile BOOLEAN NOT NULL,
    has_signature BOOLEAN NOT NULL,
    has_cv BOOLEAN NOT NULL
);

-- 3. User–permission relationships
CREATE TABLE IF NOT EXISTS public.mbamain_auser_groups (
    id BIGSERIAL PRIMARY KEY,
    auser_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id),
    group_id INTEGER NOT NULL REFERENCES public.auth_group(id),
    CONSTRAINT auser_group_unique UNIQUE (auser_id, group_id)
);

CREATE TABLE IF NOT EXISTS public.mbamain_auser_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    auser_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id),
    permission_id INTEGER NOT NULL REFERENCES public.auth_permission(id),
    CONSTRAINT auser_perm_unique UNIQUE (auser_id, permission_id)
);

-- 4. Application domain tables
-- (keep relationships but no duplicate creation)
CREATE TABLE IF NOT EXISTS public.mbamain_project (
    id BIGSERIAL PRIMARY KEY,
    project_title VARCHAR(200) NOT NULL,
    project_description TEXT NOT NULL,
    project_start_date DATE NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    ehical_clearance_number INTEGER,
    qualification VARCHAR(100),
    project_status INTEGER NOT NULL,
    primary_supervisor INTEGER,
    discipline TEXT NOT NULL,
    assessor_1 INTEGER,
    assessor_2 INTEGER,
    assessor_3 INTEGER,
    student_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id)
);

-- Minimal subset for FK integrity
CREATE TABLE IF NOT EXISTS public.mbamain_signature (
    id BIGSERIAL PRIMARY KEY,
    img_path VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    user_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id) UNIQUE
);

CREATE TABLE IF NOT EXISTS public.mbamain_examminerprofile (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    surname TEXT,
    email VARCHAR(254),
    created_at TIMESTAMPTZ NOT NULL,
    user_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id) UNIQUE
);

-- 5. Django log (safe foreign key)
CREATE TABLE IF NOT EXISTS public.django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMPTZ NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES public.django_content_type(id),
    user_id BIGINT NOT NULL REFERENCES public.mbamain_auser(id)
);

-- ✅ Add any additional mbamain_* tables as needed, following this pattern
