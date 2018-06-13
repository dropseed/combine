## Variables available by default

- `now` - the now function from datetime (usage example `{{ now().year }}`)

## Custom variables

To inject cutom variables, just put them in your `combine.yml`.

```yml
variables:
  test_variable: hey!
```

```html
<p>{{ test_variable }}</p>
```
