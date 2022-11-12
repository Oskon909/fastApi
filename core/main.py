import time
from typing import Union


from fastapi import FastAPI,Form,File,UploadFile,Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


# https://fastapi.tiangolo.com/tutorial/middleware/
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print('olololo')
    return response

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    print('Hayot')
    """
    Create a new user:
    - **param user**: User
    - **return**: call to UserOut
    """
    return user

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


@app.post("/files/")
async def create_file(file: bytes = File()):
    with open(file,'rb') as f:
        file_content = f.read()
        print(file_content)
    return {"file": file_content}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    return {"filename": file.filename}


