"""JWT transformer - creates JWT authentication properties."""

from models.layer_objects import JWTAuthenticationLayerObject


class JWTTransformer:
    """Transforms project metadata into JWT authentication properties."""
    
    @staticmethod
    def transform(package_name: str = "com.example") -> JWTAuthenticationLayerObject:
        """Transform to JWT authentication properties.
        
        Args:
            package_name: Base package name
            
        Returns:
            JWTAuthenticationLayerObject
        """
        return JWTAuthenticationLayerObject(
            packageName=f"{package_name}.auth",
            jwtSecret="your-secret-key-change-in-production",
            jwtExpiration=86400000  # 24 hours in milliseconds
        )
