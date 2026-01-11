from app.core import settings
from datetime import datetime, timedelta, timezone
import jwt, bcrypt

def encode_jwt(payload: dict,
               algorithm: str = settings.auth.algorithm,
               private_key = settings.auth.private_key_path.read_text(),
               expire_in: int = settings.auth.access_token_exp):
    update_payload = payload.copy()
    update_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(seconds=expire_in)
    update_payload['iat'] = datetime.now(tz=timezone.utc)
    encoded_jwt = jwt.encode(payload=update_payload, key=private_key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(token,
               public_key = settings.auth.public_key_path.read_text(),
               algorithm: str = settings.auth.algorithm):
    decoded_jwt = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded_jwt

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)