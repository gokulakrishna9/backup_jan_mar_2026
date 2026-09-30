"""Activity tracking generator - generates user activity tracking entities and repositories."""

from templates.activity_tracking_templates import ActivityTrackingTemplates


class ActivityTrackingGenerator:
    """Generates user activity tracking components."""
    
    @staticmethod
    def generate_crud_activity_log_entity(package_name: str) -> str:
        """Generate CrudActivityLog entity."""
        return ActivityTrackingTemplates.generate_crud_activity_log_entity(package_name)
    
    @staticmethod
    def generate_deleted_record_entity(package_name: str) -> str:
        """Generate DeletedRecord entity."""
        return ActivityTrackingTemplates.generate_deleted_record_entity(package_name)
    
    @staticmethod
    def generate_login_activity_log_entity(package_name: str) -> str:
        """Generate LoginActivityLog entity."""
        return ActivityTrackingTemplates.generate_login_activity_log_entity(package_name)
    
    @staticmethod
    def generate_grant_activity_log_entity(package_name: str) -> str:
        """Generate GrantActivityLog entity."""
        return ActivityTrackingTemplates.generate_grant_activity_log_entity(package_name)
    
    @staticmethod
    def generate_crud_activity_log_repository(package_name: str) -> str:
        """Generate CrudActivityLogRepository."""
        return ActivityTrackingTemplates.generate_crud_activity_log_repository(package_name)
    
    @staticmethod
    def generate_deleted_record_repository(package_name: str) -> str:
        """Generate DeletedRecordRepository."""
        return ActivityTrackingTemplates.generate_deleted_record_repository(package_name)
    
    @staticmethod
    def generate_login_activity_log_repository(package_name: str) -> str:
        """Generate LoginActivityLogRepository."""
        return ActivityTrackingTemplates.generate_login_activity_log_repository(package_name)
    
    @staticmethod
    def generate_grant_activity_log_repository(package_name: str) -> str:
        """Generate GrantActivityLogRepository."""
        return ActivityTrackingTemplates.generate_grant_activity_log_repository(package_name)
    
    @staticmethod
    def generate_activity_tracking_service(package_name: str) -> str:
        """Generate ActivityTrackingService."""
        return ActivityTrackingTemplates.generate_activity_tracking_service(package_name)
    
    @staticmethod
    def generate_activity_tracking_controller(package_name: str) -> str:
        """Generate ActivityTrackingController."""
        return ActivityTrackingTemplates.generate_activity_tracking_controller(package_name)
