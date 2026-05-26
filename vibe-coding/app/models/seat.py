from enum import StrEnum

from pydantic import BaseModel, Field


class SeatClass(StrEnum):
    economy = "economy"
    premium = "premium"


class Seat(BaseModel):
    seatNo: str = Field(..., examples=["1A"])
    isBooked: bool = False
    class_: SeatClass = Field(alias="class")
    mealBooked: bool = False

    model_config = {"populate_by_name": True}


class BookSeatRequest(BaseModel):
    seatNo: str = Field(..., examples=["1A"])
    mealBooked: bool = False


class SeatActionResponse(BaseModel):
    message: str
    airline: str
    seat: Seat


class AvailableSeatCount(BaseModel):
    airline: str
    availableSeats: int
    totalSeats: int


class MealBookingStats(BaseModel):
    airline: str
    mealsBooked: int
    bookedSeats: int
    totalSeats: int


class OccupancyStats(BaseModel):
    airline: str
    bookedSeats: int
    totalSeats: int
    occupancyPercentage: float
