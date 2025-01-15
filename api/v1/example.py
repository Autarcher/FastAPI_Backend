from fastapi import APIRouter, Depends, Query, Cookie, Header
from typing import Annotated
from module.example import User, CommonHeaders
from module.cookie import Cookies, CookieBase
from services.example import ExampleService
from datetime import datetime
router = APIRouter(tags=["example"])


@router.post("/example/moreParam", response_model=str)
async def example(user: User = User):
    ret = f"{user.name} age:{user.age} uuid:{user.uuid}"
    return ret


@router.post("/example/cookie/add", response_model=Cookies)
async def example(cookie: Cookies):
    time:str = Depends(datetime.now)
    instance = CookieBase(session_id=cookie.session_id,
                        fatebook_tracker=cookie.fatebook_tracker,
                        googall_tracker=cookie.googall_tracker)
    ret = await ExampleService.cookie_add(instance)
    return ret

@router.get("/example/want", response_model=str)
async def example(want:str, inputId:str = None):
    time:str = Depends(datetime.now)
    ret = f"{inputId} want:{want} time:{time}"
    return ret

@router.get("/example/header", response_model=str)
async def example(
    want: str,
    host: Annotated[str, Header()],
    save_data: Annotated[bool, Header()],
    if_modified_since: Annotated[str | None, Header()] = None,
    traceparent: Annotated[str | None, Header()] = None
):
    ret = f"host: {host}, save_data: {save_data}, if_modified_since: {if_modified_since}, traceparent: {traceparent}, want: {want}"
    return ret