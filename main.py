# from typing import Union

# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

from app import app

app.static_folder = 'assets'

if __name__ == '__main__':
    app.run()
