"""Pure fitness-domain functions used by the Flask routes and unit tests."""

from __future__ import annotations

from datetime import date, datetime

PROGRAMS = {
    "strength": {
        "goal": "strength",
        "name": "Foundation Strength",
        "sessions_per_week": 3,
        "focus": ["squat", "push", "pull", "core"],
    },
    "endurance": {
        "goal": "endurance",
        "name": "Cardio Endurance",
        "sessions_per_week": 4,
        "focus": ["steady cardio", "intervals", "mobility"],
    },
    "mobility": {
        "goal": "mobility",
        "name": "Move Better",
        "sessions_per_week": 3,
        "focus": ["hips", "shoulders", "spine", "balance"],
    },
    "weight-loss": {
        "goal": "weight-loss",
        "name": "Active Balance",
        "sessions_per_week": 5,
        "focus": ["full body", "walking", "intervals", "recovery"],
    },
}


WEEKLY_CLASSES = [
    {"day": "Monday", "time": "07:00", "name": "Strength Basics"},
    {"day": "Tuesday", "time": "18:00", "name": "Cardio Circuit"},
    {"day": "Wednesday", "time": "07:30", "name": "Mobility Flow"},
    {"day": "Friday", "time": "18:30", "name": "Full Body Fitness"},
]


def get_program(goal: str):
    """Return a program for a normalized fitness goal."""
    normalized = goal.strip().lower().replace("_", "-").replace(" ", "-")
    return PROGRAMS.get(normalized)


def calculate_bmi(height_cm, weight_kg) -> dict:
    """Calculate BMI and return a rounded value plus a standard category."""
    try:
        height = float(height_cm)
        weight = float(weight_kg)
    except (TypeError, ValueError) as exc:
        raise ValueError("height_cm and weight_kg must be numbers.") from exc

    if height <= 0 or weight <= 0:
        raise ValueError("height_cm and weight_kg must be greater than zero.")
    if height > 300 or weight > 700:
        raise ValueError("height_cm or weight_kg is outside the supported range.")

    bmi = weight / ((height / 100) ** 2)
    rounded_bmi = round(bmi, 1)

    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "healthy"
    elif bmi < 30:
        category = "overweight"
    else:
        category = "obesity"

    return {
        "height_cm": height,
        "weight_kg": weight,
        "bmi": rounded_bmi,
        "category": category,
    }


def check_membership(expiry_date: str, today: date | None = None) -> dict:
    """Return active or expired status for an ISO-formatted membership date."""
    try:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("expiry_date must use YYYY-MM-DD format.") from exc

    reference_date = today or date.today()
    days_remaining = (expiry - reference_date).days
    return {
        "expiry_date": expiry.isoformat(),
        "status": "active" if days_remaining >= 0 else "expired",
        "days_remaining": max(days_remaining, 0),
    }
