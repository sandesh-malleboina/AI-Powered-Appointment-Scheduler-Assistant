from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas

SECRET_KEY = "09dsdfsdfsdfwersdfg345666b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token_str:str,credentials_exception):
    try:
        print(token_str)
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None: 
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    return username 

