# Partials

A useful convention for Combine sites is to create "partials".
These are simply snippets of HTML (saved in [ignored files](/ignore/)) that you can `{% include %}` in multiple places across your site.

```html+jinja
<h2>A page heading</h2>

<p>...</p>

{% include "partials/_help_footer.html" %}
```
