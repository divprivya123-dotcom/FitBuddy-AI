from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)