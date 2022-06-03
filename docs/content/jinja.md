---
title: Jinja
description: Use all of the built-in Jinja functionality to render HTML pages.
---

# Jinja basics

> "Jinja is a modern and designer-friendly templating language for Python, modelled after Django’s templates."

[Jinja](https://jinja.palletsprojects.com/en/2.11.x/) is widely used in the Python world and comes with a lot of features.

These are some of the common uses within Combine,
but can always look at the [Jinja documentation](https://jinja.palletsprojects.com/en/2.11.x/) for more detail and functionality.

## Inheritance and blocks

Extending templates is fundamental to how Combine works.

Any file can be "extended",
but Combine will automatically keep anything ending in `.template.html` *out* your final build
(you don't want `base.template.html` to be deployed to the live site).

```html
<!-- base.template.html -->
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

Use the defined `block`s to insert your content.

```html
<!-- pricing.html -->
{% extends "base.template.html" %}

{% block content %}
<div class="pricing">
    <div class="flex">
        ...
    </div>
</div>
{% endblock %}
```

[More about template inheritance →](https://jinja.palletsprojects.com/en/2.11.x/templates/#template-inheritance)

## Variables, loops, and if statements

Insert [variables](https://jinja.palletsprojects.com/en/2.11.x/templates/#variables) using `{{ }}`.

```html
<!-- (HTML) -->
<meta name="description" content="{{ description }}">
```

Use [filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#filters) to modify a variable during output.

```html
<!-- (HTML) -->
<meta name="description" content="{{ description|striptags }}">
```

Iterate over objects using [for-loops](https://jinja.palletsprojects.com/en/2.11.x/templates/#for).

```html
<!-- (HTML) -->
{% for item in ["one", "two", "three"] %}
<li>{{ item }}</li>
{% endfor %}
```

[If statements](https://jinja.palletsprojects.com/en/2.11.x/templates/#if) use `if`, `elif`, and `endif`.

```html
<!-- (HTML) -->
{% if custom_variable_name %}
<h1>Use {{ custom_variable_name }}</h1>
{% endif %}
```

Combine will throw an error if a variable is not defined,
so if some pages have a variable that others don't,
you might need to more specifically check if it `is defined`.


```html
<!-- (HTML) -->
{% if custom_variable_name is defined %}
<h1>Use {{ custom_variable_name }}</h1>
{% endif %}
```

## Comments

Use `{# #}` to leave comments in Jinja.
Unlike HTML comments (`<!-- -->`),
Jinja comments will *not* show up on the live site.

```html
<!-- (HTML) -->
{# This is a comment #}
<div>
    <h1>Heading</h1>
</div>
```

[More about comments →](https://jinja.palletsprojects.com/en/2.11.x/templates/#comments)

## Syntax collisions

Sometimes you'll run into situations where Jinja's `{{ }}` syntax will conflict with a JavaScript library or writing code examples.
The easiest way around this is to surround your code with the `{% raw %}{% endraw %}` tag.
This works across multiple lines as well as on a single line.

For example:

```html
<!-- (HTML) -->
<code>{% raw %}{% code %}{% endraw %}</code>
```

Would render this in your final HTML:

```
<!-- (HTML) -->
<code>{% code %}</code>
```

For variables that include HTML, use the `|safe` filter:

```
<!-- (HTML) -->
<div>
  {{ variable_with_html|safe }}
</div>
```

[More about escaping →](https://jinja.palletsprojects.com/en/2.11.x/templates/#escaping)
