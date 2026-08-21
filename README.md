# She's the Goose

The production website for **shesthegoose.com** — home, kitchen, table and garden,
with The Quiet Ledger (the letters) as its journal.

This is a fully static site. No database, no server code, no build step required
to deploy. Everything a browser needs is inside the `site/` folder.

---

## Repository structure

```
shes-the-goose/          ← repository root (this folder)
├── README.md            ← this file
├── netlify.toml         ← Netlify configuration (publish folder, caching)
├── .gitignore
├── site/                ← THE WEBSITE. This folder is what gets deployed.
│   ├── index.html            homepage
│   ├── kitchen.html          Kitchen
│   ├── table.html            Table
│   ├── garden.html           Garden
│   ├── the-edit.html         The Edit (products / affiliate links)
│   ├── recipes.html          Recipes landing
│   ├── recipes/              one page per recipe (13 pages)
│   ├── letters/              The Quiet Ledger: index.html + 16 letter pages
│   ├── about.html            About
│   ├── search.html           Search (works entirely in the browser)
│   ├── 404.html              "page not found" page (Netlify serves it automatically)
│   ├── sitemap.xml           for search engines
│   ├── robots.txt            for search engines
│   ├── _redirects            thequietledger.co → shesthegoose.com forwarding
│   ├── css/style.css         the entire design system, one file
│   ├── js/site.js            menu, condensed header, search, newsletter thank-you
│   ├── fonts/                Bodoni Moda, Spectral, Archivo (self-hosted woff2)
│   └── images/               every photograph, pre-cropped and compressed
└── src/                 ← THE GENERATOR (optional, for larger updates)
    ├── build_site.py         rebuilds every page in site/ from the content files
    ├── content_letters.py    all 16 letters as structured text
    ├── content_recipes.py    all 13 recipes + Edit products as structured text
    ├── kitchen.body.html     ┐
    ├── table.body.html       ├ page-body templates used by the generator
    └── garden.body.html      ┘
```

**The repository root is this folder (`shes-the-goose/`).**
When you create the GitHub repository, its top level should contain
`README.md`, `netlify.toml`, `site/` and `src/` — exactly as laid out above.

---

## Deploying to Netlify (first time)

1. Push this repository to GitHub.
2. At netlify.com: **Add new site → Import an existing project → GitHub** →
   pick this repository.
3. Netlify reads `netlify.toml` automatically. Build command: none.
   Publish directory: `site`. Click **Deploy**.
4. Under **Domain management**, add `shesthegoose.com` (and `www.shesthegoose.com`)
   and follow Netlify's DNS instructions at your domain registrar.
5. **For the redirect from the old letters site:** also add `thequietledger.co`
   (and `www.thequietledger.co`) as domain aliases on this same Netlify site.
   The rules in `site/_redirects` then forward every old Quiet Ledger URL —
   each letter, each recipe, the philosophy page — to its new home on
   shesthegoose.com, permanently (301).

No step above requires touching the code.

---

## Making updates

### Small text change (one page)
Edit the page's HTML file in `site/` directly, commit, push. Netlify redeploys
automatically. The pages are plain, readable HTML.

### Adding or editing a letter or recipe (recommended path)
The letters and recipes live as structured text in `src/content_letters.py` and
`src/content_recipes.py` — title, ingredients, method steps, notes. To add one:

1. Copy an existing entry in the content file and fill in the new text.
2. From the repository root, run:  `python3 src/build_site.py`
   (needs only Python 3 — no packages to install).
3. Every page in `site/` is regenerated, including indexes, search, prev/next
   links and the sitemap. Commit and push.

The generator never touches `site/images/`, `site/fonts/`, `site/css/`,
`site/js/` or `site/_redirects` — those are yours to manage directly.

### Adding a photograph
1. Export a JPEG at roughly 1,600px on the long edge (quality ~75–80).
2. Drop it in `site/images/`.
3. Point the page at it: either replace an existing filename, or swap a
   "Photograph to come" placeholder block for
   `<img src="images/yourfile.jpg" alt="describe what is in the frame">`.

The placeholder blocks on the site double as the shot list — each names the
photograph it is waiting for.

### The newsletter
The signup forms post to Buttondown (list: `thequietledger`). To change lists,
search `site/` for `buttondown.com` and update the form action — it appears in
the footer of every page and in the letter-page signup blocks.

---

## House rules (the design system, in brief)

Stone `#E8E7E2` · band `#DCDCD1` · ink `#1F1E1A` · oxblood `#6B2B33` (hover only).
Bodoni Moda for the wordmark and display headings, Spectral for reading text and
everything in the letters, Archivo only for small uppercase labels.
No rounded corners, no shadows, no gradients, no filled buttons, no text over
photographs. When in doubt: edit, don't add.

---

## Checks before going live

- [ ] Domain(s) added on Netlify, DNS pointed
- [ ] `thequietledger.co` added as alias so `_redirects` can catch it
- [ ] Send yourself a test email through the footer signup
- [ ] Click a few affiliate links on The Edit
- [ ] Replace placeholder photographs as they are shot
