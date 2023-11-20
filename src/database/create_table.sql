CREATE TABLE IF NOT EXISTS users (
        telegram_id bigint NOT NULL,
        user_name VARCHAR,
        iq bigint NOT NULL,
        chat_id bigint NOT NULL
);