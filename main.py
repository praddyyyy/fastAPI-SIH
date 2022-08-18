from fastapi import FastAPI
from routes.user_routes import user

app = FastAPI()
app.include_router(user)
