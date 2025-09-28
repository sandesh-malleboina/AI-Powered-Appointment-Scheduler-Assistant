from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash():
    def do_hash(password:str):
        return pwd_context.hash(password)
    
    def verify(hashed_pwd,plain_password):
        return pwd_context.verify(plain_password,hashed_pwd)