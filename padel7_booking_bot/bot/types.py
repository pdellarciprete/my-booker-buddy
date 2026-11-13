from typing import TypedDict


class VenueConfig(TypedDict):
    booking_url: str
    location: str
    courts: dict[str, str]
    indoor_courts: set[str]


class CourtPreferences(TypedDict):
    date: str | None
    time: str | None
    court_type: str
    venue_config: VenueConfig
    booked_by: str


class BookingDetails(TypedDict):
    date: str
    time: str
    court: str
    location: str
    cost: str
    booked_by: str
