from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User



user_database =  Database(User)

router = APIRouter()


#회원가입
@router.post("/new")
async def create_users(body: User) -> dict:
    document = await user_database.save(body)
    return {
        "message": "users created successfully"
        ,"datas": document
    }
# http://127.0.0.1:8000/users_api/new
# {
#     "name": "홍길동",
#     "email": "test@example.com",
#     "pswd": "password123",
#     "manager": "김매니저",
#     "sellist1": "상품1",
#     "text": "안녕하세요. 반갑습니다."
# }





#로그인
@router.get("/{id}", response_model=User)
async def retrieve_users(id: PydanticObjectId) -> User:
    users = await user_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="users with supplied ID does not exist"
        )
    return users
#http://127.0.0.1:8000/users_api/65ae17c58fd7881c3089ccb1
# {
#     "_id": "65ae17c58fd7881c3089ccb1",
#     "name": "홍길동",
#     "email": "test@example.com",
#     "pswd": "password123",
#     "manager": "김매니저",
#     "sellist1": "상품1",
#     "text": "안녕하세요. 반갑습니다."
# }




#회원탈퇴
@router.delete("/{id}") 
async def delete_users(id: PydanticObjectId) -> dict:
    users = await user_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="users not found"                            #해당 id를 지우면 users not found
        )
    users = await user_database.delete(id)

    return {
        "message": "users deleted successfully."                #해당 id를 지우면 users deleted successfully
        ,"datas": users
    }

# http://127.0.0.1:8000/users_api/65ae17c58fd7881c3089ccb1      # id를 매칭하여 삭제
# {
#     "message": "users deleted successfully.",
#     "datas": true
# }