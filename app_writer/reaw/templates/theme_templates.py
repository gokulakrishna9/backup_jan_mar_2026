"""Jinja2 templates for theme CSS files."""

THEME_VARIABLES = """:root {
  /* ── Color Palette ── */
{% for token, value in colorPalette.items() %}  --{{ token }}: {{ value }};
{% endfor %}

  /* ── Typography ── */
  --font-family: {{ typography.fontFamily }};
  --font-size: {{ typography.fontSize }};
  --font-size-small: {{ typography.fontSizeSmall }};
  --font-size-large: {{ typography.fontSizeLarge }};
  --heading-font-family: {{ typography.headingFontFamily or typography.fontFamily }};
  --heading-font-weight: {{ typography.headingFontWeight }};
  --line-height: {{ typography.lineHeight }};

  /* ── Spacing ── */
  --spacing-unit: {{ spacing.unit }};
  --spacing-small: {{ spacing.small }};
  --spacing-medium: {{ spacing.medium }};
  --spacing-large: {{ spacing.large }};
  --spacing-xlarge: {{ spacing.xlarge }};

  /* ── Borders ── */
  --border-radius: {{ borders.radius }};
  --border-radius-large: {{ borders.radiusLarge }};
  --border-width: {{ borders.width }};
  --border-color: {{ borders.color }};

  /* ── Shadows ── */
  --shadow-small: {{ shadows.small }};
  --shadow-medium: {{ shadows.medium }};
  --shadow-large: {{ shadows.large }};

{% if animationsEnabled and animationStyle %}  /* ── Animations ── */
  --transition-duration: {{ animationStyle.transitionDuration }};
  --easing-function: {{ animationStyle.easingFunction }};
{% endif %}}
"""

PRIMEREACT_OVERRIDES = """/* PrimeReact theme overrides using CSS custom properties */

/* ── Global ── */
body {
  font-family: var(--font-family);
  font-size: var(--font-size);
  line-height: var(--line-height);
  color: var(--text-primary, #495057);
  background: var(--background-primary, #f8f9fa);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--heading-font-family);
  font-weight: var(--heading-font-weight);
}

/* ── Buttons ── */
.p-button {
  background: var(--accent, #6366f1);
  border-color: var(--accent, #6366f1);
  border-radius: {{ components.button.borderRadius | default('var(--border-radius)') }};
  font-weight: {{ components.button.fontWeight | default('500') }};
  padding: {{ components.button.padding | default('var(--spacing-medium) var(--spacing-large)') }};
{% if animationsEnabled and animationStyle %}  transition: background var(--transition-duration) var(--easing-function),
              border-color var(--transition-duration) var(--easing-function),
              transform var(--transition-duration) var(--easing-function);
{% endif %}}

{% if animationsEnabled and animationStyle %}.p-button:hover {
{% if animationStyle.hover.type == 'background-shift' %}  filter: brightness(1.1);
{% endif %}}

.p-button:active {
{% if animationStyle.click.type == 'scale' %}  transform: scale(0.97);
{% endif %}}
{% endif %}

/* ── Inputs ── */
.p-inputtext,
.p-inputnumber-input,
.p-inputtextarea {
  border-color: var(--border-color, #dee2e6);
  border-radius: {{ components.input.borderRadius | default('var(--border-radius)') }};
  padding: {{ components.input.padding | default('var(--spacing-medium) var(--spacing-medium)') }};
  font-family: var(--font-family);
  font-size: var(--font-size);
{% if animationsEnabled and animationStyle %}  transition: border-color var(--transition-duration) var(--easing-function),
              box-shadow var(--transition-duration) var(--easing-function);
{% endif %}}

{% if animationsEnabled and animationStyle %}.p-inputtext:focus,
.p-inputnumber-input:focus,
.p-inputtextarea:focus {
{% if animationStyle.focus.type == 'outline' %}  box-shadow: 0 0 0 2px var(--accent, #a5b4fc);
{% endif %}}
{% endif %}

/* ── DataTable ── */
.p-datatable .p-datatable-thead > tr > th {
  background: {{ components.table.headerBackground | default('var(--surface, #f8f9fa)') }};
  color: var(--text-primary, #495057);
  font-weight: var(--heading-font-weight);
}

.p-datatable .p-datatable-tbody > tr {
{% if animationsEnabled and animationStyle %}  transition: background var(--transition-duration) var(--easing-function);
{% endif %}}

{% if animationsEnabled and animationStyle %}.p-datatable .p-datatable-tbody > tr:hover {
  background: {{ components.table.rowHoverBackground | default('var(--surface, #e9ecef)') }};
}

.p-datatable .p-datatable-tbody > tr.p-highlight {
{% if animationStyle.selection.type == 'fade' %}  background: var(--accent, #a5b4fc);
  opacity: 0.9;
{% endif %}}
{% endif %}

/* ── Card ── */
.p-card {
  border-radius: {{ components.card.borderRadius | default('var(--border-radius-large)') }};
  box-shadow: {{ components.card.shadow | default('var(--shadow-small)') }};
}

/* ── Sidebar / Navigation ── */
{% if components.sidebar %}.layout-sidebar,
.app-sidebar {
{% if components.sidebar.background %}  background: {{ components.sidebar.background }};
{% endif %}{% if components.sidebar.textColor %}  color: {{ components.sidebar.textColor }};
{% endif %}}

{% if components.sidebar.activeBackground %}.layout-sidebar .active-link,
.app-sidebar .active-link {
  background: {{ components.sidebar.activeBackground }};
}
{% endif %}{% endif %}

/* ── TabView ── */
.p-tabview .p-tabview-nav li .p-tabview-nav-link {
{% if animationsEnabled and animationStyle %}  transition: border-color var(--transition-duration) var(--easing-function),
              color var(--transition-duration) var(--easing-function);
{% endif %}}

/* ── Dialog ── */
.p-dialog {
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-large);
}

/* ── Toast ── */
.p-toast .p-toast-message {
  border-radius: var(--border-radius);
}
"""
