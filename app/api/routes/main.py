from fastapi import APIRouter


router = APIRouter(prefix="")


@router.get("/")
async def greeting() -> dict:
    """Endpoint just for fun to check service health status!"""
    return {"message": "application is up!"}
