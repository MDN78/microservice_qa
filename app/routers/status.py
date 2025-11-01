from fastapi import APIRouter
from http import HTTPStatus
from app.models.AppStatus import AppStatus
from app.database.engine import check_availability

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    """Endpoint. Get app status server"""
    check_availability()
    return AppStatus(database=check_availability())
