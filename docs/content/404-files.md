---
title: 404 files
description: Create 404 templates that your hosting provider can find.
---

# 404 files

Most hosting providers have an option to specify an error or 404 template.

Since Combine generates pretty urls automatically (which would move `content/404.html` to `output/404/index.html`),
there is an optional `.keep.html` extension that keeps files exactly where you put them.

For example, `content/404.keep.html` would be output as `output/404.html`.
