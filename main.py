from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from api import router
from loguru import logger
import uvicorn


templates = Jinja2Templates(directory="templates")
servers = [
            {"url": "/api/v1", "description": "Server 1"},
            {"url": "/api/v2", "description": "Server 2"},
            {"url": "/api/v3", "description": "Server 3"},
        ]


def create_app():
    app = FastAPI(title="lya_test_App",
                  description="这是lya基于FastAPI的后端模板",
                  summary="一个后端模板",
                  version="0.0.1",
                  root_path="/api/v1",
                  )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    @app.get("/items/{item_id}")
    def read_root(item_id: str, request: Request):
        request_dict = dict(request)
        # logger.info(f"Request:{request_dict}")
        client_host = request.client.host
        return {"client_host": client_host, "item_id": item_id}
    
    @app.get("/items/id/{id}", response_class=HTMLResponse)
    async def read_item(request: Request, id: str):
        return templates.TemplateResponse(
            request=request, name="item.html", context={"id": id}
        )
    @app.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}
    app.include_router(router=router)

              
    return app

app = create_app()
openapi_schema = app.openapi()
openapi_schema["servers"] = servers
app.openapi_schema = openapi_schema
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

