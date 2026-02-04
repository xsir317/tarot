"""Test Reading models."""

from app.models.reading import Reading


def test_reading_model_attributes():
    """Test Reading model has correct attributes."""
    assert hasattr(Reading, "id")
    assert hasattr(Reading, "user_id")
    assert hasattr(Reading, "question")
    assert hasattr(Reading, "gender")
    assert hasattr(Reading, "language")
    assert hasattr(Reading, "cards")
    assert hasattr(Reading, "individual_interpretations")
    assert hasattr(Reading, "overall_interpretation")
    assert hasattr(Reading, "quota_type")


def test_reading_model_table_name():
    """Test Reading model has correct table name."""
    assert Reading.__tablename__ == "readings"
