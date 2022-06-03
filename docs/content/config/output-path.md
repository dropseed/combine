---
title: combine.yml output_path
description: Choose which directory your static site is output to.
---

# Output path

The `output_path` can change where your site is created.

By default, Combine will put your site in the `output` directory:

```yaml
# combine.yml
output_path: output
```

This can be renamed if you have a conflict or are transitioning from another convention:

```yaml
# combine.yml
output_path: public
```

Or can be redirected out of your repo entirely:

```yaml
# combine.yml
output_path: /var/www/mysite
```
