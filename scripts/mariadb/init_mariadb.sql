CREATE DATABASE metastore_iceberg DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'hive_iceberg'@'%'
    IDENTIFIED BY {SECRETE};

GRANT ALL PRIVILEGES
    ON metastore_iceberg.*
    TO 'hive_iceberg'@'%';

FLUSH PRIVILEGES;

CREATE DATABASE metastore_delta DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'hive_delta'@'%'
    IDENTIFIED BY {SECRETE};

GRANT ALL PRIVILEGES
    ON metastore_delta.*
    TO 'hive_delta'@'%';

FLUSH PRIVILEGES;