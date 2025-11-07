-- Create application user and grant privileges
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles WHERE rolname = 'satn_admin'
    ) THEN
        CREATE ROLE satn_user WITH LOGIN PASSWORD 'satn_password';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE satn_chatbot TO satn_user;
