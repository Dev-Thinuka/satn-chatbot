-- B-tree for numeric/range filters
CREATE INDEX IF NOT EXISTS ix_properties_price_from  ON properties (price_from);
CREATE INDEX IF NOT EXISTS ix_properties_beds        ON properties (beds);
CREATE INDEX IF NOT EXISTS ix_properties_baths       ON properties (baths);
CREATE INDEX IF NOT EXISTS ix_properties_car_spaces  ON properties (car_spaces);

-- Fast text search on title/location
CREATE INDEX IF NOT EXISTS ix_properties_title_trgm
  ON properties USING gin (title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_properties_location_trgm
  ON properties USING gin (location gin_trgm_ops);

-- JSONB access (features/type, amenities)
CREATE INDEX IF NOT EXISTS ix_properties_features_gin
  ON properties USING gin (features);
