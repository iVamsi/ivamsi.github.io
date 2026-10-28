# Vamsi’s portfolio

A single-page portfolio at https://ivamsi.github.io, built with semantic HTML and CSS. No build step or runtime JavaScript is required.

## Preview

From the repository root, run `python3 -m http.server 8000`, then open http://localhost:8000. Open `/404.html` directly to preview the error page; Python’s basic server does not route missing requests through that document.

## Update content

Edit `index.html` for copy and links, `styles.css` for presentation, and `assets/` for diagrams and fonts. Keep the stable `libraries`, `work`, `expertise`, `about`, and `contact` anchors. Update the social preview image and metadata when changing the site’s positioning.

Fonts are locally hosted DM Sans and DM Serif Display from Google Fonts. Their SIL Open Font Licenses are included in `assets/fonts/`.

## Content sources

Professional background and writing/contact links: https://github.com/iVamsi/ivamsi/blob/main/README.md

Project and library descriptions:

- https://github.com/iVamsi/SnapNotify/blob/main/README.md
- https://github.com/iVamsi/EasyAndroidPermissions/blob/main/README.md
- https://github.com/iVamsi/ShrinkGuard/blob/main/README.md

Descriptions cover documented functionality. They do not claim user counts, measured impact, employment history, or production adoption. Review these sources when updating project copy.

## Check and publish

Run `python3 tests/check_site.py`. Preview at 320, 390, 768, and 1440 pixels, test keyboard navigation and zoom, then run a mobile Lighthouse audit. Check project and social links. The homepage must remain usable without JavaScript.

GitHub Pages publishes the root of `master`, with HTTPS enforced. Merge the reviewed change to publish; watch the Pages build and verify the public homepage, metadata, error page, and existing API endpoint. Revert the release commit to roll back.

`WorldCountriesAPI/api/all/index.json` is an existing public endpoint. Preserve it byte-for-byte and keep its URL unchanged.

Library recognition: SnapNotify appears in [Android Weekly #692](https://androidweekly.net/issues/issue-692); EasyAndroidPermissions appears in [Android Weekly #694](https://androidweekly.net/issues/issue-694).
