from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from database import create_database
from routes import user_routes, alert_routes, filter_routes, auth_routes

app = FastAPI()

create_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(filter_routes.router)
app.include_router(alert_routes.router)
