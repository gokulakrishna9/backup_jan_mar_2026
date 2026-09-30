"""Activity tracking schema generator - generates activity tracking SQL schema."""

from templates.activity_tracking_templates import ActivityTrackingTemplates


class ActivityTrackingSchemaGenerator:
    """Generates activity tracking database schema SQL."""
    
    @staticmethod
    def generate() -> str:
        """Generate complete activity tracking schema SQL.
        
        Returns:
            SQL string with complete schema
        """
        return ActivityTrackingTemplates.ACTIVITY_TRACKING_SCHEMA_SQL
