"""Flask application factory and HTTP routes for ACEest Fitness and Gym."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from .fitness import (
    PROGRAMS,
    WEEKLY_CLASSES,
    calculate_bmi,
    check_membership,
    get_program,
)


def _error(message: str, status_code: int):
    """Return a consistent JSON error response."""
    return jsonify({"status": "error", "message": message}), status_code


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the ACEest Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(JSON_SORT_KEYS=False)

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            programs=PROGRAMS,
            weekly_classes=WEEKLY_CLASSES,
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "service": "aceest-fitness-api",
                "status": "healthy",
                "version": "1.0.0",
            }
        )

    @app.get("/api/programs")
    def list_programs():
        return jsonify({"programs": PROGRAMS, "count": len(PROGRAMS)})

    @app.get("/api/programs/<goal>")
    def program_by_goal(goal: str):
        program = get_program(goal)
        if program is None:
            return _error(
                "Unknown goal. Choose strength, endurance, mobility, or weight-loss.",
                404,
            )
        return jsonify(program)

    @app.post("/api/bmi")
    def bmi():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return _error("Request body must be a JSON object.", 400)

        try:
            result = calculate_bmi(
                height_cm=payload.get("height_cm"),
                weight_kg=payload.get("weight_kg"),
            )
        except (TypeError, ValueError) as exc:
            return _error(str(exc), 400)

        return jsonify(result)

    @app.post("/api/membership/check")
    def membership_check():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload.get("expiry_date"):
            return _error("expiry_date is required in YYYY-MM-DD format.", 400)

        try:
            result = check_membership(str(payload["expiry_date"]))
        except ValueError as exc:
            return _error(str(exc), 400)

        return jsonify(result)

    @app.get("/api/classes")
    def classes():
        return jsonify({"classes": WEEKLY_CLASSES, "count": len(WEEKLY_CLASSES)})

    @app.errorhandler(404)
    def not_found(_error_value):
        return _error("Resource not found.", 404)

    return app
