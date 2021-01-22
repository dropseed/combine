---
title: Templates
description: Extend templates to share layouts and UI across pages in your static site.
---

# Templates

Every site starts with a `base.template.html` and a `content` block.

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

## Defining blocks

You can put blocks wherever you like, and even nest them.

```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My site</title>
</head>
<body>
    {% block navbar %}
    <nav>
        ...
    </nav>
    {% endblock %}

    {% block content_container %}
    <div class="h-screen">
        {% block content %}{% endblock %}
    </div>
    {% endblock %}

    <footer>
        ...
    </footer>
</body>
</html>
```

## Building pages from templates

To use a template, just build a page that `extends` it and overrides any of the blocks.

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

## Building templates from templates

You can layer your templates to style entire sections of your site.

```html+jinja
{% extends "base.template.html" %}

{% block content_container %}
<div class="case-study-container">
    {% block case_study %}{% endblock %}
</div>
{% endblock %}
```

```html+jinja
{% extends "case_study.template.html" %}

{% block case_study %}
<h1>NewCo Case Study</h1>
<p>...</p>
{% endblock %}
```
