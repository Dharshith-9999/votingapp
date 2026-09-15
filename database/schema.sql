CREATE TABLE IF NOT EXISTS votes (
    id BIGSERIAL PRIMARY KEY,
    voter_id UUID NOT NULL UNIQUE,
    option VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_vote_option
        CHECK (option IN ('cats', 'dogs'))
);

CREATE INDEX IF NOT EXISTS idx_votes_option
    ON votes(option);

CREATE INDEX IF NOT EXISTS idx_votes_created_at
    ON votes(created_at);