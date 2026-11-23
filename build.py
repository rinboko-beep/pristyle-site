# Builds the Pristyle site into public/.
#   python3 build.py
# Edit CONFIG below (phone, area, Instagram, site URL) and rebuild.
import json, os, shutil, html

CONFIG = {
    "SITE": os.environ.get("SITE_URL", "https://pristyle-il.netlify.app"),
    "PHONE": "058-7740-640",          # taken from the sign in the video – confirm
    "AREA": "",                        # e.g. "צפון והקריות" – shown in footer/description when set
    "INSTAGRAM": "",                   # e.g. "https://instagram.com/pristyle"
}

MAINS = [
    ("חלת שניצל", "בליווי מטבוחה, חצילים ופלפל חריף", "אפשר בלי חריף", "#ffc928", "sandwich"),
    ("מיני המבורגרים", "בתוספת ירקות, בליווי רוטב איולי פסטו", "", "#ff8a1f", "burger"),
    ("מיני פיתות עראייס", "במילוי בשר בקר טחון, בליווי טחינה", "", "#ea3b2a", "pita"),
    ("טורטייה", "במילוי חזה עוף, בליווי רוטב מרינדה", "", "#45b34a", "wrap"),
    ("פלאפל", "חצאי פיתות פלאפל ביתי, בליווי טחינה", "מתאים לצמחונים ולטבעונים", "#c7a6ff", "falafel"),
]
SIDES = ["אגרול ירקות", "כרובית מטוגנת", "סיגרים", "פסטלים", "טבעות בצל", "חציל מצופה",
         "כדורי פירה", "ציפס תפו״א", "ציפס בטטה", "קובה"]
SIDE_COLORS = ["#ffc928", "#ff8a1f", "#ea3b2a", "#45b34a", "#8a3fd0", "#ff4d6d", "#f1f1f4"]

ICONS = {
 "sandwich": '<path d="M10 52c0-14 14-22 36-22s36 8 36 22" /><path d="M8 60h76" /><path d="M12 68c8 4 16-4 24 0s16-4 24 0 16-4 24 0"/><path d="M14 78h64c0 6-6 8-32 8S14 84 14 78z"/><path d="M30 40v-4M46 36v-4M62 40v-4"/>',
 "burger": '<path d="M14 44c0-14 14-24 32-24s32 10 32 24z"/><path d="M10 54h72"/><path d="M12 62c10 5 18-5 34 0s24-5 34 0"/><path d="M14 72h64v4c0 6-8 10-32 10S14 82 14 76z"/><path d="M34 32h.1M46 28h.1M58 32h.1"/>',
 "pita": '<path d="M12 70 46 22l34 48c-6 10-62 10-68 0z"/><path d="M28 56c6 3 12-3 18 0s12-3 18 0"/><path d="M22 64h48"/>',
 "wrap": '<path d="M20 26h52l-6 58H26z"/><path d="M20 26c10 8 42 8 52 0"/><path d="M30 44c6 4 12-4 18 0s12-4 16 0"/><path d="M28 60h36"/>',
 "falafel": '<circle cx="30" cy="58" r="14"/><circle cx="62" cy="58" r="14"/><circle cx="46" cy="34" r="14"/><path d="M26 54h.1M34 62h.1M58 54h.1M66 62h.1M42 30h.1M50 38h.1"/>',
}

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 0 1 2.2 12C2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9a9.7 9.7 0 0 1 2.9 6.9c0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2A11.8 11.8 0 0 0 12 .2C5.5.2.2 5.5.2 12c0 2.1.5 4.1 1.6 5.9L.1 24l6.3-1.6c1.7.9 3.7 1.4 5.6 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.4-8.4z"/></svg>'

FAQ = [
    ("כמה עולה שולחן לאירוע?", "יש שלושה תפריטים: סטנדרט 80 ₪ לראש, גולד 95 ₪ לראש ופרימיום 110 ₪ לראש. בכל תפריט יש פירות, ירקות ורטבים, וההבדל הוא בכמות המנות העיקריות והתוספות."),
    ("מה ההזמנה המינימלית?", "הזמנה מינימום 50 ראש."),
    ("מה ההבדל בין סטנדרט, גולד ופרימיום?", "סטנדרט: מנה עיקרית אחת ו־3 סוגי תוספות. גולד: 2 מנות עיקריות ו־5 סוגי תוספות. פרימיום: 3 מנות עיקריות ו־7 סוגי תוספות."),
    ("יש אפשרות לצמחונים וטבעונים?", "כן. הפלאפל (חצאי פיתות פלאפל ביתי עם טחינה) מתאים לצמחונים ולטבעונים, וגם הירקות והפירות על השולחן."),
    ("אפשר בלי חריף?", "כן. בחלת השניצל אפשר להוריד את הפלפל החריף."),
    ("יש גם שולחן פירות?", "כן: שולחן פירות, קיאק פירות, מגש פירות וקינוחים. כתבו לנו מה אתם צריכים ונבנה לכם הצעה."),
    ("איך מזמינים?", "כותבים לנו בוואטסאפ את התאריך, המקום ומספר האורחים, או בונים תפריט כאן באתר ושולחים. אנחנו חוזרים אליכם לסגור את הפרטים."),
]

RING_IMGS = ["big-table", "pool-guests", "closeup-land", "chef", "garden-table", "rings", "hall-table", "window-table", "pool-party", "table-land", "pergola", "team"]
PLANE_IMGS = ["garden-wide", "big-table", "hall-wide", "window-table", "pergola",
              "rings", "closeup-land", "chef", "table-land", "pool-table",
              "event-sign", "pool-guests", "garden-table", "hall-table", "team"]
COLS = [["big-table", "pool-guests", "garden-table", "hall-table", "pergola"],
        ["closeup-land", "chef", "rings", "table-land", "window-table"],
        ["pool-party", "event-sign", "garden-wide", "team", "pool-table"]]
WIDE = {"closeup-land", "table-land"}
ALT = {"big-table": "שולחן קייטרינג ארוך עם ירקות צבעוניים, כרוב סגול ומנות חמות", "pool-guests": "אורחים מתאספים סביב שולחן Pristyle במסיבת בריכה",
       "closeup-land": "תקריב של השולחן: פלפלים, גזר, צ׳יפס, חצילים ופיתות", "chef": "השף של Pristyle מציג שולחן ערוך",
       "garden-table": "שולחן קייטרינג באירוע בגינה", "rings": "טבעות בצל, ירקות ומנות על השולחן", "hall-table": "שולחן ערוך באולם אירועים",
       "window-table": "שולחן ירקות וכריכים מול חלון", "pool-party": "חבר׳ה ליד שולחן Pristyle במסיבת בריכה", "table-land": "שולחן עם שיפודים, ירקות ופסטלים",
       "pergola": "אירוע בגינה מתחת לפרגולה", "team": "הצוות של Pristyle מאחורי שולחן", "hall-wide": "הקמת שולחן באולם", "pool-table": "שולחן ארוך ליד הבריכה",
       "event-sign": "שולחן ליד שלט אירוע", "garden-wide": "שני שולחנות באירוע בגינה"}

def esc(s): return html.escape(s, quote=True)

def build():
    c = CONFIG
    num = "972" + c["PHONE"].replace("-", "").lstrip("0")
    wa = f"https://wa.me/{num}?text=" + __import__("urllib.parse").parse.quote("היי Pristyle, הגעתי מהאתר ואשמח לשמוע פרטים על שולחן לאירוע")
    ring = "".join(f'<div class="ph"><img src="img/{n}.jpg" alt="" loading="eager" decoding="async"></div>' for n in RING_IMGS)
    plane = "".join(f'<div class="t"><img src="img/{n}.jpg" alt="" loading="lazy" decoding="async"></div>' for n in PLANE_IMGS)
    words = [m[0] for m in MAINS] + SIDES + ["שולחן פירות", "קיאק פירות", "ירקות", "רטבים"]
    def chips(ws, off):
        out = ""
        for i, w in enumerate(ws * 2):
            out += f'<span class="chip" style="background:{SIDE_COLORS[(i + off) % len(SIDE_COLORS)]}"><i></i>{esc(w)}</span>'
        return out
    half = len(words) // 2
    dishes = ""
    for i, (n, d, tag, col, ic) in enumerate(MAINS):
        dishes += (f'<article class="dish" style="background:linear-gradient(160deg,{col},color-mix(in srgb,{col} 70%,#000))">'
                   f'<div class="num">0{i+1}</div><svg class="ico" viewBox="0 0 92 92" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[ic]}</svg>'
                   f'<h3>{esc(n)}</h3><p>{esc(d)}</p>{f"<span class=tag>{esc(tag)}</span>" if tag else ""}</article>')
    dishes += ('<article class="dish photo"><img src="img/closeup-land.jpg" alt="" loading="lazy"><div class="num">+</div>'
               '<h3>ועוד המון צבע</h3><p>תוספות, ירקות חתוכים, פירות ורטבים בכל תפריט.</p><a class="tag" href="#packages">לתפריטים ולמחירים</a></article>')
    sides = "".join(f'<span class="side"><b style="background:{SIDE_COLORS[i % len(SIDE_COLORS)]}"></b>{esc(s)}</span>' for i, s in enumerate(SIDES))
    colsh = "".join('<div class="col">' + "".join(f'<img src="img/{n}.jpg" class="{"w" if n in WIDE else ""}" alt="{esc(ALT.get(n, "שולחן של Pristyle"))}" loading="lazy" decoding="async">' for n in col) + '</div>' for col in COLS)
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    ld_biz = {"@context": "https://schema.org", "@type": "FoodEstablishment", "name": "Pristyle",
              "alternateName": "פריסטייל", "slogan": "כל אירוע בסטייל", "url": c["SITE"] + "/",
              "image": c["SITE"] + "/img/og.jpg", "logo": c["SITE"] + "/img/logo.png",
              "telephone": "+" + num, "priceRange": "₪80–₪110 לראש", "servesCuisine": ["ישראלי", "קייטרינג", "אוכל רחוב"],
              "description": "שולחנות קייטרינג צבעוניים לאירועים: מנות עיקריות חמות, תוספות, ירקות, פירות ורטבים.",
              "hasMenu": {"@type": "Menu", "hasMenuSection": [
                  {"@type": "MenuSection", "name": "תפריטים", "hasMenuItem": [
                      {"@type": "MenuItem", "name": n, "offers": {"@type": "Offer", "price": p, "priceCurrency": "ILS"}}
                      for n, p in [("תפריט סטנדרט (לראש)", 80), ("תפריט גולד (לראש)", 95), ("תפריט פרימיום (לראש)", 110)]]}]}}
    if c["AREA"]: ld_biz["areaServed"] = c["AREA"]
    if c["INSTAGRAM"]: ld_biz["sameAs"] = [c["INSTAGRAM"]]
    rep = {
        "SITE": c["SITE"], "WA": esc(wa), "WA_NUM": num, "WA_ICON": WA_SVG,
        "WA_ICON_DARK": WA_SVG.replace('fill="currentColor"', 'fill="#06260f"'),
        "PHONE_DISPLAY": c["PHONE"], "PHONE_DISPLAY_BTN": f'<span class="ltr">{c["PHONE"]}</span>',
        "AREA_TEXT": (f"משרתים את {c['AREA']}." if c["AREA"] else ""), "AREA_FOOT": (f" · {esc(c['AREA'])}" if c["AREA"] else ""),
        "IG_LINK": (f'<a href="{esc(c["INSTAGRAM"])}" target="_blank" rel="noopener">אינסטגרם</a>' if c["INSTAGRAM"] else ""),
        "RING": ring, "PLANE": plane, "CHIPS1": chips(words[:half], 0), "CHIPS2": chips(words[half:], 3),
        "DISHES": dishes, "SIDES": sides, "COLS": colsh, "FAQ_HTML": faq_html,
        "MAINS_JSON": json.dumps([m[0] for m in MAINS], ensure_ascii=False), "SIDES_JSON": json.dumps(SIDES, ensure_ascii=False),
        "LD_FAQ": json.dumps(ld_faq, ensure_ascii=False), "LD_BUSINESS": json.dumps(ld_biz, ensure_ascii=False),
    }
    t = open("template.html", encoding="utf-8").read()
    for k, v in rep.items(): t = t.replace("{{" + k + "}}", v)
    assert "{{" not in t, t[t.index("{{"):t.index("{{") + 40]
    shutil.rmtree("public", ignore_errors=True); os.makedirs("public")
    open("public/index.html", "w", encoding="utf-8").write(t)
    shutil.copytree("img", "public/img"); shutil.copytree("media", "public/media")
    open("public/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {c['SITE']}/sitemap.xml\n")
    from datetime import date
    open("public/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{c["SITE"]}/</loc><lastmod>{date.today()}</lastmod></url></urlset>\n')
    print("built public/ (", len(t) // 1024, "KB html )")

if __name__ == "__main__":
    build()
