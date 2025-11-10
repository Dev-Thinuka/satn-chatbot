-- Create dedicated application user
/*DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'satn_user') THEN
      CREATE ROLE satn_user WITH LOGIN PASSWORD 'satn_password';
   END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE satn_chatbot TO satn_user;
