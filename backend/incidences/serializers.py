"""DRF serializers for the Incidence model."""

from rest_framework import serializers

from .models import Incidence, IncidenceStatus


class IncidenceSerializer(serializers.ModelSerializer):
    """
    Read-optimized serializer for listing incidences.

    Validates ``status`` against the ``IncidenceStatus`` enum so invalid
    values are rejected at the API boundary rather than hitting the DB.
    """

    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Incidence
        fields = [
            "id",
            "title",
            "fingerprint",
            "status",
            "status_display",
            "first_seen",
            "last_seen",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_status(self, value: str) -> str:
        valid = {s.value for s in IncidenceStatus}
        if value not in valid:
            raise serializers.ValidationError(
                f"Invalid status '{value}'. Must be one of: {', '.join(sorted(valid))}."
            )
        return value
