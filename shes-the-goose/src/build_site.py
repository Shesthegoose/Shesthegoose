#!/usr/bin/env python3
# She's the Goose — static site generator
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_letters import LETTERS
from content_recipes import RECIPES, SUPPERS, EDIT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ROOT  # pages live at the repository root
TOPLINK = '\n  <div class="measure toplink"><a class="rulelink" href="#top">Back to top<span class="arw">&uarr;</span></a></div>\n'
NAV = [("Home","index.html"),("Kitchen","kitchen.html"),("Table","table.html"),
       ("Garden","garden.html"),("The Edit","the-edit.html"),("Recipes","recipes.html"),
       ("About","about.html"),("Search","search.html")]

def header(active, p=""):
    items = "".join(
        f'<li><a href="{p}{href}" class="{"on" if name==active else ""}">{name}</a></li>'
        for name,href in NAV)
    m_depts = "".join(f'<a href="{p}{h}">{n}</a>' for n,h in NAV[1:4])
    citems  = "".join(f'<a href="{p}{h}">{n}</a>' for n,h in NAV[1:])
    m_more  = "".join(f'<a href="{p}{h}">{n}</a>' for n,h in NAV[4:])
    return f"""<div class="page" id="top">
  <div class="strip">
    <span>Late Summer</span>
    <span><a href="{p}letters/index.html">Letters &mdash; the journal</a></span>
  </div>
  <header class="masthead">
    <a href="{p}index.html"><p class="wordmark">She&rsquo;s the Goose</p></a>
  </header>
  <nav class="nav" aria-label="Primary">
    <ul>{items}</ul>
    <div class="nav-mobile">
      <button type="button" onclick="document.getElementById('menu').classList.add('open')">Menu</button>
      <a href="{p}search.html">Search</a>
    </div>
  </nav>
  <div class="condensed" id="condensed" aria-hidden="true">
    <a href="{p}index.html" class="c-name">She&rsquo;s the Goose</a>
    <nav class="c-nav" aria-label="Condensed">{citems}</nav>
    <button class="c-menu" type="button" onclick="document.getElementById('menu').classList.add('open')">Menu</button>
  </div>
  <div class="menu-overlay" id="menu">
    <div class="m-top">
      <span class="eyebrow">She&rsquo;s the Goose</span>
      <button class="m-close" type="button" onclick="document.getElementById('menu').classList.remove('open')">Close</button>
    </div>
    <div class="grp"><a href="{p}index.html">Home</a>{m_depts}{m_more}<a href="{p}letters/index.html">Letters</a></div>
  </div>
"""

def signup(p=""):
    return f"""<form class="signup" action="https://buttondown.com/api/emails/embed-subscribe/thequietledger" method="post" target="bd-frame" onsubmit="bdThanks(this)">
            <input type="email" name="email" aria-label="Email address" placeholder="Your email" autocomplete="email" required>
            <button type="submit">Subscribe</button>
          </form>
          <iframe name="bd-frame" class="bd-frame" tabindex="-1" aria-hidden="true"></iframe>"""

def footer(p=""):
    links = "".join(f'<a href="{p}{h}">{n}</a>' for n,h in NAV[1:])
    return f"""  <footer class="foot2">
    <div class="measure">
      <div class="top">
        <p class="fm">She&rsquo;s the Goose</p>
        <div class="sg">
          <h4>Letters from She&rsquo;s the Goose</h4>
          <p class="cap" style="margin-top:0">One letter, now and then. No noise, no selling.</p>
          {signup(p)}
          <p class="thanks" id="bdThanksMsg" style="display:none;font-family:var(--text);font-style:italic;font-weight:300;font-size:.85rem;color:var(--ink-soft);margin:.9rem 0 0">Thank you &mdash; look for a note to confirm.</p>
        </div>
      </div>
      <div class="links"><a href="{p}letters/index.html">Letters</a>{links}</div>
      <div class="base">
        <span>&copy; 2026 She&rsquo;s the Goose</span>
        <span>As an Amazon Associate, She&rsquo;s the Goose earns from qualifying purchases.</span>
      </div>
    </div>
  </footer>
</div>
<script src="{p}js/site.js"></script>"""

def page(fname, title, active, body, p="", desc="", bodyclass="", ogimg="images/hero.jpg"):
    canon = "" if fname=="index.html" else fname
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{html.escape(desc) if desc else 'She’s the Goose — home, kitchen, table and garden, done well.'}">
<link rel="canonical" href="https://shesthegoose.com/{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc) if desc else 'She’s the Goose — home, kitchen, table and garden, done well.'}">
<meta property="og:image" content="https://shesthegoose.com/{ogimg}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23E8E7E2'/%3E%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='38' text-anchor='middle' fill='%231F1E1A'%3EG%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{p}css/style.css">
</head>
<body class="{bodyclass}">
{header(active,p)}{body}
{footer(p)}
</body>
</html>"""
    path = os.path.join(SITE, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(doc)
    print("wrote", fname, len(doc)//1024, "KB")

# ---------------------------------------------------------------- homepage
def build_home():
    lead = next(l for l in LETTERS if l["no"]==16)
    s15  = next(l for l in LETTERS if l["no"]==15)
    s14  = next(l for l in LETTERS if l["no"]==14)
    body = f"""
  <section class="hero-home">
    <div class="hero-type">
      <div class="hero-type-inner">
        <p class="eyebrow">August &middot; Gathering</p>
        <h1 class="hero-head">A table set for the last of the summer fruit.</h1>
        <p class="stand hero-stand">Figs, late grapes, the good cheese unwrapped an hour early. A board like this one is less about cooking than about deciding an ordinary Thursday is worth stopping for &mdash; and then setting the table as though you meant it.</p>
        <a class="rulelink" href="the-edit.html">Set the table<span class="arw">&rarr;</span></a>
      </div>
      <p class="hero-credit">Photographed at home. Aged cheddar and havarti, black figs, red grapes, garden chrysanthemum and eucalyptus.</p>
    </div>
    <figure class="hero-figure">
      <img src="images/hero.jpg" alt="An overhead grazing board of cheeses, cured meats, figs, grapes and pears, ringed with eucalyptus and pink chrysanthemum on pale stone.">
    </figure>
  </section>

  <section class="home-ledger">
    <div class="measure">
      <div class="intro">
        <p class="eyebrow">The journal of She&rsquo;s the Goose</p>
        <div class="markline"><span class="r"></span><p class="mark">The Quiet Ledger</p><span class="r"></span></div>
        <p class="tagline-l">A record of ordinary moments, kept on purpose.</p>
        <p class="note">One letter each week, written slowly.</p>
      </div>
      <div class="home-letters">
        <article class="lead-l">
          <a href="letters/letter-16.html">
            <img src="images/letter-16.jpg" alt="A quiet tree-lined road in full summer leaf, a yellow centre line running away into shade.">
            <p class="eyebrow">Letter no. 16 &middot; Summer</p>
            <h3 class="lt-title">{lead["title"]}</h3>
            <p class="lt-x">{lead["excerpt"]}</p>
            <span class="rulelink" style="margin-top:1.35rem">Read the letter<span class="arw">&rarr;</span></span>
          </a>
        </article>
        <div class="stack-l">
          <article><a href="letters/letter-15.html">
            <img src="images/letter-15.jpg" alt="A rocky New England coastline under a clear sky.">
            <div>
              <p class="eyebrow">Letter no. 15 &middot; Summer</p>
              <h3 class="lt-title">{s15["title"]}</h3>
              <p class="lt-x">{s15["excerpt"]}</p>
            </div>
          </a></article>
          <article><a href="letters/letter-14.html">
            <img src="images/k_led.jpg" alt="A roasted salmon fillet on a charred cedar plank set on a rope trivet.">
            <div>
              <p class="eyebrow">Letter no. 14 &middot; Summer</p>
              <h3 class="lt-title">{s14["title"]}</h3>
              <p class="lt-x">{s14["excerpt"]}</p>
            </div>
          </a></article>
        </div>
      </div>
      <div class="foot-l">
        <span class="eyebrow">Sixteen letters and counting</span>
        <a class="rulelink" href="letters/index.html">Read the journal<span class="arw">&rarr;</span></a>
      </div>
    </div>
  </section>

  <section class="home-depts measure">
    <div class="row3">
      <a class="d-k" href="kitchen.html">
        <img src="images/dept-kitchen.jpg" alt="A peach galette on a green leaf-pattern plate, seen from above.">
        <h3>Kitchen</h3>
        <p class="b">What we actually cook, and how to cook it well enough to make again.</p>
      </a>
      <a class="d-t" href="table.html">
        <img src="images/dept-table.jpg" alt="Lit taper candles rising from a runner of peonies, dahlias and autumn foliage.">
        <h3>Table</h3>
        <p class="b">How the table gets set, what goes on it, and who it gets set for.</p>
      </a>
      <a class="d-g" href="garden.html">
        <img src="images/dept-garden.jpg" alt="Hands lowering a hyacinth into dark spring soil beside a stone edge.">
        <h3>Garden</h3>
        <p class="b">What is happening outside, month by month, in one ordinary garden.</p>
      </a>
    </div>
  </section>

  <section class="breather">
    <img src="images/breather.jpg" alt="A long dinner table lit with white tapers, peonies and dahlias running down the centre, a botanical plate at each setting.">
    <div class="measure"><p class="cap" style="max-width:56ch">The long table, lit and waiting. Set in the afternoon, so the evening only has to arrive.</p></div>
  </section>

  <section class="home-recipes measure">
    <div class="home-edit" style="padding-top:0"><div class="head" style="padding-bottom:0">
      <div><p class="eyebrow">From the kitchen</p>
      <h2 style="font-family:var(--text);font-weight:400">Recipes</h2></div>
      <a class="rulelink" href="recipes.html">All recipes<span class="arw">&rarr;</span></a>
    </div></div>
    <div class="grid" style="margin-top:clamp(1.5rem,3vw,2.25rem)">
      <article class="lead-r"><a href="recipes/lemon-sugar-cookies.html">
        <img src="images/home-recipes-lead.jpg" alt="Iced lemon sugar cookies on a green plate with eucalyptus and lemon slices.">
        <p class="eyebrow" style="margin-top:1rem">From the Oven &middot; Every season</p>
        <h3 class="lt-title">Soft Lemon Sugar Cookies</h3>
        <p class="lt-x">Zest rubbed into the sugar by hand, soft centers left pale, and a thin lemon glaze. Better on the second day than the first.</p>
        <p class="meta" style="margin-top:1rem">350&deg;F &middot; Makes 24</p>
      </a></article>
      <div class="idx">
        <a href="recipes/pie-crust.html"><span class="t">The Pie Crust</span><span class="m">Basic Series</span></a>
        <a href="recipes/cherry-pie.html"><span class="t">The Cherry Pie That Started It All</span><span class="m">1 hr</span></a>
        <a href="recipes/chocolate-chip-cookies.html"><span class="t">Bakery-Style Chocolate Chip Cookies</span><span class="m">18 large</span></a>
        <a href="recipes/brown-butter-snickerdoodles.html"><span class="t">Brown Butter Snickerdoodles</span><span class="m">Makes 24</span></a>
      </div>
      <p style="margin:1.6rem 0 0;grid-column:2"><a class="rulelink" href="recipes.html">The three collections<span class="arw">&rarr;</span></a></p>
    </div>
  </section>

  <section class="home-edit measure">
    <div class="head">
      <div>
        <p class="eyebrow">Curated</p>
        <h2>The Edit</h2>
        <p class="body" style="max-width:52ch">Nothing is listed unless it has lived in this house and earned its place &mdash; used, kept, and quietly returned to.</p>
      </div>
      <a class="rulelink" href="the-edit.html">See the full Edit<span class="arw">&rarr;</span></a>
    </div>
    <div class="cats">
      <a href="the-edit.html#table"><h3>The Table</h3><p>Chargers, tapers, and the pieces that anchor a setting.</p></a>
      <a href="the-edit.html#kitchen"><h3>The Kitchen</h3><p>The tools that cook everything photographed on this site.</p></a>
      <a href="the-edit.html#home"><h3>The Home</h3><p>What makes the house feel like someone lives in it.</p></a>
    </div>
  </section>

  <section class="sunday">
    <div class="inner">
      <p class="eyebrow">Letters from She&rsquo;s the Goose</p>
      <h2>One letter, now and then</h2>
      <p class="b">No noise, no selling &mdash; just the same quiet, delivered when it&rsquo;s written.</p>
      {signup("")}
      <p class="thanks">Thank you &mdash; look for a note to confirm.</p>
    </div>
  </section>
"""
    page("index.html","She’s the Goose","Home",body,"",
         "She’s the Goose — home, kitchen, table and garden, done well. With The Quiet Ledger, a weekly letter on ordinary life.", bodyclass="home")

# ------------------------------------------------------- department pages
def adapt_body(src):
    b = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), src), encoding="utf-8").read()
    b = re.sub(r'src="data:image/jpeg;base64,__([a-z0-9_]+)__"', r'src="images/\1.jpg"', b)
    return b

def build_depts():
    # KITCHEN
    b = adapt_body("kitchen.body.html")
    b = b.replace('<p class="meta">50 min &middot; Serves 6 &middot; The Basic Series</p>',
                  '<p class="meta">Serves 6&ndash;8 &middot; Oven 400&deg;F &middot; From the Oven</p>')
    b = b.replace('<h2>The galette you can make without a recipe.</h2>',
                  '<h2>The galette, unpeeled on purpose.</h2>')
    b = b.replace('<p class="stand">Cold butter, one round of pastry, and whatever fruit is two days from going. It is the only late-summer dessert worth turning the oven on for, and it forgives nearly everything &mdash; a crooked fold, too much juice, an oven that runs hot.</p>',
                  '<p class="stand">Cold butter, one round of pastry, and a hidden layer of ground almonds doing quiet work underneath the fruit. It forgives nearly everything &mdash; a crooked fold, too much juice, an oven that runs hot &mdash; and the skins stay on, because they should.</p>')
    b = b.replace('<p style="margin:1.6rem 0 0"><a class="rulelink" href="#">Read the method<span class="arw">&rarr;</span></a></p>',
                  '<p style="margin:1.6rem 0 0"><a class="rulelink" href="recipes/peach-galette.html">Read the recipe<span class="arw">&rarr;</span></a></p>')
    # river item fixes — real recipes and links
    b = b.replace('<h3>Cedar-Plank Salmon</h3>','<h3>Cedar-Plank Salmon with Fresh Thyme</h3>')
    b = b.replace('<p class="eyebrow">Suppers</p>\n          <h3>Cedar-Plank','<p class="eyebrow">Suppers</p>\n          <h3>Cedar-Plank')
    b = b.replace('<p class="meta">30 min &middot; Serves 4</p>','<p class="meta">Suppers &middot; About 1 hr with the soak</p>')
    b = b.replace('<p class="eyebrow">The Basic Series</p>\n          <h3>Blueberry Crumb Cake</h3>',
                  '<p class="eyebrow">From the Oven</p>\n          <h3>Blueberry Crumb Cake</h3>')
    b = b.replace('<p class="meta">1 hr &middot; Serves 8</p>','<p class="meta">55&ndash;65 min &middot; Serves 8&ndash;10</p>')
    b = b.replace('<p class="body">A one-bowl cake with more crumb than cake, which is the correct ratio. It keeps three days on the counter and is better on the second.</p>',
                  '<p class="body">Berries layered through the middle, sour cream keeping the cake tender, and big brown-sugar crumbs on top &mdash; the pieces left deliberately large.</p>')
    b = b.replace('<p class="eyebrow">The Basic Series</p>\n          <h3>Lemon Shortbread, Iced</h3>',
                  '<p class="eyebrow">From the Oven</p>\n          <h3>Soft Lemon Sugar Cookies</h3>')
    b = b.replace('<p class="body">Three ingredients and a lemon. The icing is technically optional, and you should not treat it as optional.</p>',
                  '<p class="body">Zest rubbed into the sugar by hand, soft centers left pale, and a thin lemon glaze. Better on the second day.</p>')
    b = b.replace('<p class="meta">40 min &middot; Makes 18</p>','<p class="meta">350&deg;F &middot; Makes 24</p>')
    b = b.replace('<p class="eyebrow">The Cookie Tin</p>\n          <h3>Cranberry and White Chocolate</h3>',
                  '<p class="eyebrow">From the Oven</p>\n          <h3>Raspberry White Chocolate Cookies</h3>')
    b = b.replace('<p class="body">The one that gets requested. Chill the dough overnight &mdash; that is the entire trick, and skipping it is why most versions spread flat.</p>',
                  '<p class="body">Freeze-dried raspberries folded in whole, so the flecks stay bright pink through the oven. Crisp at the edge, soft in the middle.</p>')
    b = b.replace('<p class="meta">45 min &middot; Makes 24</p>','<p class="meta">350&deg;F &middot; Makes 24</p>')
    # wire river links in order: salmon, crumb cake, lemon, raspberry
    targets = ['recipes.html#suppers','recipes/blueberry-crumb-cake.html','recipes/lemon-sugar-cookies.html','recipes/raspberry-white-chocolate-cookies.html']
    parts = b.split('<a href="#" style="display:contents">')
    out = parts[0]
    for i,part in enumerate(parts[1:]):
        link = targets[i] if i < len(targets) else 'recipes.html'
        out += f'<a href="{link}" style="display:contents">' + part
    b = out
    # Basic Series index → real
    b = re.sub(r'<ol>.*?</ol>', """<ol>
      <li><a href="recipes/pie-crust.html"><span class="n">I</span><span class="t">The Pie Crust</span><span class="d">One bowl, cold butter, a little patience while it chills. The first thing worth learning by heart.</span></a></li>
      <li><a href="recipes/basil-pesto.html"><span class="n">II</span><span class="t">Classic Basil Pesto</span><span class="d">Summer basil, toasted pine nuts, garlic, and good cheese, loosened with olive oil.</span></a></li>
    </ol>
    <p class="cap" style="margin-top:1.5rem;max-width:56ch">More foundations are joining the series &mdash; a good stock, the everyday vinaigrette, a loaf of bread, the puff pastry worth the trouble. Added slowly, as they&rsquo;re written.</p>""", b, count=1, flags=re.S)
    b = b.replace('<h2>Eight foundations.</h2>','<h2>The foundations.</h2>')
    b = b.replace('<p class="body">Learn these and most other recipes stop being recipes and start being variations. No photographs here on purpose &mdash; these are methods, not dishes.</p>',
                  '<p class="body">The building blocks &mdash; the foundations you make once and reach for again, the quiet groundwork beneath the rest of the kitchen.</p>')
    b = b.replace('<a class="rulelink" href="#">All thirty-one<span class="arw">&rarr;</span></a>',
                  '<a class="rulelink" href="recipes.html">The Basic Series<span class="arw">&rarr;</span></a>')
    # Ledger module → Letter 14 (Cooking Outside)
    b = b.replace('<p class="eyebrow">Letter no. 7</p>','<p class="eyebrow">Letter no. 14 &middot; Summer</p>')
    b = b.replace('<h3>The Pot on the Stove</h3>','<h3>Cooking Outside</h3>')
    b = b.replace('<p class="body">Something cooking all afternoon is a way of saying, without saying it, that you intend to be home. The kitchen is the only room that keeps announcing itself &mdash; you can be three rooms away and still know exactly what stage dinner is at.</p>',
                  '<p class="body">The cedar plank sits in the sink for about an hour before dinner. It always wants to float, so I put a bowl on top of it and leave it alone. That&rsquo;s about all there is to it.</p>')
    b = b.replace('<div class="unit">\n        <a href="#" style="display:contents">','<div class="unit">\n        <a href="letters/letter-14.html" style="display:contents">')
    b += TOPLINK
    page("kitchen.html","Kitchen — She’s the Goose","Kitchen",b,"",
         "Kitchen — what we cook, in season, with the Basic Series foundations and the recipes behind it.")

    # TABLE
    b = adapt_body("table.body.html")
    b = b.replace('<a class="rulelink" href="#">See how it was set<span class="arw">&rarr;</span></a>',
                  '<a class="rulelink" href="the-edit.html#table">What the table is set with<span class="arw">&rarr;</span></a>')
    b = b.replace('<a class="rulelink" href="#">Read the piece<span class="arw">&rarr;</span></a>','')
    b = b.replace('''<span>
          <img src="images/t_g5.jpg" alt="A grazing board of cheeses, cured meats, figs and grapes ringed with eucalyptus and chrysanthemum.">
        </span>
        <p class="cap">The board, built on a tray so it can be carried out whole and carried back the same way.</p>''',
'''<div class="ph r45"><span class="pl">Photograph to come</span><span class="ps">The table set for evening, before anyone sits down</span></div>
        <p class="cap">The evening setting &mdash; still to be photographed.</p>''')
    b = b.replace('<h3>The One-Vase Rule</h3>','')
    b = b.replace('<h3>Light It Like a Restaurant</h3>','')
    b = b.replace('<a class="rulelink" href="#">Build the board<span class="arw">&rarr;</span></a>',
                  '<a class="rulelink" href="the-edit.html#table">The Table, in The Edit<span class="arw">&rarr;</span></a>')
    b = b.replace('<a href="#">\n          <img src="images/t_g1','<a href="the-edit.html#table">\n          <img src="images/t_g1')
    b = re.sub(r'<a href="#">(\s*<img)', r'<span>\1', b)
    b = re.sub(r'</a>(\s*<p class="cap">)', r'</span>\1', b)
    # fix titled figures whose <a> became <span>: h3 inside span is fine (no dead links)
    b += TOPLINK
    page("table.html","Table — She’s the Goose","Table",b,"",
         "Table — settings, centerpieces, candlelight and gathering.")

    # GARDEN
    b = adapt_body("garden.body.html")
    b = b.replace('<p class="eyebrow">Letter no. 9</p>','<p class="eyebrow">Letter no. 13 &middot; Summer</p>')
    b = b.replace('<h3>Walking in Cold Air</h3>','<h3>The Long Light</h3>')
    b = b.replace('<p class="body">You go out for the air and come back with the whole morning still in your coat. There is a particular kind of thinking that only happens at walking pace, outdoors, with no destination and nothing to carry.</p>',
                  '<p class="body">It was almost nine last night and still light out. I checked the clock twice because it didn&rsquo;t seem possible. The dishes were in the sink where I&rsquo;d left them. I sat down on the back step instead and never did go in.</p>')
    b = b.replace('''<div class="unit">
        <a href="#" style="display:contents">
          <figure class="fig" style="margin:0">
            <img src="images/g_led.jpg" alt="A rocky New England coastline under a clear sky, waves breaking over dark stone.">
          </figure>
          <div>''','''<div class="unit solo">
        <a href="letters/letter-13.html" style="display:contents">
          <div>''')
    b += TOPLINK
    page("garden.html","Garden — She’s the Goose","Garden",b,"",
         "The Garden — one ordinary New England garden, season by season.")

def build_edit():
    coll_html = ""
    flip = False
    for c in EDIT:
        items = "".join(
            f'<li><a href="{url}" target="_blank" rel="sponsored noopener"><span class="n">{i+1:02d}</span><span class="nm">{html.escape(n)}</span><span class="rs">{html.escape(d)}&ensp;<span style="font-family:var(--utility);font-size:.58rem;letter-spacing:.16em;text-transform:uppercase">View&nbsp;&rarr;</span></span></a></li>'
            for i,(n,d,url) in enumerate(c["items"]))
        cls = "editcol flip" if flip else "editcol"
        coll_html += f"""
    <section class="{cls}" id="{c['key']}">
      <figure class="fig">
        <img src="images/{c['img']}" alt="{html.escape(c['cap'])}">
        <p class="cap">{c['cap']}</p>
      </figure>
      <div>
        <h2>{c['title']}</h2>
        <p class="body">{c['body']}</p>
        <ol class="items">{items}</ol>
      </div>
    </section>"""
        flip = not flip
    body = f"""
  <section class="edit-head measure">
    <h1>The Edit</h1>
    <p class="stand">Nothing is listed here unless it has earned a place in my own home &mdash; used, kept, and quietly returned to. No brand pays to appear.</p>
    <p class="disclose">As an Amazon Associate, She&rsquo;s the Goose earns from qualifying purchases. Every item is chosen first and linked afterwards.</p>
  </section>
  <div class="measure"><div class="dept-rule"></div></div>

  <div class="edits measure">{coll_html}
  </div>
{TOPLINK}"""
    page("the-edit.html","The Edit — She’s the Goose","The Edit",body,"",
         "The Edit — a short, honest list of the pieces that have earned a place in this house.")

# ---------------------------------------------------------------- recipes
def build_recipes():
    oven = [r for r in RECIPES if r["coll"]=="From the Oven"]
    basics = [r for r in RECIPES if r["coll"]=="The Basic Series"]
    oven_sorted = [r for r in oven if r["img"]] + [r for r in oven if not r["img"]]
    cards = ""
    for r in oven_sorted:
        if r["img"]:
            visual = f'<img src="images/{r["img"]}" alt="{html.escape(r["title"])}">'
        else:
            visual = f'<div class="ph r45"><span class="pl">Photograph to come</span><span class="ps">{html.escape(r["title"])}</span></div>'
        cards += f"""<article class="rcard"><a href="recipes/{r['slug']}.html">
        {visual}
        <p class="eyebrow">{r['eyebrow'].split('·')[-1].strip()}</p>
        <h3>{r['title']}</h3>
        <p class="meta">{r['meta'][2] if len(r['meta'])>2 else r['meta'][0]}</p>
      </a></article>"""
    basic_rows = "".join(
        f'<li><a href="recipes/{r["slug"]}.html"><span class="n">{["I","II"][i]}</span><span class="t">{r["title"]}</span><span class="d">{r["dek"]}</span></a></li>'
        for i,r in enumerate(basics))
    supper_rows = "".join(
        f'<li><a href="recipes.html#suppers"><span class="n">{i+1:02d}</span><span class="t">{sup["title"]}</span><span class="d">{sup["desc"]}</span></a></li>'
        for i,sup in enumerate(SUPPERS))
    body = f"""
  <section class="rec-head measure">
    <p class="eyebrow">From the Kitchen</p>
    <h1>Recipes</h1>
    <p class="stand">Recipes and kitchen rituals meant to be lived with, not rushed through. Everything here has been cooked in this kitchen and written down afterwards.</p>
  </section>
  <div class="measure"><div class="dept-rule"></div></div>

  <section class="coll measure" id="oven" style="border-top:0;margin-top:0;padding-top:clamp(2rem,4vw,3.25rem)">
    <div class="coll-head">
      <div>
        <h2>From the Oven</h2>
        <p class="body">Pies and slow baking &mdash; the recipes for unhurried afternoons, kept season to season.</p>
      </div>
    </div>
    <div class="cards cards-3">{cards}</div>
  </section>

  <section class="coll measure" id="basic-series">
    <div class="coll-head">
      <div>
        <h2>The Basic Series</h2>
        <p class="body">The building blocks &mdash; made once, reached for again. No photographs on purpose: these are methods, not dishes.</p>
      </div>
    </div>
    <div class="basic" style="grid-template-columns:1fr">
      <ol style="columns:2">{basic_rows}</ol>
      <p class="cap" style="max-width:60ch">More foundations are joining the series &mdash; a good stock, the everyday vinaigrette, a loaf of bread, the puff pastry worth the trouble. Added slowly, as they&rsquo;re written.</p>
    </div>
  </section>

  <section class="coll measure" id="suppers">
    <div class="coll-head">
      <div>
        <h2>Suppers</h2>
        <p class="body">Something warm for the end of the day. Six summer suppers so far &mdash; full recipe pages are being written now.</p>
      </div>
    </div>
    <div class="suppers" style="grid-template-columns:.8fr 1.2fr">
      <article><span>
        <img src="images/s1.jpg" alt="A roasted salmon fillet on a charred cedar plank set on a woven rope trivet.">
        <p class="cap">Cedar-plank salmon with fresh thyme &mdash; the plank soaks an hour, the honey-Dijon glaze goes on, and the cedar smokes gently while it grills.</p>
      </span></article>
      <div class="index"><ol>{supper_rows}</ol>
      <p class="cap" style="margin-top:1.4rem">Fall and winter suppers will join the table as the year turns.</p></div>
    </div>
  </section>
{TOPLINK}"""
    page("recipes.html","Recipes — She’s the Goose","Recipes",body,"",
         "Recipes from the kitchen at She’s the Goose — pies and slow baking, foundations, and seasonal suppers.")

def build_recipe_pages():
    for idx,r in enumerate(RECIPES):
        prev = RECIPES[idx-1] if idx>0 else RECIPES[-1]
        nxt  = RECIPES[(idx+1)%len(RECIPES)]
        hero = ""
        if r["img"]:
            wide = r["img"].replace(".jpg","-wide.jpg")
            wide = wide if os.path.exists(os.path.join(SITE,"images",wide)) else r["img"]
            hero = f'<figure class="bleed"><img src="../images/{wide}" alt="{html.escape(r["title"])}"></figure>\n'
        ing = ""
        for gname,items in r["ingredients"]:
            lis = "".join(f"<li>{i}</li>" for i in items)
            ing += f'<div class="grp"><p class="gl">{gname}</p><ul>{lis}</ul></div>'
        def stephtml(st):
            if isinstance(st, list):
                return "".join(f'<p style="margin-top:{".6rem" if j else "0"}">{t}</p>' for j,t in enumerate(st))
            return f"<p>{st}</p>"
        steps = "".join(
            f'<li><span class="n">{i+1:02d}</span><div>{stephtml(st)}</div></li>' for i,st in enumerate(r["method"]))
        notes = "".join(f"<p>{n}</p>" for n in r["notes"])
        intro = "".join(f"<p>{p}</p>" for p in r["intro"])
        meta = "".join(f"<span>{m}</span>" for m in r["meta"])
        body = f"""
  {hero}<section class="measure">
    <div class="r-open">
      <a href="../recipes.html"><p class="lockup" style="font-family:'Archivo',sans-serif;font-weight:500;font-size:.6rem;letter-spacing:.24em;text-transform:uppercase;color:#5E5C53;margin:0">{r['eyebrow']}</p></a>
      <h1>{r['title']}</h1>
      <p class="dek">{r['dek']}</p>
      <div class="meta">{meta}</div>
    </div>
    <div class="r-body">{intro}</div>
    <div class="r-split">
      <div class="r-ing"><h2>Ingredients</h2>{ing}</div>
      <div class="r-method"><h2>Method</h2><ol>{steps}</ol></div>
    </div>
  </section>
  <section class="r-notes"><div class="inner"><h2>Notes</h2>{notes}</div></section>
  <section class="measure"><div class="r-nav three">
    <a href="{prev['slug']}.html" class="pv"><p class="eyebrow">Previous recipe</p><h3>{prev['title']}</h3></a>
    <a href="../recipes.html" class="mid"><p class="eyebrow">&nbsp;</p><span class="rulelink">Back to Recipes</span></a>
    <a href="{nxt['slug']}.html" class="nx"><p class="eyebrow">Next recipe</p><h3>{nxt['title']}</h3></a>
  </div></section>
"""
        page(f"recipes/{r['slug']}.html", f"{r['title']} — She’s the Goose","Recipes",body,"../",
             r["dek"], ogimg=("images/"+(r["img"] or "rec-raspberry.jpg")))

# ---------------------------------------------------------------- letters
def build_letters():
    seasons = [("Winter","Letters I – IX",[l for l in LETTERS if l["season"]=="Winter"]),
               ("Spring","Letters X – XII",[l for l in LETTERS if l["season"]=="Spring"]),
               ("Summer","Letters XIII – XVI",[l for l in LETTERS if l["season"]=="Summer"])]
    blocks = ""
    for name,label,ls in seasons:
        rows = "".join(f"""<div class="let-row"><a href="{l['slug']}.html">
          <span class="no">No. {l['no']:02d}</span><span class="t">{l['title']}</span><span class="arr">&rarr;</span>
          <span class="x">{l['excerpt']}</span></a></div>""" for l in ls)
        blocks += f"""
      <section class="season-block">
        <div class="s-head"><h2>{name}</h2><span class="n">{label}</span></div>
        {rows}
      </section>"""
    body = f"""
  <div style="background:var(--band)">
  <section class="let-head measure">
    <p class="eyebrow">The journal of She&rsquo;s the Goose</p>
    <div class="markline"><span class="r"></span><h1>The Quiet Ledger</h1><span class="r"></span></div>
    <p class="tagline-l">A record of ordinary moments, kept on purpose.</p>
    <p class="count">Sixteen letters, one each week</p>
  </section>
  <section class="let-lead measure">
    <img src="../images/letters-lead.jpg" alt="A glass mug of coffee with cinnamon on the counter by a bright window.">
    <p class="cap">The first photograph in the Ledger &mdash; the hour before anyone else wakes.</p>
  </section>
  <div class="measure" style="padding-bottom:clamp(3rem,6vw,5rem)">{blocks}
  <div class="toplink"><a class="rulelink" href="#top">Back to top<span class="arw">&uarr;</span></a></div></div>
  </div>
"""
    page("letters/index.html","The Quiet Ledger — Letters","",body,"../",
         "The Quiet Letters — a weekly record of ordinary moments, kept on purpose. Sixteen letters across the seasons.")

    for idx,l in enumerate(LETTERS):
        prev = LETTERS[idx-1] if idx>0 else None
        nxt  = LETTERS[idx+1] if idx<len(LETTERS)-1 else None
        epi = ""
        if l["epigraph"]:
            epi = f"""<div class="epigraph"><p>&ldquo;{l['epigraph']}&rdquo;<span class="src">{l['source']}</span></p></div>"""
        paras = "".join(f"<p>{p}</p>" for p in l["body"])
        sig = '<div class="letter-sig"><p>Until next week,<br>Jessica</p></div>' if l["signed"] else ""
        pv = f'<a href="{prev["slug"]}.html" class="pv"><p class="eyebrow">Previous &middot; No. {prev["no"]:02d}</p><h3>{prev["title"]}</h3></a>' if prev else '<span></span>'
        nx = f'<a href="{nxt["slug"]}.html" class="nx"><p class="eyebrow">Next &middot; No. {nxt["no"]:02d}</p><h3>{nxt["title"]}</h3></a>' if nxt else '<span></span>'
        body = f"""
  <div style="background:var(--band)">
  <div class="letter-open">
    <p class="eyebrow">{l['season']} Letters &middot; No. {l['no']:02d}</p>
    <h1>{l['title']}</h1>
    <div class="rule-c"></div>
  </div>
  {epi}
  <div class="letter-body">{paras}</div>
  {sig}
  <div class="letter-nav"><div class="grid three">{pv}<a href="index.html" class="mid"><p class="eyebrow">&nbsp;</p><span class="rulelink">All letters</span></a>{nx}</div></div>
  <section class="sunday" style="margin-top:clamp(3rem,6vw,5rem)">
    <div class="inner">
      <p class="eyebrow">Letters from She&rsquo;s the Goose</p>
      <h2>One letter, now and then</h2>
      <p class="b">No noise, no selling &mdash; just the same quiet, delivered when it&rsquo;s written.</p>
      {signup("../")}
      <p class="thanks">Thank you &mdash; look for a note to confirm.</p>
    </div>
  </section>
  </div>
"""
        page(f"letters/{l['slug']}.html", f"{l['title']} — The Quiet Ledger","",body,"../",
             l["excerpt"])

# ---------------------------------------------------------------- about
def build_about():
    body = """
  <section class="about-open measure">
    <img src="images/about.jpg" alt="A round table set for three, white plates on wood chargers, a low arrangement of lilies and delphinium.">
    <div>
      <p class="eyebrow">About</p>
      <h1>A home does not need to be perfect to feel beautiful.</h1>
      <p class="stand">A note from Jessica &mdash; on home, on the things that earn their place, and on why this exists.</p>
    </div>
  </section>
  <div class="measure"><div class="dept-rule"></div></div>

  <div class="about-body">
    <p>A good lamp in the corner. Dinner cooking before the guests arrive. Flowers from the grocery store dropped into a heavy vase. Linens wrinkled from being used often. A kitchen that looks lived in, not staged.</p>
    <p>This is a collection of recipes, objects, gatherings, and details that make everyday life feel warmer, slower, and more intentional. Nothing is shared here unless it has earned a place in my own home &mdash; used, kept, and quietly returned to.</p>
  </div>

  <div class="measure" style="max-width:900px;padding-top:clamp(2.5rem,5vw,4rem)">
    <div class="ph r32"><span class="pl">Photograph to come</span><span class="ps">The kitchen in the morning, as it actually is</span></div>
  </div>

  <div class="pullq"><p>The real adventure is in the small things. The pot of soup on a cold afternoon. The first light through the kitchen window before anyone else is awake. If you rush through those moments, you miss your life.</p></div>

  <div class="about-body">
    <p>The letters began as a private record of small mornings, slow meals, and the kind of thinking that only happens when the house is still. Eventually it felt worth sharing &mdash; not as advice, just as a life lived at a quieter pace.</p>
    <p>My faith is not a footnote here. It is the foundation. This isn&rsquo;t something I feel the need to explain. It is simply what is true.</p>
    <p>Thank you for being here. I hope you find something in these pages that makes you want to slow down &mdash; just a little &mdash; and look more carefully at your own ordinary life.</p>
    <p>It is more beautiful than you think.</p>
    <p class="sig">&mdash; Jessica</p>
  </div>

  <div class="measure" style="max-width:900px;padding-top:clamp(2.5rem,5vw,4rem)">
    <div class="ph r32"><span class="pl">Photograph to come</span><span class="ps">The house, lived in &mdash; a corner that is actually ours</span></div>
  </div>
"""
    page("about.html","About — She’s the Goose","About",body,"",
         "About She’s the Goose — a note from Jessica on home, and on why this exists.")

# ---------------------------------------------------------------- search
def build_search():
    data = []
    for l in LETTERS:
        data.append(dict(k=f"Letter No. {l['no']:02d} · {l['season']}", t=l["title"],
                         x=l["excerpt"], u=f"letters/{l['slug']}.html",
                         b=re.sub(r'<[^>]+>','', " ".join(l["body"]))[:1200]))
    for r in RECIPES:
        data.append(dict(k=f"Recipe · {r['coll']}", t=r["title"], x=r["dek"],
                         u=f"recipes/{r['slug']}.html",
                         b=" ".join(g for _,items in r["ingredients"] for g in items)))
    for sup in SUPPERS:
        data.append(dict(k="Recipe · Suppers", t=sup["title"], x=sup["desc"],
                         u="recipes.html#suppers"))
    for c in EDIT:
        for n,d,u in c["items"]:
            data.append(dict(k=f"The Edit · {c['title']}", t=n, x=d, u=f"the-edit.html#{c['key']}"))
    for n,h in NAV:
        data.append(dict(k="Page", t=n, x="", u=h))
    body = f"""
  <section class="search-head measure">
    <h1>Search She&rsquo;s the Goose</h1>
    <div class="search-bar">
      <input type="search" id="q" placeholder="Letters, recipes, the Edit&hellip;" autofocus autocomplete="off" aria-label="Search">
    </div>
    <div class="results" id="results"></div>
  </section>
  <script>window.SEARCH_DATA = {json.dumps(data)};</script>
"""
    page("search.html","Search — She’s the Goose","Search",body,"",
         "Search letters, recipes, and The Edit.")

# ---------------------------------------------------------------- js
def build_js():
    js = """// She's the Goose — shared behavior
function bdThanks(form){
  var page = form.closest('.sunday, .foot');
  if(page){ var t = page.querySelector('.thanks') || document.getElementById('bdThanksMsg');
    if(t){ t.classList.add('show'); t.style.display='block'; } }
  setTimeout(function(){ var e=form.querySelector('input[type=email]'); if(e) e.value=''; },400);
}
// condensed masthead bar
(function(){
  var bar=document.getElementById('condensed');
  var nav=document.querySelector('.nav');
  if(!bar||!nav) return;
  var threshold=0, ticking=false;
  function measure(){ threshold = nav.getBoundingClientRect().bottom + window.scrollY; }
  measure(); window.addEventListener('resize', measure);
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      bar.classList.toggle('show', window.scrollY > threshold);
      ticking=false;
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
})();
document.addEventListener('keydown', function(e){
  if(e.key==='Escape'){ var m=document.getElementById('menu'); if(m) m.classList.remove('open'); }
});
// search page
(function(){
  var q=document.getElementById('q'), out=document.getElementById('results');
  if(!q||!out||!window.SEARCH_DATA) return;
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function render(term){
    out.innerHTML='';
    term=term.trim().toLowerCase();
    if(term.length<2) return;
    var hits=window.SEARCH_DATA.filter(function(d){
      return (d.t+' '+d.x+' '+d.k+' '+(d.b||'')).toLowerCase().indexOf(term)>-1;
    }).slice(0,30);
    if(!hits.length){ out.innerHTML='<p class="none">Nothing found for &ldquo;'+esc(term)+'&rdquo;. Try a season, a dish, or a room.</p>'; return; }
    hits.forEach(function(d){
      var row=document.createElement('div'); row.className='r-row';
      row.innerHTML='<a href="'+d.u+'"><span class="k">'+esc(d.k)+'</span><span class="t">'+esc(d.t)+'</span>'+(d.x?'<span class="x">'+esc(d.x)+'</span>':'')+'</a>';
      out.appendChild(row);
    });
  }
  q.addEventListener('input',function(){render(q.value);});
})();
"""
    open(os.path.join(SITE,"js","site.js"),"w",encoding="utf-8").write(js)
    print("wrote js/site.js")

def build_extras():
    body = """
  <section class="measure" style="text-align:center;padding:clamp(4rem,9vw,7rem) 0">
    <p class="eyebrow">Page not found</p>
    <h1 style="font-family:var(--display);font-weight:400;font-size:clamp(1.9rem,3.2vw,3.1rem);margin:.85rem 0 0">This page has wandered off.</h1>
    <p class="stand" style="margin:1.2rem auto 0;max-width:44ch">Like the geese, it may simply have moved on for the season. The letters, the recipes, and the rest of the house are all still where they were.</p>
    <p style="margin:2rem 0 0"><a class="rulelink" href="/index.html">Back to the house<span class="arw">&rarr;</span></a></p>
  </section>
"""
    page("404.html","Page not found — She’s the Goose","",body,"","")
    # sitemap + robots
    urls = ["","kitchen.html","table.html","garden.html","the-edit.html","recipes.html",
            "about.html","search.html","letters/index.html"]
    urls += [f"letters/{l['slug']}.html" for l in LETTERS]
    urls += [f"recipes/{r['slug']}.html" for r in RECIPES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>https://shesthegoose.com/{u}</loc></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(SITE,"sitemap.xml"),"w").write(sm)
    open(os.path.join(SITE,"robots.txt"),"w").write("User-agent: *\nAllow: /\nSitemap: https://shesthegoose.com/sitemap.xml\n")
    print("wrote 404.html sitemap.xml robots.txt")

if __name__ == "__main__":
    build_home(); build_depts(); build_edit(); build_recipes()
    build_recipe_pages(); build_letters(); build_about(); build_search(); build_js()
    build_extras()
    print("done")
