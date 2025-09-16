from fastapi import APIRouter


router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/")
def get_all_cars():
    return {"message": "get all cars"}