from fastapi import FastAPI, HTTPException
import sqlite3 as sq
from uuid import uuid4
import random

app = FastAPI(
    title='Kamstri game'
)


@app.post('/connect/{player_id}')
def connect(player_id: str):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT * FROM players WHERE player_id = "{player_id}"')
        player = cur.fetchone()

        if player is None:
            raise HTTPException(status_code=401, detail='Player is not registered')

        cur.execute(f'UPDATE players SET active = 1 WHERE player_id = "{player_id}"')

        return [{'player_id': player[0],
                 'name': player[1],
                 'country': player[2],
                 'score': player[3],
                 'length': len(player)},
                {'status': 'Successfully connected'}]


@app.post('/register/')
def register(name: str, country: str):
    player_id = str(uuid4())

    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'INSERT INTO players(player_id, name, country) '
                    f'VALUES ("{player_id}", "{name}", "{country}")')
        con.commit()

        return [{'player_id': player_id,
                 'name': name,
                 'country': country},
                {'status': 'Successfully registered'}]


@app.get('/active_players/')
def get_active_players():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT player_id FROM players WHERE active = 1')
        players = cur.fetchall()

        if not players:
            raise HTTPException(status_code=204)

        if len(players) == 2:
            cur.execute(f'UPDATE players SET active = 0, playing = 1 WHERE active = 1')

        return players


@app.get('/play/')
def play():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT player_id FROM players WHERE playing = 1')
        players = cur.fetchall()

        if not players:
            raise HTTPException(status_code=204)

        if len(players) == 2:
            cur.execute(f'UPDATE players SET playing = 0 WHERE playing = 1')

        winner = random.choice(players)
        cur.execute(f'UPDATE players SET score = 1 WHERE player_id = "{winner[0]}"')

        return players
