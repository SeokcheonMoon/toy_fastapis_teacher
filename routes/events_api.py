from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.events import Event

router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

# 새로운 레코드 추가
@router.post("/new")
async def create_event(body: Event) -> dict:
    document = await event_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }

# id를 기준으로 하나의 row를 DB에서 Postman 으로 가져오는 것
@router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# 삭제 (해당 event가 있을 경우 row를 삭제, event가 없으면 Event not found를 출력한다.)
@router.delete("/{id}")                                                                     # function이 delete
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    event = await event_database.delete(id)

    return {
        "message": "Event deleted successfully."
        ,"datas": event
    }