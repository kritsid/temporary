from flask import g
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    conn = psycopg2.connect('postgres://anrmmfmwifrybj:67cd7e91bea09eebf8e238a9206863425d759fc36e98150187b2a16902bbc123@ec2-3-215-40-176.compute-1.amazonaws.com:5432/dnd2jr2gjkgo', cursor_factory=DictCursor)
    conn.autocommit = True
    sql = conn.cursor()
    return conn, sql

def get_db():
    db = connect_db()

    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]

    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]

    return g.postgres_db_cur

def init_db():
    db = connect_db()

    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()

    db[0].close()

def init_admin():
    db = connect_db()

    db[1].execute('update users set admin = True where name = %s', ('admin', ))

    db[1].close()
    db[0].close()
