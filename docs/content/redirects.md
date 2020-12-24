# Redirects

Currently the best way to do proper redirects with Combine is to define them within your [hosting provider](/deploy/).

Some hosts don't provide a redirect feature though.
So if you really need redirects and are ok with it not being a real 301/302,
you can use Combine's basic HTML redirect template.

This works by creating a `{path}.redirect` page (like you would any other page) and putting a URL in the contents.
So, to redirect `/contact-us/` to `/contact/`,
you would create `contact-us.redirect` with this content:

```
/contact/
```

Under the hood, this is rendered using a template that will effectively get a user to where they need to go:

```html+jinja
<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8>
  <title>Redirecting...</title>
  <link rel=canonical href="{{ redirect_url }}">
  <meta http-equiv=refresh content="0; url={{ redirect_url }}">
</head>
<body>
  <h1>Redirecting...</h1>
  <a href="{{ redirect_url }}">Click here if you are not redirected.</a>
  <script>location='{{ redirect_url }}'</script>
</body>
</html>
```
