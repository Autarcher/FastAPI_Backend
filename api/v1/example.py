from fastapi import APIRouter, Depends, Query, Cookie, Header
from typing import Annotated
from module.example import User, CommonHeaders, UserBase
from module.cookie import Cookies, CookieBase
from services.example import ExampleService
from datetime import datetime
router = APIRouter(tags=["example"])

@router.get("/example/want", response_model=str, include_in_schema=False)
async def example(want:str, inputId:str = None):
    time:str = Depends(datetime.now)
    ret = f"{inputId} want:{want} time:{time}"
    return ret

@router.post("/example/moreParam", response_model=str)
async def example(user: User = User):
    ret = f"{user.name} age:{user.age} uuid:{user.uuid}"
    return ret

@router.get("/example/cookie", response_model=str)
async def example(name: Annotated[str, Cookie()]):
    time:str = Depends(datetime.now)
    ret = f"name: {name} time:{time}"
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


@router.post("/example/cookie/add", response_model=Cookies)
async def example(cookie: Cookies):
    time:str = Depends(datetime.now)
    instance = CookieBase(session_id=cookie.session_id,
                        fatebook_tracker=cookie.fatebook_tracker,
                        googall_tracker=cookie.googall_tracker)
    ret = await ExampleService.cookie_add(instance)
    return ret

@router.post("/example/user/add", response_model=UserBase)
async def example(user: UserBase):
    time:str = Depends(datetime.now)
    instance = User(name=user.name,
                        password=user.password,
                        age=user.age)
    ret = await ExampleService.user_add(instance)
    return ret


#后台任务
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@router.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


