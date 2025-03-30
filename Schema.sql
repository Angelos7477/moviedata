-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    original_title TEXT,
    description TEXT,
    imdb_rating TEXT,
    rt_rating TEXT,
    imdb_rating_is_fallback BOOLEAN DEFAULT FALSE
);

-- Directors table
CREATE TABLE IF NOT EXISTS directors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    imdb_link TEXT
);

-- Many-to-many relationship between movies and directors
CREATE TABLE IF NOT EXISTS movie_directors (
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    director_id INTEGER REFERENCES directors(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, director_id)
);
