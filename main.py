from fastapi import FastAPI
import uvicorn
from api import router

def create_app():
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}
    app.include_router(router=router)
    return app

app = create_app()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

