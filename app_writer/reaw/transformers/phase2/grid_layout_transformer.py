"""Grid layout transformer — produces GridLayoutProperties from LayoutDefinition."""

from models.property_objects import GridLayoutProperties
from models.react_definition_models import LayoutDefinition


class GridLayoutTransformer:
    """Transforms layout definition into grid layout properties."""

    @staticmethod
    def transform(layout: LayoutDefinition) -> GridLayoutProperties:
        """Produce grid layout properties for AppLayout.jsx and CSS.

        Args:
            layout: Layout definition from layout.json.

        Returns:
            GridLayoutProperties for template rendering.
        """
        return GridLayoutProperties(
            applicationName=layout.applicationName,
            header=layout.header,
            footer=layout.footer,
            leftNav=layout.leftNav,
            navGroups=layout.navGroups,
        )
