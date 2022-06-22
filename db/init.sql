DROP SCHEMA voctab CASCADE;
CREATE SCHEMA voctab;
SET search_path TO voctab;

CREATE TABLE voctab.entries
(
    en_content VARCHAR(64),
    ru_content VARCHAR(64),
    success_count INT DEFAULT 0,
    fail_count INT DEFAULT 0,
    PRIMARY KEY(en_content, ru_content)
)
