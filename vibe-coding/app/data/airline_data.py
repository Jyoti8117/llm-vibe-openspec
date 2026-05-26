from dataclasses import dataclass
from random import Random

from models.seat import Seat, SeatClass


@dataclass(frozen=True)
class CabinLayout:
    min_seats: int
    max_seats: int
    premium_rows: int
    premium_letters: tuple[str, ...]
    economy_letters: tuple[str, ...]


AIRLINE_LAYOUTS = {
    "Indigo": CabinLayout(36, 50, 2, ("A", "B", "C", "D", "E", "F"), ("A", "B", "C", "D", "E", "F")),
    "Akasa": CabinLayout(30, 48, 2, ("A", "B", "C", "D", "E", "F"), ("A", "B", "C", "D", "E", "F")),
    "Air India": CabinLayout(32, 50, 3, ("A", "C", "D", "F"), ("A", "B", "C", "D", "E", "F")),
    "SpiceJet": CabinLayout(30, 48, 1, ("A", "B", "C", "D", "E", "F"), ("A", "B", "C", "D", "E", "F")),
    "Air India Express": CabinLayout(24, 42, 1, ("A", "C", "D", "F"), ("A", "B", "C", "D", "E", "F")),
}


def _generate_seats(airline: str, layout: CabinLayout) -> list[Seat]:
    randomizer = Random(airline)
    total_seats = randomizer.randint(layout.min_seats, layout.max_seats)
    seats: list[Seat] = []
    row = 1

    while len(seats) < total_seats:
        if row == 13:
            row += 1
            continue

        seat_class = SeatClass.premium if row <= layout.premium_rows else SeatClass.economy
        letters = layout.premium_letters if seat_class == SeatClass.premium else layout.economy_letters

        for letter in letters:
            if len(seats) == total_seats:
                break

            seats.append(Seat(seatNo=f"{row}{letter}", class_=seat_class))

        row += 1

    return seats


AIRLINE_SEATS: dict[str, list[Seat]] = {
    airline: _generate_seats(airline, layout)
    for airline, layout in AIRLINE_LAYOUTS.items()
}
