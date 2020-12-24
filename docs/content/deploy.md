# Deployment

Ultimately a Combine site is like any other static site.
You can deploy it to a number of hosts or custom servers,
often times for free.

A Google search will turn up lots of options, but here are a few:

- [GitHub Pages](https://pages.github.com/)
- [Netlify](https://www.netlify.com/)
- [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html)
- [Digital Ocean App Platform](https://www.digitalocean.com/products/app-platform/)

Wherever you host it, the gist of deploying is running `combine build` and pointing the host to the `<repo>/output` directory.

On Netlify, for example, you can run these commands in their build environment which can leverage environment variables and a simple git-push-deploy workflow.

If you use `netlify.toml`, it would look like this:

```toml
[build]
    publish = "output"
    command = "combine build"
```

## Redirects

One other thing to keep in mind for deploying is [how redirects can be handled](/redirects/).
You may not need them right off the bat,
but eventually content will move and it would be ideal to do a proper 301/302 redirect.

On Netlify, this can again be set in `netlify.toml`:

```toml
[build]
    publish = "output"
    command = "combine build"

[[redirects]]
    from = "/contact-us/"
    to = "/contact/"
```

If your host doesn't have redirects and you're ok with not having a true server-level redirect,
then you can use Combine's [HTML redirect template](/redirects/).
