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

#회원탈퇴
@router.delete("/{id}") 
async def delete_users(id: PydanticObjectId) -> dict:
    users = await user_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="users not found"
        )
    users = await user_database.delete(id)

    return {
        "message": "users deleted successfully."
        ,"datas": users
    }