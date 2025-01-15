from fastapi import FastAPI
import uvicorn
from api import router
from fastapi.staticfiles import StaticFiles

def create_app():
    app = FastAPI(title="lya_test_App",
                  description="这是lya基于FastAPI的后端模板",
                  summary="一个后端模板",
                  version="0.0.1",)
    app.mount("/static", StaticFiles(directory="static"), name="static")
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

