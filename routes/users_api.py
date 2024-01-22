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
async def create_event(body: User) -> dict:
    document = await user_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }

#로그인
@router.get("/{id}", response_model=User)
async def retrieve_event(id: PydanticObjectId) -> User:
    users = await user_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return users

#회원탈퇴
@router.delete("/{id}")                                                                     # function이 delete
async def delete_event(id: PydanticObjectId) -> dict:
    users = await user_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    users = await user_database.delete(id)

    return {
        "message": "Event deleted successfully."
        ,"datas": users
    }