-- backend/app/db/create_listings.sql
-- Creates pgvector extension, schema, listings table for chatbot

CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS chatbot;

SET search_path = chatbot, public;

CREATE TABLE IF NOT EXISTS chatbot.listings (
    id SERIAL PRIMARY KEY,
    external_id TEXT UNIQUE,         -- ID from WordPress or external source
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC,
    currency VARCHAR(10),
    address TEXT,
    suburb TEXT,
    city TEXT,
    state TEXT,
    postcode VARCHAR(20),
    bedrooms INTEGER,
    bathrooms INTEGER,
    land_area NUMERIC,
    property_type VARCHAR(80),
    images TEXT[],            -- array of image URLs
    source VARCHAR(80),       -- e.g., 'wordpress'
    source_url TEXT,
    available_from DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    embedding vector(1536)    -- set vector dimension to match embedding model
);

-- Optional: index on external_id already created by UNIQUE constraint.
-- Create vector index later after population (example for ivfflat):
-- CREATE INDEX IF NOT EXISTS idx_listings_embedding ON chatbot.listings USING ivfflat (embedding) WITH (lists = 100);