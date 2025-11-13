BEGIN;

-- =========================
-- AGENTS: code + code_str
-- =========================
ALTER TABLE public.agents
  ADD COLUMN IF NOT EXISTS code integer,
  ADD COLUMN IF NOT EXISTS code_str text GENERATED ALWAYS AS (lpad(code::text, 4, '0')) STORED;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                 WHERE c.relkind = 'S' AND c.relname = 'agents_code_seq' AND n.nspname = 'public') THEN
    CREATE SEQUENCE public.agents_code_seq START 1;
  END IF;
END $$;

ALTER TABLE public.agents
  ALTER COLUMN code SET DEFAULT nextval('public.agents_code_seq');

-- Backfill any NULL codes
UPDATE public.agents
SET code = nextval('public.agents_code_seq')
WHERE code IS NULL;

-- Bump sequence to MAX(code)
SELECT setval('public.agents_code_seq', COALESCE((SELECT MAX(code) FROM public.agents), 0));

ALTER TABLE public.agents
  ALTER COLUMN code SET NOT NULL;

ALTER TABLE public.agents
  ADD CONSTRAINT IF NOT EXISTS agents_code_unique UNIQUE (code);

-- =========================
-- USERS: code + code_str
-- =========================
ALTER TABLE public.users
  ADD COLUMN IF NOT EXISTS code integer,
  ADD COLUMN IF NOT EXISTS code_str text GENERATED ALWAYS AS (lpad(code::text, 4, '0')) STORED;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                 WHERE c.relkind = 'S' AND c.relname = 'users_code_seq' AND n.nspname = 'public') THEN
    CREATE SEQUENCE public.users_code_seq START 1;
  END IF;
END $$;

ALTER TABLE public.users
  ALTER COLUMN code SET DEFAULT nextval('public.users_code_seq');

UPDATE public.users
SET code = nextval('public.users_code_seq')
WHERE code IS NULL;

SELECT setval('public.users_code_seq', COALESCE((SELECT MAX(code) FROM public.users), 0));

ALTER TABLE public.users
  ALTER COLUMN code SET NOT NULL;

ALTER TABLE public.users
  ADD CONSTRAINT IF NOT EXISTS users_code_unique UNIQUE (code);

-- =========================
-- PROPERTIES: code + code_str
-- =========================
ALTER TABLE public.properties
  ADD COLUMN IF NOT EXISTS code integer,
  ADD COLUMN IF NOT EXISTS code_str text GENERATED ALWAYS AS (lpad(code::text, 4, '0')) STORED;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                 WHERE c.relkind = 'S' AND c.relname = 'properties_code_seq' AND n.nspname = 'public') THEN
    CREATE SEQUENCE public.properties_code_seq START 1;
  END IF;
END $$;

ALTER TABLE public.properties
  ALTER COLUMN code SET DEFAULT nextval('public.properties_code_seq');

UPDATE public.properties
SET code = nextval('public.properties_code_seq')
WHERE code IS NULL;

SELECT setval('public.properties_code_seq', COALESCE((SELECT MAX(code) FROM public.properties), 0));

ALTER TABLE public.properties
  ALTER COLUMN code SET NOT NULL;

ALTER TABLE public.properties
  ADD CONSTRAINT IF NOT EXISTS properties_code_unique UNIQUE (code);

COMMIT;
