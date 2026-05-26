from threading import Lock

from fastapi import HTTPException, status

from data.airline_data import AIRLINE_SEATS
from models.seat import (
    AvailableSeatCount,
    BookSeatRequest,
    MealBookingStats,
    OccupancyStats,
    Seat,
    SeatActionResponse,
)


class BookingService:
    def __init__(self) -> None:
        self._booking_lock = Lock()

    def list_airlines(self) -> list[str]:
        return list(AIRLINE_SEATS.keys())

    def book_seat(self, airline: str, request: BookSeatRequest) -> SeatActionResponse:
        with self._booking_lock:
            seat = self._get_seat(airline, request.seatNo)
            self._validate_seat_is_available(airline, seat)
            seat.isBooked = True
            seat.mealBooked = request.mealBooked

        return SeatActionResponse(
            message="Seat booked successfully.",
            airline=airline,
            seat=seat,
        )

    def cancel_seat(self, airline: str, seat_no: str) -> SeatActionResponse:
        seat = self._get_seat(airline, seat_no)

        if not seat.isBooked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seat {seat.seatNo} is not booked for {airline}.",
            )

        seat.isBooked = False
        seat.mealBooked = False

        return SeatActionResponse(
            message="Seat cancelled successfully.",
            airline=airline,
            seat=seat,
        )

    def get_available_count(self, airline: str) -> AvailableSeatCount:
        seats = self._get_airline_seats(airline)
        available_count = sum(not seat.isBooked for seat in seats)

        return AvailableSeatCount(
            airline=airline,
            availableSeats=available_count,
            totalSeats=len(seats),
        )

    def get_seat_status(self, airline: str) -> list[Seat]:
        return self._get_airline_seats(airline)

    def get_occupancy_stats(self, airline: str) -> OccupancyStats:
        seats = self._get_airline_seats(airline)
        booked_seats = sum(seat.isBooked for seat in seats)
        occupancy_percentage = round((booked_seats / len(seats)) * 100, 2)

        return OccupancyStats(
            airline=airline,
            bookedSeats=booked_seats,
            totalSeats=len(seats),
            occupancyPercentage=occupancy_percentage,
        )

    def get_meal_stats(self, airline: str | None = None) -> list[MealBookingStats]:
        airlines = [airline] if airline else self.list_airlines()

        return [
            self._build_meal_stats(current_airline)
            for current_airline in airlines
        ]

    def _build_meal_stats(self, airline: str) -> MealBookingStats:
        seats = self._get_airline_seats(airline)

        return MealBookingStats(
            airline=airline,
            mealsBooked=sum(seat.mealBooked for seat in seats),
            bookedSeats=sum(seat.isBooked for seat in seats),
            totalSeats=len(seats),
        )

    def _get_airline_seats(self, airline: str) -> list[Seat]:
        seats = AIRLINE_SEATS.get(airline)

        if seats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Airline '{airline}' was not found.",
            )

        return seats

    def _get_seat(self, airline: str, seat_no: str) -> Seat:
        normalized_seat_no = seat_no.upper()

        for seat in self._get_airline_seats(airline):
            if seat.seatNo == normalized_seat_no:
                return seat

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat '{seat_no}' was not found for {airline}.",
        )

    def _validate_seat_is_available(self, airline: str, seat: Seat) -> None:
        if seat.isBooked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seat {seat.seatNo} is already booked for {airline}.",
            )


booking_service = BookingService()
