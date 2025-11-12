CREATE INDEX IF NOT EXISTS ix_properties_title               ON properties (title);
CREATE INDEX IF NOT EXISTS ix_properties_location            ON properties (location);
CREATE INDEX IF NOT EXISTS ix_properties_price               ON properties (price);
CREATE INDEX IF NOT EXISTS ix_properties_agent_id            ON properties (agent_id);
CREATE INDEX IF NOT EXISTS ix_properties_features_jsonb_gin  ON properties USING GIN (features);
CREATE INDEX IF NOT EXISTS ix_agents_name ON agents (name);
CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);
