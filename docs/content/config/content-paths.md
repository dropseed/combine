# Content paths

Combine merges multiple `content_paths` together before rendering your final site.
You will rarely need to change this behavior.

By default, this includes a set of templates defined by Combine itself + your `content`:

```yaml
content_paths:
- "content"
- "<combine path>/base_content"
```

If a [`theme`](/theme/) is present,
that will be included too:

```yaml
content_paths:
- "content"
- "theme/content"
- "<combine path>/base_content"
```
