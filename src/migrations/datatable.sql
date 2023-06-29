CREATE TABLE data (
  id SERIAL PRIMARY KEY,
  updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  content jsonb
  type text
);

CREATE INDEX data_content_index ON data USING gin (content);