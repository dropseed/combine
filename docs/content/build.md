---
title: Build steps
description: Define build steps for compiling assets for your static site.
---

# Build steps

Modern sites often come with build or compile steps for CSS and JavaScript.

Combine supports these workflows by automatically running additional commands after the regular build process.

After you install your JS dependencies or whatever you need,
add the commands to your `combine.yml`:

```yaml
steps:
  - run: "./node_modules/.bin/tailwind build ./content/assets/_main.css -o ./output/assets/main.css"
    watch:
      - "./tailwind.config.js"
      - "./content/assets/_main.css"
  - run: "./node_modules/.bin/pitchfork index output -c .content"
  - run: "./node_modules/.bin/parcel build theme/content/assets/_main.js --out-dir output/assets --out-file main.js"
    watch: ["./content/assets/_main.js"]
```

All of the steps are run when your *entire* site is built.
Individual steps can be run automatically when certain files are edited,
by using the `watch` field.

Note that these custom steps are run *after* combine has rendered the rest of your site.
So when you are generating output,
you are the one responsible for putting it in the end location you want it (i.e. `./output/css/main.css`).
This keeps the generated/compiled files out of your `content` directory which is tracked in git.

As you can see in the example,
you'll often want to combine this with the [ignored files](/ignore/) feature to keep the source files out of your final build.
