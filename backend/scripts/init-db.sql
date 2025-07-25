-- Database initialization script for Cosmere API
-- This script creates the database and user if they don't exist

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE cosmere_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cosmere_db')\gexec

-- Create user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'cosmere_user') THEN
        CREATE USER cosmere_user WITH PASSWORD 'cosmere_password';
    END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE cosmere_db TO cosmere_user;
GRANT ALL ON SCHEMA public TO cosmere_user; 