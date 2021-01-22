---
title: combine.yml steps
description: Define build steps for compiling assets for your static site.
---

# Steps

[Use steps to provide additional commands to be run during your build.](/build/)

The `run` command and `watch` patterns are executed from wherever you run `combine <build|work>`.
Typically this will be the root of your repo.

```yaml
steps:
  - run: "./node_modules/.bin/tailwind build ./content/assets/_main.css -o ./output/assets/main.css"
    watch:
      - "./tailwind.config.js"
      - "./content/assets/_main.css"
```

The `watch` field is not required.

```yaml
steps:
- run: "./node_modules/.bin/pitchfork index output -c .content"
```
