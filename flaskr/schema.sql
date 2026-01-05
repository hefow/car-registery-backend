-- ============================
-- Vehicle Registration System
-- MVP Database Schema
-- PostgreSQL
-- ============================

-- ----------------------------
-- USERS TABLE
-- ----------------------------
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- VEHICLE TYPES TABLE
-- ----------------------------
CREATE TABLE vehicle_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Predefined vehicle types
INSERT INTO vehicle_types (name) VALUES
('Car'),
('Motorcycle'),
('Truck'),
('Bus'),
('Electric Vehicle');

-- ----------------------------
-- VEHICLES TABLE
-- ----------------------------
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    vehicle_type_id INTEGER NOT NULL,

    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    manufacture_year INTEGER NOT NULL,

    vin VARCHAR(100) UNIQUE NOT NULL,
    license_plate VARCHAR(50) UNIQUE NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vehicle_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vehicle_type
        FOREIGN KEY (vehicle_type_id)
        REFERENCES vehicle_types(id)
);

-- ----------------------------
-- VEHICLE DOCUMENTS TABLE
-- ----------------------------
CREATE TABLE vehicle_documents (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vehicle_document
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(id)
        ON DELETE CASCADE
);
