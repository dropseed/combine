---
title: Absolute URLS
description: Create absolute URLs for production, staging, preview, and development environments.
---

# Absolute URLs

In some cases, like open graph tags, you are *required* to use an absolute URL.
The trick with this is that you will want it to be correct in development, staging/preview environments, *and* production.

The recommended way to do this is to use Combine's `absolute_url` Jinja filter,
which requires a variable named `base_url`.

### Setting the `base_url` variable

In your `combine.yml`, define the `base_url` variable so that it's available across your site.

Here's an example:

```yaml
variables:
  base_url:
    default: "https://combine.dropseed.io"
    from_env: URL  # netlify
```

In development, this will be automatically set to `http://127.0.0.1:{port}` when you run `combine work`.

In staging or preview environments, the best thing to do is use an environment variable to populate this automatically.
In this example we're using [the `URL` environment variable from Netlify](https://docs.netlify.com/configure-builds/environment-variables/#deploy-urls-and-metadata).

Production will also use the `URL` environment varible on Netlify,
but setting a default means that `combine build` will default to the production URL whether or not we run the command on Netlify.

### Using the `absolute_url` filter

With the `base_url` variable set,
you can now use the `absolute_url` filter to pull everything together and get correct absolute URLs across your site,
in every environment.

This works with hard-coded strings:

```html+jinja
<meta property="og:image" content="{{ '/static/img/open-graph.png'|absolute_url }}" />
```

As well as variables:

```html+jinja
<meta property="og:image" content="{{ image_url|absolute_url }}" />
```

Combine also automatically sets the `url` variable for the current page that is being built.
So in templates, you can use that to automatically create an absolute URL to the current page:

```html+jinja
<meta property="og:url" content="{{ url|absolute_url }}" />
```
