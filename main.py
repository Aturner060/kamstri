from fastapi import FastAPI, HTTPException
import sqlite3 as sq


app = FastAPI(
    title='Kamstri game'
)


@app.post('/connect/{player_id}')
def connect(player_id: int):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'SELECT * FROM players WHERE player_id = {player_id}')
        player = cur.fetchone()

        if player is None:
            raise HTTPException(status_code=404, detail='Player is undefined')

        return {'player_id': player[0],
                'name': player[1],
                'country': player[2],
                'score': player[3]}


@app.post('/register/')
def register(user_name: str, user_country: str):
    pass

