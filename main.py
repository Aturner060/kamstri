from fastapi import FastAPI, status, Response

app = FastAPI(
    title='Kamstri game'
)

users = [
    {'id': 1, 'name': 'John', 'country': 'Ukraine', 'score': 0},
    {'id': 2, 'name': 'Bob', 'country': 'Germany', 'score': 1},
    {'id': 3, 'name': 'Miranda', 'country': 'France', 'score': 2},
    {'id': 4, 'name': 'Alex', 'country': 'Italy', 'score': 1},
]


@app.post('/connect/{user_id}')
def connect(user_id: int):
    current_user = [user for user in users if user.get('id') == user_id]
    if current_user:
        return current_user
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post('/register/')
def register(user_name: str, user_country: str):
    pass

