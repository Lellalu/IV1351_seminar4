from dataclasses import dataclass
from datetime import date

@dataclass
class Instrument:
    """Representing an instrument"""
    id: int
    brand: str
    rented_price_per_month: int

    def __str__(self):
        return f'id={self.id}, brand={self.brand}, rented_price_per_month={self.rented_price_per_month}'


@dataclass
class Rental:
    """Representing a rental"""
    id: int
    start_date: date
    end_date: date
    instrument_id: int
    student_id: int
    rental_policy_id: int

    def __str__(self):
        return f'id={self.id}, start_date={self.start_date}, end_date={self.end_date}, instrument_id={self.instrument_id}, student_id={self.student_id}, rental_policy_id={self.rental_policy_id}'