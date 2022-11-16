from psycopg2 import sql

from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT * FROM shows;')


def get_shows_limited(order_by="rating", order="DESC", limit=15, offset=0):
    return data_manager.execute_select(
        sql.SQL("""
            SELECT
                shows.id,
                shows.title,
                shows.year,
                shows.runtime,
                shows.rating,
                string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
                shows.trailer,
                shows.homepage

            FROM shows
                JOIN show_genres ON shows.id = show_genres.show_id
                JOIN genres ON show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY
                CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
                CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
        """
                ).format(order_by=sql.Identifier(order_by)),
        {"order": order, "limit": limit, "offset": offset}
    )


def get_show_by_id(show_id):
    return data_manager.execute_select(
        """
        SELECT * FROM shows
        WHERE id = %(show_id)s;
        """
        , {"show_id": show_id}, fetchall=False)


def get_seasons_by_show_id(show_id):
    return data_manager.execute_select(
        """
        SELECT * FROM seasons
        WHERE show_id = %(show_id)s;
        """
        , {"show_id": show_id})


def get_show_actors(show_id):
    return data_manager.execute_select(
        """
        SELECT actors."name" FROM shows
        INNER JOIN show_characters ON show_characters.show_id = shows.id
        INNER JOIN actors ON actors.id = show_characters.actor_id
        WHERE shows.id = %(show_id)s
        """
        , {"show_id": show_id})


def get_show_genres():
    return data_manager.execute_select(
        """
        SELECT * FROM show_genres;
        """)


def get_genres_names():
    return data_manager.execute_select(
        """
        SELECT * FROM genres;
        """)


def get_shows_ordered_by(order_by, order, limit, offset):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT * FROM shows
        ORDER BY 
            CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
            CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
        LIMIT %(limit)s
        OFFSET %(offset)s;
        """).format(order_by=sql.Identifier(order_by))
        , {"order": order, "limit": limit, "offset": offset})