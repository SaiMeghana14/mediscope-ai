from fastapi import HTTPException, Header
import os

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY", "12345"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
