---
title: combine.yml steps
description: Define build steps for compiling assets for your static site.
---

# Steps

[Use steps to provide additional commands to be run during your build.](/build/)

The `run` command will be executed whenever a full site build is processed:

```yaml
# combine.yml
steps:
- run: "./node_modules/.bin/pitchfork index output -c .content"
```

To also run the command when specific files are edited locally,
you can specify a list of patterns under `watch`:

```yaml
# combine.yml
steps:
  - run: "./node_modules/.bin/tailwind -i ./content/assets/_main.css -o ./output/assets/main.css"
    watch:
      - "./tailwind.config.js"
      - "./content/assets/_main.css"
```

For tools that include their own watch process,
you can have Combine run that command automatically during `combine work` by specifing a command string instead of a list of patterns:

```yaml
# combine.yml
steps:
  - run: "./node_modules/.bin/tailwind -i ./content/assets/_main.css -o ./output/assets/main.css"
    watch: "./node_modules/.bin/tailwind -i ./content/assets/_main.css -o ./output/assets/main.css --watch"
```
