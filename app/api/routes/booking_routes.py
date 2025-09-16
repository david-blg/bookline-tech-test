from fastapi import APIRouter


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/")
def get_bookings():
    return {"message": "get bookings"}