import psycopg2
from ury_wrapped.config import cfg


_conn: "psycopg2.connection" = None  # type: ignore


def get_db_connection():
    return psycopg2.connect(
        host=cfg.db_host,
        port=cfg.db_port,
        user=cfg.db_user,
        password=cfg.db_password.get_secret_value(),
        database="membership",
    )


def query_one(q: str, *args):
    global _conn
    if _conn is None:
        _conn = get_db_connection()

    with _conn.cursor() as cur:
        cur.execute(q, args)
        return cur.fetchone()
