
from datetime import datetime, timedelta
from typing import Optional


from fastapi import Request, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose import ExpiredSignatureError, JWTError

from jose.exceptions import ExpiredSignatureError, JWSError, JWTClaimsError

from app.config import SECRET_KEY_ACCESS_TOKEN, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_YEARS, ACCESS_TOKEN_EXPIRE_TYPE
from app.config import REFRESH_TOKEN_EXPIRE_DAYS, REFRESH_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_TYPE,REFRESH_TOKEN_EXPIRE_YEARS,SECRET_KEY_REFRESH_TOKEN


class JWTRepo:

    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_access_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        if expires_delta :
            expire = datetime.utcnow() + expires_delta
        elif ACCESS_TOKEN_EXPIRE_TYPE == "DAYS":
            expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            to_encode.update({"exp": expire})
        elif ACCESS_TOKEN_EXPIRE_TYPE == "YEARS":
            expire = datetime.utcnow() + timedelta(year=ACCESS_TOKEN_EXPIRE_YEARS)
            to_encode.update({"exp": expire})
        elif ACCESS_TOKEN_EXPIRE_TYPE == "MINUTES":
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
        else:
            to_encode.update()
        encode_jwt = jwt.encode(to_encode, SECRET_KEY_ACCESS_TOKEN, algorithm=ALGORITHM)

        return encode_jwt
    
    def generate_refresh_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        if expires_delta :
            expire = datetime.utcnow() + expires_delta
        elif REFRESH_TOKEN_EXPIRE_TYPE == "DAYS":
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            to_encode.update({"exp": expire})
        elif REFRESH_TOKEN_EXPIRE_TYPE == "YEARS":
            expire = datetime.utcnow() + timedelta(year=REFRESH_TOKEN_EXPIRE_YEARS)
            to_encode.update({"exp": expire})
        elif REFRESH_TOKEN_EXPIRE_TYPE == "MINUTES":
            expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
        else:
            to_encode.update()
        encode_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH_TOKEN, algorithm=ALGORITHM)

        return encode_jwt

    def decode_access_token(self):
        try:
            decode_token = jwt.decode(
                self.token, SECRET_KEY_ACCESS_TOKEN, algorithms=[ALGORITHM])
            return decode_token #if decode_token["exp"] >= datetime.time() else None
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail={"status": "Unauthorized", "message": "Expired access token!"})
        except JWTError:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication access token!"})
        
    def decode_refresh_token(self):
        try:
            decode_token = jwt.decode(
                self.token, SECRET_KEY_REFRESH_TOKEN, algorithms=[ALGORITHM])
            return decode_token #if decode_token["exp"] >= datetime.time() else None
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail={"status": "Unauthorized", "message": "Expired refresh token!"})
        except JWTError:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication refresh token!"})

    @staticmethod
    async def extract_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY_ACCESS_TOKEN, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})

class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)


    async def __call__(self, request: Request, access_token: str = Cookie(None)):
        if access_token is None:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization cookies."})
        else:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(access_token)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
                if not self.verify_jwt(credentials.credentials):
                    raise HTTPException(
                        status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
                return credentials.credentials
            else:
                raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})
        


    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            return True if jwt.decode(jwt_token, SECRET_KEY_ACCESS_TOKEN, algorithms=[ALGORITHM]) is not None else  False
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
        

class JWTBearerAdmin(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearerAdmin, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAdmin, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            try:
                if JWTRepo.extract_token(credentials.credentials)["role"] != "admin":
                    raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            except:
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        else:
                raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})
        
    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            return True if jwt.decode(jwt_token, SECRET_KEY_ACCESS_TOKEN, algorithms=[ALGORITHM]) is not None else  False
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})