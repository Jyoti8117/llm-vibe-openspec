from fastapi import HTTPException

from models.seat import BookSeatRequest
from services.booking_service import BookingService


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def print_occupancy(service: BookingService, airline: str) -> None:
    stats = service.get_occupancy_stats(airline)
    print(
        f"{airline}: {stats.bookedSeats}/{stats.totalSeats} booked "
        f"({stats.occupancyPercentage}%)"
    )


def try_booking(
    service: BookingService,
    airline: str,
    seat_no: str,
    meal_booked: bool = False,
) -> None:
    try:
        response = service.book_seat(
            airline,
            BookSeatRequest(seatNo=seat_no, mealBooked=meal_booked),
        )
        meal_text = "with meal" if response.seat.mealBooked else "without meal"
        print(f"Booked {response.airline} seat {response.seat.seatNo} {meal_text}.")
    except HTTPException as exc:
        print(f"Could not book {airline} seat {seat_no}: {exc.detail}")


def try_cancel(service: BookingService, airline: str, seat_no: str) -> None:
    try:
        response = service.cancel_seat(airline, seat_no)
        print(f"Cancelled {response.airline} seat {response.seat.seatNo}.")
    except HTTPException as exc:
        print(f"Could not cancel {airline} seat {seat_no}: {exc.detail}")


def main() -> None:
    service = BookingService()

    print_section("Available Airlines")
    for airline in service.list_airlines():
        count = service.get_available_count(airline)
        print(f"{airline}: {count.availableSeats}/{count.totalSeats} seats available")

    print_section("Booking Seats")
    try_booking(service, "Indigo", "1A", meal_booked=True)
    try_booking(service, "Indigo", "1A", meal_booked=False)
    try_booking(service, "Air India", "1C", meal_booked=True)
    try_booking(service, "SpiceJet", "2F")

    print_section("Occupancy")
    print_occupancy(service, "Indigo")
    print_occupancy(service, "Air India")
    print_occupancy(service, "SpiceJet")

    print_section("Meal Statistics")
    for stats in service.get_meal_stats():
        print(
            f"{stats.airline}: {stats.mealsBooked} meals "
            f"for {stats.bookedSeats} booked seats"
        )

    print_section("Cancel Seat")
    try_cancel(service, "Indigo", "1A")
    print_occupancy(service, "Indigo")


if __name__ == "__main__":
    main()
