---
title: combine.yml variables
description: Set variables across your site using hardcoded values or environment variables.
---

# Variables

Variables defined in `combine.yml` will be applied across your site,
and can be overridden with page-level variables.

The simplest way to define a variable is to hard-code a string:

```yaml
# combine.yml
variables:
  site_name: My site
```

Variables can be set automatically by reading from environment variables:

```yaml
# combine.yml
variables:
  google_tag_manager_id:
    from_env: GOOGLE_TAG_MANAGER_ID
```

And you can provide a `default` if there are situations where the env variable won't be present:

```yaml
# combine.yml
variables:
  base_url:
    default: "https://combine.dropseed.dev"
    from_env: URL  # a Netlify variable
```

[More about using variables →](/variables/)
