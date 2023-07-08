from fastapi import FastAPI, HTTPException
import sqlite3 as sq
from uuid import uuid4


app = FastAPI(
    title='Kamstri game'
)


# with sq.connect('database.db') as con:
#     cur = con.cursor()
#
#     cur.execute("""CREATE TABLE IF NOT EXISTS players (
#         player_id TEXT PRIMARY KEY,
#         player_name TEXT NOT NULL,
#         player_country TEXT NOT NULL,
#         player_score INTEGER NOT NULL DEFAULT 0
#         )""")


@app.post('/connect/{player_id}')
def connect(player_id: str):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT * FROM players WHERE player_id = "{player_id}"')
        player = cur.fetchone()

        if player is None:
            raise HTTPException(status_code=401, detail='Player is unauthorised')

        return {'player_id': player[0],
                'player_name': player[1],
                'player_country': player[2],
                'player_score': player[3]}


@app.post('/register/')
def register(player_name: str, player_country: str):
    player_id = str(uuid4())

    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'INSERT INTO players(player_id, player_name, player_country) '
                    f'VALUES ("{player_id}", "{player_name}", "{player_country}")')
        con.commit()

        return {'player_id': player_id,
                'player_name': player_name,
                'player_country': player_country}
