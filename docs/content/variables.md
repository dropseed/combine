---
title: Variables
description: Set variables across your site using hardcoded values or environment variables.
---

# Variables

Variables can be set on specific pages, or across the entire site.

## Site variables

Site variables are often used to change output for development, staging, and production environments.
The best place to put these is in [combine.yml](/config/variables/).

### Hard-coding variables in combine.yml

```yaml
variables:
  site_name: My site
  version: v3.1.1
```

### Using environment variables in combine.yml

You can leverage environment variables keep settings out of your repo or get build environment details from your hosting provider.

```yaml
variables:
  base_url:
    default: "https://combine.dropseed.io"
    from_env: URL  # a Netlify variable
```

If you want the environment variable to be "required",
then simply remove the `default` field.

```yaml
variables:
  google_tag_manager_id:
    from_env: GOOGLE_TAG_MANAGER_ID
```

Combine will throw an error if you use an "undefined" variable
(which can help catch deployment misconfigurations if you forget to set the env variables).

```html+jinja
<script>
    ...{{ google_tag_manager_id }}
</script>
```

In some scenarios,
a missing environment variable is ok and you can write a special if statement to check that case.
Be careful when you do this though — you lose your safety net if the env variable is accidentally removed.

```html+jinja
{% if google_tag_manager_id is defined %}
<script>
    ...{{ google_tag_manager_id }}
</script>
{% endif %}
```

## Page variables

The other way to use variables is to define them on specific pages.
This is often used to pass the values back to the template they are extending.

An example would be setting meta values in the `<head>` of your root template:

```html+jinja
<!-- base.template.html -->
<head>
  {% if title is defined %}<meta property="og:title" content="{{ title }}" />{% endif %}
</head>
```

### Setting variables in HTML

There is both a single-line and multi-line way to use Jinja [`{% set %}`](https://jinja.palletsprojects.com/en/2.11.x/templates/#assignments) tag.

```html+jinja
{% extends "base.template.html" %}

{% set title = "My page title" %}
```

```html+jinja
{% extends "base.template.html" %}

{% set title -%}
My page title
{%- endset %}
```

### Setting variables in Markdown

In [Markdown pages](/markdown/), you can set variables using YAML frontmatter.

```md
---
title: My page title
---

My page content with frontmatter above it!
```

## Built-in variables

There are a handful of variables that Combine sets automatically.

### `env`

Automatically set to `development` when running `combine work`,
and `production` when running `combine build`.

### `now`

Automatically set to the current time of the build.
This is the Python `datetime.datetime.now` function and can be used in templates as `{{ now().year }}`, for example.

### `template`

Used only in Markdown to determine which template to use for rendering the page.
Set to `markdown.template.html` by default and can be overriden with frontmatter.

### `base_url`

Automatically set to `http://127.0.0.1:{port}` in development,
and is required by the [`absolute_url` filter](/absolute-urls/).

### `url`

Automatically set to the URL of the *current* page when it is being built.
