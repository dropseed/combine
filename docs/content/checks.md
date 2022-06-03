---
title: Checks
description: Fast, automated checks to build a usable, discoverable, and shareable static site.
---

# Checks

We maintain a set of carefully considered checks that we believe *every* successful public website should pass.
They can be considered "best practices",
but we deliberately choose things that are both valuable *and* achievable.

If you resolve all of the Combine checks, you will probably get good scores on other tools like [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) and [Ahrefs Site Audit](https://ahrefs.com/site-audit).
A big advantage of Combine checks is they run *while* you work,
so you can fix issues before they get published.


**Long story short, don't ignore combine checks.** They cover three core principles:

#### Keep it **Usable**

Find broken links, massive images, mixed-content warnings and all the simple things that make the difference between a good experience and a poor one.

#### Be **Discoverable**

Everybody wants to be showing up in Google searches. Doing the basics here goes a long way — write the page titles, add "alt" text on images, and have friendly URLs.

#### Make it **Shareable**

When links to your site are shared on Facebook or Twitter, do they look ok? We'll point out where you're missing the *most important* Open Graph tags.

## Internal link broken

Combine automatically detects broken links to internal pages.
You could have redirects for these in your hosting provider,
but there is no reason not to update the link to make it correct.

## Title missing

The `<title>` tag should be present on every page.

One way to do this is by using a "title" variable in the `<head>` section of your base template:

```html+jinja
<!-- base.template.html -->
<head>
  <title>{% if title is defined %}{{ title }} - {% endif %}YourBusinessName</title>
</head>
```

Then set the title variable on each page:

```html+jinja
<!-- about-us.html -->
{% extends "base.template.html" %}

{% set title = "About Us" %}
```

## Title empty

The `<title>` tag is present, but has no text.
This is typically a templating mistake.

## Meta description empty

The meta description tag is empty, which is typically a templating mistake.

Using a variable makes this easy to write for each page:

```html+jinja
<!-- base.template.html -->
<head>
  {% if description is defined %}<meta name="description" content="{{ description }}">{% endif %}
</head>
```

In HTML:

```html+jinja
<!-- my-page.html -->
{% extends "base.template.html" %}

{% set description = "Use Jinja and basic HTML and Markdown to build a simple, predictable static site." %}
```

And Markdown:

```markdown
<!-- my-page.md -->
---
description: Use Jinja and basic HTML and Markdown to build a simple, predictable static site.
---

Page content here...
```

## Meta description length

Meta descriptions should generally be between 50 and 320 characters long.

## Image alt missing

The "alt" text describes an image for both accessibility and SEO purposes:

```html+jinja
<!-- (HTML) -->
<img src="pancakes.png" alt="Stack of blueberry pancakes with powdered sugar">
```

If an image is purely decorative, then the alt text should be an empty string:

```html+jinja
<!-- (HTML) -->
<img src="curved-border.png" alt="">
```

## Duplicate ID

Duplicate IDs can cause problems for accessibility, JavaScript, links, and otherwise catch templating errors.
Every `id` on a page should be unique.

## Favicon missing

Using `/favicon.ico` is the easiest, most widely supported option for having a Favicon.
You can include other variations and their corresponding `<head>` tags,
but if you only do one thing,
simply put `favicon.ico` at the root of your site.

## HTTPS mixed content

Combine assumes you will deploy your site with HTTPS.
Linking to stylesheets, scripts, images, etc. through *http://* can cause browsers to display an insecure, "mixed content" warning.

## File size too large

We have some baseline checks to prevent you from accidentally using assets that are way bigger than they need to be
(often by mistake).
This usually involves images that can and should be downsized or compressed.

## Open Graph title missing

The Open Graph title can usually be the same as your page title,
but without any company/branding suffixes (which can instead be put in the Open Graph `site_name`).

If you use a templating pattern like is [mentioned above](#title-missing),
then you can use the same title variable for your `<title>` and "og:title".

```html+jinja
<!-- base.template.html -->
<head>
  {% if title is defined %}<meta property="og:title" content="{{ title }}" />{% endif %}
</head>
```

## Open Graph description missing

This should be a couple sentences describing your page,
which often shows up in places like Facebook when people link to your site.

Again, a templating solution can be handy here:

```html+jinja
<!-- base.template.html -->
<head>
  {% if description is defined %}<meta property="og:description" content="{{ description }}" />{% endif %}

  <!-- Optional: use the same variable for your general meta description -->
  {% if description is defined %}<meta name="description" content="{{ description }}">{% endif %}
</head>
```

```html+jinja
<!-- my-page.html -->
{% extends "base.template.html" %}

{% set description = "Use Jinja and basic HTML and Markdown to build a simple, predictable static site." %}
```

## Open Graph type missing

Unless you are writing articles or some other special kind of content,
the [Open Graph type](https://ogp.me/#types) can be set to "website" for all of your pages.

```html+jinja
<!-- base.template.html -->
<head>
  <meta property="og:type" content="website" />
</head>
```

## Open Graph URL missing

The Open Graph URL should be the canonical, absolute URL to the current page.

In Combine, the automatic [url variable](/variables/#url) and [`absolute_url` filter can help (don't forget to set the `base_url` variable though)](/absolute-urls/):

```html+jinja
<!-- base.template.html -->
<head>
  <meta property="og:url" content="{{ url|absolute_url }}" />
</head>
```

## Open Graph image missing

The Open Graph image gets used in all kinds of social networks on modern chat/document apps.
If you only do one thing, just set a default image for all pages on your site.

One solution is to set a default (note the use of the `absolute_url` filter to make it absolute),
and to use an optional variable for customizing per-page:

```html+jinja
<!-- base.template.html -->
<head>
  {% if image_url is defined -%}
  <meta property="og:image" content="{{ image_url|absolute_url }}" />
  {%- else -%}
  <meta property="og:image" content="{{ '/assets/img/open-graph.png'|absolute_url }}" />
  {%- endif %}
</head>
```

```html+jinja
<!-- my-page.html -->
{% extends "base.template.html" %}

{% set image_url = "/img/picture.png" %}
```

Dimensions and design can get confusing depending on which article you read,
but a simple example is to use a 1280px x 640px image like this template from GitHub:

![GitHub Open Graph template](/assets/img/repository-open-graph-template.png)

## Open Graph site_name missing

This can be the same on every page, and should reflect the name of your site.
Most of the time, this can just be the name of your company.

```html+jinja
<!-- base.template.html -->
<head>
  <meta property="og:site_name" content="YourBusinessName" />
</head>
```

## Open Graph URL not canonical HTTPS

[As mentioned above](#open-graph-url-missing), the URL needs to be absolute, canonical, and HTTPS.

## Open Graph image not canonical HTTPS

[As mentioned above](#open-graph-image-missing), the image needs to be absolute, canonical, and HTTPS.
