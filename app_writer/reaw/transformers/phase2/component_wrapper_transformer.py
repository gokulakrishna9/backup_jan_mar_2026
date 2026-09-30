"""Component wrapper transformer — produces ComponentWrapperProperties for PrimeReact wrappers."""

from typing import List

from models.property_objects import ComponentWrapperProperties


# The 10 PrimeReact wrapper components
_WRAPPERS = [
    ("DataTableWrapper", "DataTable", "primereact/datatable"),
    ("InputTextWrapper", "InputText", "primereact/inputtext"),
    ("InputNumberWrapper", "InputNumber", "primereact/inputnumber"),
    ("CalendarWrapper", "Calendar", "primereact/calendar"),
    ("DropdownWrapper", "Dropdown", "primereact/dropdown"),
    ("CheckboxWrapper", "Checkbox", "primereact/checkbox"),
    ("InputTextareaWrapper", "InputTextarea", "primereact/inputtextarea"),
    ("ButtonWrapper", "Button", "primereact/button"),
    ("DialogWrapper", "Dialog", "primereact/dialog"),
    ("ToastWrapper", "Toast", "primereact/toast"),
]


class ComponentWrapperTransformer:
    """Produces properties for the 10 PrimeReact wrapper components."""

    @staticmethod
    def transform() -> List[ComponentWrapperProperties]:
        """Produce wrapper properties for all PrimeReact components.

        Returns:
            List of ComponentWrapperProperties for each wrapper.
        """
        return [
            ComponentWrapperProperties(
                componentName=name,
                primeReactComponent=prime_component,
                primeReactImport=import_path,
            )
            for name, prime_component, import_path in _WRAPPERS
        ]
