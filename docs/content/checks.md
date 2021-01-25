---
title: Checks
description: Fast, automated checks to build a usable, discoverable, and shareable static site.
---

# Checks

We maintain a set of carefully considered checks that we believe *every* successful public website should pass.
Sure, they can be considered "best practices".
But we deliberately choose things that are both valuable *and* achievable.

If you resolve all of the Combine checks, you will probably get good scores on other tools like [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) and [Ahrefs Site Audit](https://ahrefs.com/site-audit).
A big advantage of Combine checks is they run *while* you work,
so you can fix issues as they are created.


**Long story short, don't ignore combine checks.**

Our checks cover three core principles:

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

Try adding this to the `<head>` section of a template:
`<title>{% if title is defined %}{{ title }}{% endif %}</title>`

Then set the title variable on each page:
`{% set title = "Page Title" %}`

## Title empty

The `<title>` tag is present, but has no text.
This is typically a templating mistake.

## Meta description empty

The meta description tag is empty, which is typically a templating mistake.

## Meta description length

Meta descriptions should generally be between 50 and 320 characters long.

## Image alt missing

The "alt" text describes an image for both accessibility and SEO purposes:

```html
<img src="pancakes.png" alt="Stack of blueberry pancakes with powdered sugar">
```

If an image is purely decorative, then the alt text should be an empty string:

```html
<img src="curved-border.png" alt="">
```

## Duplicate ID

Duplicate IDs can cause problems for accessibility, JavaScript, links, and otherwise catch templating errors.
Every `id` on a page should be unique.

## Favicon missing

Using `/favicon.ico` is the easiest, most widely support option for having a Favicon.
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

## Open graph title missing

TODO

## Open graph description missing

TODO

## Open graph type missing

TODO

## Open graph url missing

TODO

## Open graph image missing

TODO

## Open graph site_name missing

TODO

## Open graph URL not canonical HTTPS

TODO

## Open graph image not canonical HTTPS

TODO
