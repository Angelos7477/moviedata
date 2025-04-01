# db.py

import psycopg2

def connect_db(config):
    return psycopg2.connect(**config)

def clear_database(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM movie_directors")
        cur.execute("DELETE FROM directors")
        cur.execute("DELETE FROM movies")
    conn.commit()

def insert_movie_with_directors(conn, movie, directors, imdb_rating=None, rt_rating=None, imdb_rating_is_fallback=False):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO movies (id, title, original_title, description, imdb_rating, rt_rating, imdb_rating_is_fallback)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                imdb_rating = EXCLUDED.imdb_rating,
                rt_rating = EXCLUDED.rt_rating,
                imdb_rating_is_fallback = EXCLUDED.imdb_rating_is_fallback
        """, (
            movie['id'], movie['title'], movie['original_title'], movie['overview'],
            imdb_rating, rt_rating, imdb_rating_is_fallback
        ))
        for director in directors:
            cur.execute("""
                INSERT INTO directors (id, name, imdb_link)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (director['id'], director['name'], director['imdb_link']))  
            cur.execute("""
                INSERT INTO movie_directors (movie_id, director_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (movie['id'], director['id']))
    conn.commit()

