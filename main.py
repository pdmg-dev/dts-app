from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="DTS MVP")

@app.get("/", response_class=HTMLResponse)
def hello():
    return "<h1>Hello DTS MVP!</h1>"
