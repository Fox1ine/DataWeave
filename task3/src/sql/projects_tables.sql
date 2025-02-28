CREATE TABLE user_sessions (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    active BOOLEAN NOT NULL,
    page_name TEXT NOT NULL,
    last_activity_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);


CREATE TABLE pages (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_pages_name ON pages(name);


CREATE TABLE events (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_name TEXT NOT NULL,
    page_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_events_user_id_page_id ON events(user_id, page_id);
