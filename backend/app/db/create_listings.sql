-- Enable pgvector for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schema (owned by admin)
CREATE SCHEMA IF NOT EXISTS chatbot AUTHORIZATION satn_admin;

-- Ensure satn_user uses chatbot schema by default
ALTER ROLE satn_user SET search_path TO chatbot, public;

-- Set active schema
SET search_path TO chatbot, public;

-- =====================================================
-- TABLE: listings
-- =====================================================
CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    price NUMERIC(12,2),
    bedrooms INT,
    bathrooms INT,
    area_sqft NUMERIC(10,2),
    image_url TEXT,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TRIGGER: auto-update updated_at column
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_timestamp ON listings;
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON listings
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- OWNERSHIP & PERMISSIONS
-- =====================================================
ALTER SCHEMA chatbot OWNER TO satn_admin;
ALTER TABLE chatbot.listings OWNER TO satn_admin;

GRANT USAGE ON SCHEMA chatbot TO satn_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA chatbot TO satn_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA chatbot
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO satn_user;
