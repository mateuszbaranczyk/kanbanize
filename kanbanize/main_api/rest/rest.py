from fastapi import APIRouter

from kanbanize.schemas import Group, GroupResponse, GroupUuid

group = APIRouter(prefix="/group", tags=["group"])


@group.post("/create")
async def create_group(group: Group) -> GroupResponse:
    return group


@group.get("/get/{uuid}")
async def get_group(uuid: GroupUuid) -> GroupResponse:
    return uuid


@group.put("/edit/{uuid}")
async def edit_group(uuid: GroupUuid, group: Group) -> GroupResponse:
    return group
