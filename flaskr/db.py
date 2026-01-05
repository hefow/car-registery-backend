import psycopg2
from flask import g ,current_app
import click


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            current_app.config['DATABASE_URL']
        )
    return g.db

def close_db(e=None):
    db=g.pop('db',None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor();

    with current_app.open_resource('schema.sql') as f:
        sql = f.read().decode('utf-8')
        cursor.execute(sql)
    db.commit()
    cursor.close()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('initialized database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)