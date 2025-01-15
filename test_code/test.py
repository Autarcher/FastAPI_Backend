from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Response, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from loguru import logger
import os

fake_users_db = {
    "lya": {
        "username": "lya",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashed123123",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
}


app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://10.13.3.184:8000",
    "http://localhost:8000",
    "http://10.13.3.184",
    # "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user




SECRET_KEY = "your_secret_key"  # 请使用更安全的密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 设置Token过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


DOWNLOAD_PATH = "C:/Users/lya/PycharmProjects/FastAPIProject/downloadFile/"
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"{DOWNLOAD_PATH}{filename}"
    if not os.path.exists(file_path):
        return {"message": "File not found"}
    with open(file_path, "rb") as file:
        file_content = file.read()
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    return Response(content=file_content, media_type="application/octet-stream", headers=headers)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # if not file.content_type in ["image/jpeg", "image/png", "image/gif"]:
    #     return {"message": "Invalid file type"}
    with open(f"{DOWNLOAD_PATH}{file.filename}", "wb") as buffer:
        while contents := file.file.read(1024 * 1024):
            buffer.write(contents)
    return {"filename": file.filename}

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
