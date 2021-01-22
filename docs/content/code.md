---
title: Code highlighting
description: Highlight code in HTML or Markdown pages using Pygments.
---

# Code highlighting

Technical documentation (like this site) oftens requires highlighting code.
Combine uses [Pygments](https://pygments.org/docs/) to do the highlighting and you can style it with CSS.

[The available languages/lexers can be found here.](https://pygments.org/docs/lexers/)

## Highlighting code in HTML pages

Combine comes with a `{% code %}` tag that works just liked the fenced code blocks in Markdown.

```html+jinja
{% code "python" %}
def test():
    print("hi!")
{% endcode %}
```

If your code sample uses Jinja-like syntax,
then use the `{% raw %}` tag to avoid conflicts.

```html+jinja
{% code "html" %}{% raw %}
{% code "python" %}
def test():
    print("hi!")
{% endcode %}
{% endraw %}{% endcode %}
```

## Highlighting code in Markdown pages

In Markdown you can use fenced code blocks just like you're used to.

````html+jinja
```python
def test():
    print("hi!")
```
````

## Styling with CSS

To style it, you just need to add some CSS.
Run `combine utils highlight-css` to output the CSS which can be copied and modified.
