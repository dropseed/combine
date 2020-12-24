# Themes

To re-use layouts and styling across multiple projects,
you can create a theme.

A theme is really nothing more than a separate directory of content which gets *combined* (pun intended) with the content for your current site.

To use a theme,
create `theme` directory next to your `content` directory.
When you build the site, Combine will automatically merge the `theme/content` and `content` directories. To overwrite files from the theme, simply use the same path (i.e. `content/_sidebar.html` will overwrite `theme/content/_sidebar.html`).

## Sharing themes

Because `theme` is just a directory,
a useful way to share it across repos is to use something like [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

## Using other directories

Using a directory named `theme` is a pattern that Combine detects automatically,
but you can change the name or even combine multiple directories by setting the [`content_paths`](/config/content-paths/).
