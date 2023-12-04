-- Filters
CREATE TABLE `filters` (
    `id` VARCHAR(255) NOT NULL PRIMARY KEY
);

INSERT INTO filters (id) VALUES
('attacker'),
('chrome'),
('client'),
('device'),
('domain'),
('ip'),
('method'),
('os'),
('referer'),
('request'),
('useragent'),
('browser'),
('webserver'),
('api'),
('user');


-- Users
CREATE TABLE `users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    `last_login` TIMESTAMP NULL,
    `permissions` INT DEFAULT 0
);

INSERT INTO users (username, password, permissions) VALUES
('admin', '$2b$12$ABWxvEq7sAXbx9F0PPFQd.3bZ3Utt1vy6/lSaNVAtBlfzmG/30Zbe', 2),
('john', '$2b$12$VkzX9I3.jniHBHGQY9bcE.8rAO9VnlNfWYJslOl7e4eaQV4x7ZEMe', 1);