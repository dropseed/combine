---
title: Build steps
description: Define build steps for compiling assets for your static site.
---

# Build steps

Modern sites often come with build or compile steps for CSS and JavaScript.

Combine supports these workflows by integrating these commands directly into the build process.

In development, each build step can define a `watch` process that will run in the background during `combine work`:

```yaml
steps:
- run: "./node_modules/.bin/tailwind -i ./content/assets/_main.css -o ./output/assets/main.css"
  watch: "./node_modules/.bin/tailwind -i ./content/assets/_main.css -o ./output/assets/main.css --watch"
```

The `run` process will be used when building the production site,
and it will also be used during `combine work` (after a full site rebuild) if no `watch` process is defined:

```yaml
steps:
- run: "./node_modules/.bin/pitchfork index output -c .content"
```

If you want the `run` process to be run after a specific file is modified during `combine work`,
you can define a list of [patterns](https://docs.python.org/3/library/fnmatch.html) and Combine will also re-run the `run` process when any of those files are modified:

```yaml
steps:
- run: "./node_modules/.bin/pitchfork index output -c .content"
  watch:
    - "./content/*.html"
    - "./content/*.js"
```

Note that the `run` processes happen *after* combine has rendered the rest of your site.
So when you are generating output,
you are the one responsible for putting it in the end location you want it (i.e. `./output/css/main.css`).
This keeps the generated/compiled files out of your `content` directory which is tracked in git.

As you can see in the example,
you'll often want to combine this with the [ignored files](/ignore/) feature to keep the source files out of your final build.
