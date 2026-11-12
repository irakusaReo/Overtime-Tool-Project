# Proxima Nova font files

Every page uses **Proxima Nova**, wired up in `css/fonts.css`. The font is licensed (Mark Simonson Studio / Adobe Fonts), so the files aren't committed to this repo.

Add your organisation's licensed web-font files here, using these exact names:

| Weight | Used for | File |
|---|---|---|
| 400 Regular | Body text, table cells | `ProximaNova-Regular.woff2` |
| 500 Medium | Labels, badges, menu items | `ProximaNova-Medium.woff2` |
| 600 Semibold | Headings, buttons, navigation | `ProximaNova-Semibold.woff2` |
| 700 Bold | Stat values, "CX INTRANET" | `ProximaNova-Bold.woff2` |
| 800 Extrabold | (reserved) | `ProximaNova-Extrabold.woff2` |
| 900 Black | Landing hero ("CX", "CALL CENTRE") | `ProximaNova-Black.woff2` |

If Proxima Nova is installed on the machine, it is used even without these files. For Figma (html.to.design), install Proxima Nova in Figma, or as a desktop font, so the imported layers keep the typeface.

If your organisation uses Adobe Fonts instead, add the kit's `<link>` before `css/fonts.css` in each page's `<head>`. The family name `proxima-nova` should then be added first in `--font-family` in `css/tokens.css`.
