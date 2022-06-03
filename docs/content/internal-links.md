---
title: Internal links
description: Link to pages using the predictable output from Combine.
---

# Internal links

The easiest way to link to pages and assets is to use relative paths.
These will work in both development and production,
and should be very predictable based on the names of your directories and files.

For example:

```html+jinja
<!-- (HTML) -->
<!-- To link to <repo>/content/pricing/enterprise.html -->
<a href="/pricing/enterprise/">Pricing</a>
```

The same is true for images, CSS, etc.

In some cases, like open graph tags, you are *required* to use an [absolute URL](/absolute-urls/) which gets more complicated.
