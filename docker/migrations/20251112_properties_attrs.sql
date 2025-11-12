-- 2025-11-12: Add rich listing attributes required by SRS/WordPress fields
CREATE EXTENSION IF NOT EXISTS pg_trgm;

ALTER TABLE properties
  ADD COLUMN IF NOT EXISTS price_from NUMERIC(14,2),
  ADD COLUMN IF NOT EXISTS beds        INTEGER,
  ADD COLUMN IF NOT EXISTS baths       INTEGER,
  ADD COLUMN IF NOT EXISTS car_spaces  INTEGER,
  ADD COLUMN IF NOT EXISTS est_completion TEXT,      -- free text like "Q4 2026"
  ADD COLUMN IF NOT EXISTS video_url       TEXT,
  ADD COLUMN IF NOT EXISTS virtual_tour_url TEXT,
  ADD COLUMN IF NOT EXISTS brochure_url     TEXT,
  ADD COLUMN IF NOT EXISTS floor_plan_url   TEXT,
  ADD COLUMN IF NOT EXISTS price_list_url   TEXT;

-- Keep backward-compat with existing 'price' by defaulting price_from
UPDATE properties SET price_from = COALESCE(price_from, price);

-- Defensive constraints (cheap)
ALTER TABLE properties
  ADD CONSTRAINT chk_beds_nonneg       CHECK (beds        IS NULL OR beds        >= 0),
  ADD CONSTRAINT chk_baths_nonneg      CHECK (baths       IS NULL OR baths       >= 0),
  ADD CONSTRAINT chk_carspaces_nonneg  CHECK (car_spaces  IS NULL OR car_spaces  >= 0),
  ADD CONSTRAINT chk_pricefrom_nonneg  CHECK (price_from  IS NULL OR price_from  >= 0);

