from fastapi import APIRouter


router = APIRouter(prefix="")


@router.get("/")
async def greeting() -> dict:
    return {"message": "application is up!"}
