import datetime
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
from database import database, user_table


SECRET_KEY = "u6hy4ath6in7k6y8abigb83oi3thr3o32win52t69hre544es8t1a2c8k7s"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"])

credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
)

def access_token_expire_minutes() -> int:
    return 30 

def create_access_token(email: str):
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=30
    )
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(email: str):
    query = user_table.select().where(user_table.c.email==email)
    result = await database.fetch_one(query)
    if result:
        return result
    
async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        raise credentials_exception

    if not verify_password(password, user.password):
        raise credentials_exception

    return user 

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub") # sub is subject
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"} # extra info - tells client to try again cuz token expired

        ) from e # gives more info in traceback
    except JWTError as e:
        raise credentials_exception from e
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user 


    
