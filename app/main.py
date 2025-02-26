import uvicorn
from fastapi import FastAPI, Request
from routes.users import user_router

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# init fastapi
app = FastAPI(
    title="Simple FastAPI",
    description="Simple REST API with GET, POST, and DELETE operations documentations",
    version="0.2",
    contact={
        "name": "Github Link",
        "url": "https://github.com/ranwiesiel/simple-fastapi",
    },
    docs_url="/api/docs",
)

@app.get("/", tags=["Homepage"])
def homepage(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

app.include_router(user_router, prefix="/api/users", tags=["Users"])


if __name__ == '__main__':
    uvicorn.run(app, port=8000)