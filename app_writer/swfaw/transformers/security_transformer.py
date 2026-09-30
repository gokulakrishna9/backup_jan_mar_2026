"""Security transformer - creates security config properties."""

from models.layer_objects import SecurityConfigLayerObject


class SecurityTransformer:
    """Transforms project metadata into security config properties."""
    
    @staticmethod
    def transform(package_name: str = "com.example") -> SecurityConfigLayerObject:
        """Transform to security config properties.
        
        Args:
            package_name: Base package name
            
        Returns:
            SecurityConfigLayerObject
        """
        return SecurityConfigLayerObject(
            packageName=f"{package_name}.config",
            jwtSecret="your-secret-key-change-in-production",
            jwtExpiration=86400000  # 24 hours in milliseconds
        )
