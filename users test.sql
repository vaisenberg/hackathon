-- CREATE TABLE clients (
--     id SERIAL PRIMARY KEY,
--     first_name VARCHAR(100),
--     last_name VARCHAR(100),
--     phone VARCHAR(15) UNIQUE,
--     country TEXT NOT NULL,
--     unique_number VARCHAR(15) UNIQUE
-- );

-- CREATE TABLE wallet (
--     client_id SERIAL PRIMARY KEY,
--     amount FLOAT NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- );

-- CREATE TABLE USD (
--     client_id SERIAL PRIMARY KEY,
--     amount FLOAT NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- 	);

-- CREATE TABLE EUR (
--     client_id SERIAL PRIMARY KEY,
--     amount FLOAT NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- 	);

-- CREATE TABLE CHF (
--     client_id SERIAL PRIMARY KEY,
--     amount FLOAT NOT NULL,
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- 	);

-- CREATE TABLE big_purchases (
--     id SERIAL PRIMARY KEY,
--     client_id BIGINT NOT NULL, 
--     amount DECIMAL(10, 2) NOT NULL,
--     month DATE NOT NULL, 
--     FOREIGN KEY (client_id) REFERENCES clients(id)
-- );
SELECT * FROM wallet

-- 21014
-- 24177

