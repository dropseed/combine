# Variables

Variables defined in `combine.yml` will be applied across your site,
and can be overridden with page-level variables.

The simplest way to define a variable is to hard-code a string:

```yaml
variables:
  site_name: My site
```

Variables can be set automatically by reading from environment variables:

```yaml
variables:
  google_tag_manager_id:
    from_env: GOOGLE_TAG_MANAGER_ID
```

And you can provide a `default` if there are situations where the env variable won't be present:

```yaml
variables:
  base_url:
    default: "https://combine.dropseed.io"
    from_env: URL  # a Netlify variable
```

[More about using variables →](/variables/)
