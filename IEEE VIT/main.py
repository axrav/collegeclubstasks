import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from functions import song_url, tube_dl

app = FastAPI(docs_url=None, redoc_url=None)
import re
reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

class User(BaseModel):
    username: str
    password: str

    class Example:
        example_ = {
            "example": {"username": "Aaravxd", "password": "12345Listen"}
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "8ab59c839dc8bb94334f8f7af4520cf764fcf4f4a66c33698e7f0d85d4d2f7d6"
    )


# config
@AuthJWT.load_config
def config():
    return Settings()


# users
Total = []

# prefilled
admin = {"username": "Aarav", "password": "FFFFFF"}


# Signup Part
@app.post("/signup", status_code=201)
def signup(user: User):
    if not re.match(reg, user.password):
        return {"error": "Your password format is incorrect, your password should contain 8 characters with a number and a special character"}
    new_u = {"username": user.username, "password": user.password}
    Total.append(new_u)

    return new_u


admin_token = ""


@app.post("/login")
def login(user: User, auth: AuthJWT = Depends()):
    for x in Total:
        if (x["username"] == user.username) & (x["password"] == user.password):
            token_ = auth.create_access_token(subject=user.username)
            return {"token": token_}
        raise HTTPException(
            status_code=401, detail="Invalid Username or Password"
        )


@app.post("/adminlogin")
def admin_login(user: User, auth: AuthJWT = Depends()):
    if (admin["username"] == user.username) & (
        admin["password"] == user.password
    ):
        token_ = auth.create_refresh_token(subject=user.username)
        return {"admin token": token_}
    raise HTTPException(status_code=401, detail="You arent' an admin")


@app.get("/song/{Songz_name}")
async def me(Songz_name, auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
    except Exception as _:
        raise HTTPException(status_code=401, detail="Invalid Token")
    x = song_url(Songz_name)
    finalize = tube_dl(x)
    return FileResponse(finalize, media_type="audio/mp3")


@app.get("/clean")
def clean(auth: AuthJWT = Depends()):
    try:
        auth.jwt_refresh_token_required()
    except Exception as _:
        raise HTTPException(
            status_code=401,
            detail="You Cant Clean the cache, you arent an admin!",
        )
    os.system("rm *.mp3")
    return {"status": 200, "details": "cleaned all cache successfully"}
