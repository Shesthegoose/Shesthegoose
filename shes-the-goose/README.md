# She's the Goose

The production website for **shesthegoose.com** — home, kitchen, table and garden,
with The Quiet Ledger (the letters) as its journal.

This is a fully static site. **The website lives at the repository root** — the
`index.html` you see at the top level of this repository is the homepage, and the
`css/`, `js/`, `fonts/` and `images/` folders beside it are the assets every page
points to. Keep them together and nothing can break.

---

## Repository structure

```
(repository root)
├── index.html           homepage
├── kitchen.html         Kitchen
├── table.html           Table
├── garden.html          Garden
├── the-edit.html        The Edit (products / affiliate links)
├── recipes.html         Recipes landing
├── recipes/             one page per recipe (13 pages)
├── letters/             The Quiet Ledger: index.html + 16 letter pages
├── about.html           About
├── search.html          Search (works entirely in the browser)
├── 404.html             "page not found" (Netlify serves it automatically)
├── sitemap.xml          for search engines
├── robots.txt           for search engines
├── _redirects           thequietledger.co → shesthegoose.com forwarding
├── css/style.css        the entire design system, one file
├── js/site.js           menu, condensed header, search, newsletter thank-you
├── fonts/               Bodoni Moda, Spectral, Archivo (self-hosted)
├── images/              every photograph, pre-cropped and compressed
├── netlify.toml         Netlify configuration (publish = ".", the root)
├── src/                 the generator (optional, for larger updates)
└── README.md            this file
```

**Important:** the HTML pages find their styling at `css/style.css` *relative to
themselves*. That works because `css/` sits at the repository root next to
`index.html`. If files are ever rearranged so that `css/` is somewhere else,
the site will render unstyled — the fix is always to restore this exact layout,
never to edit the paths inside the pages.

---

## Replacing the current repository contents (fixing an unstyled deploy)

If the site is live but unstyled, the files on GitHub don't match this layout.
The clean fix:

1. In your GitHub repository, delete the old files (or start a fresh repository).
2. Upload **everything inside this package's folder** so that `index.html`,
   `css/`, `netlify.toml` etc. sit at the **top level** of the repository —
   not inside any wrapping folder.
3. In Netlify: **Site configuration → Build & deploy → Build settings** —
   set **Publish directory** to blank or `.` (the repository root), and
   **Build command** to blank. (The `netlify.toml` in this package sets this
   automatically for new deploys, but check the dashboard hasn't overridden it.)
4. Netlify redeploys on push. Hard-refresh the site (Cmd+Shift+R) to bypass
   your browser's cached unstyled version.

A correct deploy shows the "She's the Goose" wordmark in the tall serif
(Bodoni) on a warm stone background. If you see plain black text on white,
the publish directory or folder layout is still off.

---

## Deploying to Netlify (first time)

1. Push this repository to GitHub.
2. netlify.com → **Add new site → Import an existing project → GitHub** → pick
   this repository. Build command: none. Publish directory: `.` (the root).
3. **Domain management** → add `shesthegoose.com` and `www.shesthegoose.com`,
   follow Netlify's DNS instructions at your registrar.
4. Also add `thequietledger.co` and `www.thequietledger.co` as aliases on this
   same site — the rules in `_redirects` then forward every old Quiet Ledger
   URL (each letter, each recipe, the philosophy page) to its new home, 301.

---

## Making updates

### Small text change (one page)
Edit the page's HTML file directly, commit, push. Netlify redeploys
automatically. The pages are plain, readable HTML.

### Adding or editing a letter or recipe (recommended path)
Letters and recipes live as structured text in `src/content_letters.py` and
`src/content_recipes.py`. To add one:

1. Copy an existing entry in the content file and fill in the new text.
2. From the repository root run:  `python3 src/build_site.py`
   (needs only Python 3 — nothing to install).
3. Every page is regenerated — indexes, search, prev/next links, sitemap.
   Commit and push.

The generator never touches `images/`, `fonts/`, `css/`, `js/` or
`_redirects` — those are yours to manage directly.

### Adding a photograph
1. Export a JPEG at roughly 1,600px on the long edge (quality ~75–80).
2. Drop it in `images/`.
3. Replace an existing filename, or swap a "Photograph to come" placeholder
   block for `<img src="images/yourfile.jpg" alt="describe the frame">`.
   The placeholder blocks double as the shot list.

### The newsletter
Signup forms post to Buttondown (list `thequietledger`). To change lists,
search the repository for `buttondown.com` and update the form action.

---

## House rules (the design system, in brief)

Stone `#E8E7E2` · band `#DCDCD1` · ink `#1F1E1A` · oxblood `#6B2B33` (hover only).
Bodoni Moda for the wordmark and display headings, Spectral for reading text and
the letters, Archivo only for small uppercase labels. No rounded corners, no
shadows, no gradients, no filled buttons, no text over photographs.
When in doubt: edit, don't add.
