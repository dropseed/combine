# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet.

## [2.1.2] - 2021-04-26

- Ignore sms:// in link checking
- Update python-frontmatter to ^1.0.1

## [2.1.1] - 2021-01-25

- Change file size math and add current size to output
- Strip whitespace when checking broken internal links
- Remove query string parameters when checking broken internal links

## [2.1.0] - 2021-01-22

Add open graph, page title, meta description, image size, and internal broken link checks.

## [2.0.1] - 2021-01-19

Make `combine build --check` exit 1 if there are issues.

## [2.0.0] - 2021-01-19

- Start implementation of "checks"
  - img alt text check
  - duplicate IDs check
  - HTTPS mixed content check
  - favicon.ico check
- Smarter rebuilding of site in `combine work` due to understanding relationships between templates
- Always ignore "node_modules", ".venv", ".cache", and "venv" in `combine work` file watching
- Cleaner `combine work` output

## [1.0.1] - 2021-01-06

Require importlib-metadata and typing_extensions directly if Python < 3.8.

## [1.0.0] - 2020-12-24

Combine has been in use on production sites for a while now, so we might as well act like it!

[Unreleased]: https://github.com/dropseed/combine/compare/2.1.2...HEAD
[2.1.2]: https://github.com/dropseed/combine/releases/tag/2.1.2
[2.1.1]: https://github.com/dropseed/combine/releases/tag/2.1.1
[2.1.0]: https://github.com/dropseed/combine/releases/tag/2.1.0
[2.0.1]: https://github.com/dropseed/combine/releases/tag/2.0.1
[2.0.0]: https://github.com/dropseed/combine/releases/tag/2.0.0
[1.0.1]: https://github.com/dropseed/combine/releases/tag/1.0.1
[1.0.0]: https://github.com/dropseed/combine/releases/tag/1.0.0
