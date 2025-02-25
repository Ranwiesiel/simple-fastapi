import uvicorn
from fastapi import FastAPI
from routes.users import user_router
    

# init fastapi
app = FastAPI(
    title="Simple FastAPI",
    description="Simple REST API with GET, POST, and DELETE operations documentations",
    version="0.2",
    docs_url="/api/docs",
)

app.include_router(user_router, prefix="/api/users", tags=["users"])


if __name__ == '__main__':
    uvicorn.run(app, port=8000)