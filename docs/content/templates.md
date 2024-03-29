---
title: Templates
description: Extend templates to share layouts and UI across pages in your static site.
---

# Templates

Templates are used to share layouts, headers, and footers across your site.
A template defines "blocks" which can be overwritten by the pages that "extend" it.

To keep templates out of your final build (ex. "example.com/base.template/index.html")
you should always [use the naming convention `<name>.template.html`](/ignore/).

Every site starts with a `base.template.html` and a `content` block.

```html+jinja
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

## Defining blocks

You can put blocks wherever you like, and even nest them.

```html+jinja
<!-- base.template.html -->
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
<!-- my-page.html -->
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
<!-- case-study.template.html -->
{% extends "base.template.html" %}

{% block content_container %}
<div class="case-study-container">
    {% block case_study %}{% endblock %}
</div>
{% endblock %}
```

```html+jinja
<!-- newco-case-study.html -->
{% extends "case_study.template.html" %}

{% block case_study %}
<h1>NewCo Case Study</h1>
<p>...</p>
{% endblock %}
```
