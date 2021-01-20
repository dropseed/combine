# Checks

We maintain a set of carefully considered checks that we believe *every* successful public website should pass.
Sure, they can be considered "best practices".
But we deliberately choose things that are both valuable *and* achievable.

**Long story short, don't ignore combine checks.**

Our checks cover three core principles:

#### Keep it **Usable**

Find broken links, massive images, mixed-content warnings and all the simple things that make the difference between a good experience and a poor one.

#### Be **Discoverable**

Everybody wants to be showing up in Google searches. Doing the basics here goes a long way — write the page titles, add "alt" text on images, and have friendly URLs.

#### Make it **Shareable**

When links to your site are shared on Facebook or Twitter, do they look ok? We'll point out where you're missing the *most important* Open Graph tags.

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
