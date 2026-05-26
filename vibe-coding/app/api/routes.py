from fastapi import APIRouter, Query

from models.seat import (
    AvailableSeatCount,
    BookSeatRequest,
    MealBookingStats,
    OccupancyStats,
    Seat,
    SeatActionResponse,
)
from services.booking_service import booking_service

router = APIRouter(prefix="/airlines", tags=["Airline Seats"])


@router.get("", response_model=list[str])
def list_airlines() -> list[str]:
    return booking_service.list_airlines()


@router.post("/{airline}/seats/book", response_model=SeatActionResponse)
def book_seat(airline: str, request: BookSeatRequest) -> SeatActionResponse:
    return booking_service.book_seat(airline, request)


@router.post("/{airline}/seats/{seat_no}/cancel", response_model=SeatActionResponse)
def cancel_seat(airline: str, seat_no: str) -> SeatActionResponse:
    return booking_service.cancel_seat(airline, seat_no)


@router.get("/{airline}/available-count", response_model=AvailableSeatCount)
def get_available_seat_count(airline: str) -> AvailableSeatCount:
    return booking_service.get_available_count(airline)


@router.get("/{airline}/seats/status", response_model=list[Seat])
def get_seat_status(airline: str) -> list[Seat]:
    return booking_service.get_seat_status(airline)


@router.get("/{airline}/occupancy", response_model=OccupancyStats)
def get_occupancy_percentage(airline: str) -> OccupancyStats:
    return booking_service.get_occupancy_stats(airline)


@router.get("/meal-statistics", response_model=list[MealBookingStats])
def get_meal_booking_statistics(
    airline: str | None = Query(default=None),
) -> list[MealBookingStats]:
    return booking_service.get_meal_stats(airline)
