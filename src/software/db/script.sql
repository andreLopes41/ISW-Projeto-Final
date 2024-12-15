DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'secure_password') THEN
        EXECUTE 'CREATE DATABASE secure_password';
    END IF;
END
$$;


CREATE TABLE IF NOT EXISTS records (
        id SERIAL PRIMARY KEY,
        domain VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        create_at DATE
);