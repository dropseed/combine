---
title: Getting started
description: Create a new Combine static site and your first pages.
---

# Getting started

## Installing Combine

Combine is written in Python.
The easiest way to install and use it is with [barrel](https://barrel.dev).
If you're familiar with Python, you can also install it using pip/pipenv/poetry.

```sh
# (Terminal)
mkdir mysite
cd mysite
git init
echo "/output\n/.venv" > .gitignore
curl -sSL https://barrel.dev/install.py | python3 - combine
```

## Creating a site

All of your content will be located in a directory named "content".

**1. Create the content directory first:**

```sh
# (Terminal)
mkdir content
```

Inevitably you'll want at least one template for managing the `<head>` and `<body>` tags.
How you use it can evolve, but you should have one block named "content".

**2. Grab a starter you like or copy this into `content/base.template.html`:**

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

Most (if not all) of your pages will extend your main template.
You can [read more about how Jinja works](/jinja/) if you aren't familiar,
but the basics will get you a long way.

**3. Copy this into `content/index.html` to create your homepage:**

```html
<!-- index.html -->
{% extends "base.template.html" %}

{% block content %}
<h1>Home!</h1>
{% endblock %}
```

**4. Run `combine build` to put everything together.**

```sh
# (Terminal)
combine build
```

## Working on your site

When you're editing your site,
you'll want to use `combine work` to create a development server and automatically rebuild when you edit files.

```sh
# (Terminal)
combine work
```
