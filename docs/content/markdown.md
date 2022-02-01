---
title: Markdown
description: Render Markdown directly in your HTML, or build entire pages in Markdown.
---

# Markdown

Combine offers two ways to use Markdown.
One way is to write specific sections of an HTML page in Markdown.
The other is to write *entire* pages in pure Markdown.

## Markdown in HTML

On an HTML page, use Combine's `{% markdown %}` tag to switch modes.

```html+jinja
<h1>Some HTML!</h1>

{% markdown %}
## And content
{% endmarkdown %}
```

When paired with `{% include %}`,
you can import Markdown content from another file.
This can be a useful pattern embedding user- or machine-generated files are also readable on sites like GitHub.

```html+jinja
<h2>You can also include a markdown file</h2>

{% markdown %}
{% include "README.md" %}
{% endmarkdown %}
```

You can also render variables to markdown using the `|markdown` filter.

```html+jinja
<h2>The markdown filter</h2>

{{ variable|markdown }}
```

## Entire pages in Markdown

For simple pages (like documentation) you can choose to write an entire file in Markdown.
The only requirement is that you have a block named `content` in your `base.template.html`.

```md
# A Markdown page

Everything in here will be rendered using `markdown.template.html`!
```

You can customize the default Markdown template by creating your own `content/markdown.template.html` file. This is the default:

```html+jinja
{% extends "base.template.html" %}

{% block content %}
{% markdown %}
{{ content }}
{% endmarkdown %}
{% endblock %}
```

### Frontmatter

Markdown files can use frontmatter to set specific variables for the page,
or to choose a specific template.
The `template` field has special behavior,
but anything else will be injected into the page as a [variable](/variables/).

```md
---
title: Group conditions
description: Custom rules for deciding who needs to review which PRs
template: config/field.template.html
next:
  url: /config/labels/
  title: Group labels
---

# A markdown page

Everything in here will be rendered using `markdown.template.html`!
```

## HTML in Markdown

When you're writing in Markdown,
you can also write straight HTML for more specific styling.

```md
# Heading

<p class="text-lg">A larger paragraph style.</p>
```
