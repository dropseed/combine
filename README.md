# Combine

**Build a straightforward marketing or documentation website with the power of [Jinja](http://jinja.pocoo.org/).
No fancy JavaScript here &mdash; this is just like the good old days.**

Put your site into the "content" directory and Combine will:

- Render files using Jinja
- Create pretty URLs ("file-system routing")
- Inject variables
- Run custom build steps (like building Tailwind)

Most sites follow a simple pattern.

Create a `base.template.html`:

```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My site</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

And use it (ex. `pricing.html`):

```html+jinja
{% extends "base.template.html" %}

{% block content %}
<div class="pricing">
    <div class="flex">
        ...
    </div>
</div>
{% endblock %}
```

In the end, you get a static HTML site that can be deployed almost anywhere.
