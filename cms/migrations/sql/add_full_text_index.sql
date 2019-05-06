CREATE INDEX site_post_search ON cms_post
USING GIN (to_tsvector('english', "Title" || ' ' || "Subtitle" || ' ' || "BodyMarkdown"))