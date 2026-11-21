#!/usr/bin/env python3
"""THE OVERNIGHT EDITION - a one-page dark-edition newspaper summing up
Friday 20 November 2026: 38 stories, 13 pictured cards, a locator map,
25 briefs, a numbers strip and a date check.

Draws entry.png (1024x1024) next to this file using only Pillow primitives:
flat vector-style shapes, no external images. Deterministic: no randomness,
no clocks, no network. All facts come from the day's news pool; a source is
named beside every story.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16                      # page margin
CW = W - 2 * MX              # content width = 992

# --- Theme B: dark "overnight" edition -------------------------------------
BG = (14, 26, 43)            # deep navy #0E1A2B
PANEL = (22, 40, 63)         # panel navy #16283F
PANEL_DK = (11, 21, 36)      # caption band / inset #0B1524
CREAM = (242, 234, 216)      # #F2EAD8
MUTED = (185, 196, 212)      # #B9C4D4
GOLD = (232, 179, 60)        # #E8B33C
ALERT = (217, 95, 75)        # #D95F4B
LINE = (58, 82, 112)         # hairline on navy
LAND = (201, 168, 106)       # pale gold land #C9A86A

REGIONS = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

PLAYFAIR = "PlayfairDisplay-900.ttf"
ARCH_B = "Archivo-Bold.ttf"
ARCH_M = "Archivo-Medium.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

_cache = {}


def F(name, size):
    key = (name, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))
    return _cache[key]


def tw(s, font):
    return d.textlength(s, font=font)


def wrap(text, font, max_w):
    """Greedy word wrap; returns lines that each fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, name, size, max_w, floor=8):
    """Shrink a font until text fits max_w (never below floor px)."""
    while size > floor and tw(text, F(name, size)) > max_w:
        size -= 1
    return F(name, size)


def text(x, y, s, font, fill=CREAM, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def panel(x, y, w, h, fill=PANEL, outline=None):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline)

# --- The day's pool (facts verbatim from the merged NI20 pool) --------------
NUMBERS = [
    ("3", "bridges over the Dnipro damaged in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan's share index, Friday's close"),
    ("100,000", "youth visas a year in the UK-EU deal"),
    ("$120bn", "adaptation finance gap left open at COP31"),
    ("118", "runs by Glenn Phillips against India"),
]

TIMELINE = [
    ("Overnight", "Kyiv barrage: seven waves from 01:25 local"),
    ("02:30 UTC", "Cyclone Akvan makes landfall in Odisha"),
    ("06:00 UTC", "Tokyo close: Nikkei -5.1% in the AI sell-off"),
    ("Midday", 'Brussels: UK and EU seal the "reset" deal'),
    ("Evening", "Wellington: Phillips completes 118 vs India"),
]

REGION_COUNTS = [
    ("EUROPE", 9), ("ASIA", 10), ("MIDEAST", 3), ("AFRICA", 4),
    ("AMERICAS", 4), ("OCEANIA", 3), ("GLOBAL", 5),
]

# no, place, region, topic, headline, deck, strip source tag, strip data
# label, caption band, pin lon/lat
CARDS = [
    (1, "KYIV, UKRAINE", "EUROPE", "WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of about 110 missiles and 400 drones killed at "
     "least nine people across Ukraine and cut power and water in the "
     "capital. (Kyiv Independent, BBC)",
     "Officials' count", "3 BRIDGES HIT", "KYIV - THE DNIPRO",
     (30.5, 50.4)),
    (2, "ODISHA, INDIA", "ASIA", "WEATHER",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after more "
     "than 300,000 people were moved to shelters. No deaths were reported. "
     "(IMD, Deccan Herald)",
     "Weather office", "LANDFALL - 8 AM", "GOPALPUR - ODISHA COAST",
     (84.9, 19.3)),
    (3, "TAIPEI - SEOUL - TOKYO", "ASIA", "MARKETS",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chipmakers led the slide. (Al Jazeera, Anadolu)",
     "Closing prices",
     "TAIPEI -6.2% - SEOUL -5.2% - TOKYO -5.1% - HONG KONG -1.9%",
     "ASIA CLOSES - FRIDAY", (121.0, 25.0)),
    (4, "BRUSSELS", "EUROPE", "DIPLOMACY",
     'UK and EU seal a "reset" deal',
     "Food trade, youth visas, carbon link - 100,000 youth visas a year. "
     "(Reuters)",
     "Agreed - Reuters", "AGREED", "BRUSSELS - RESET DEAL",
     (4.3, 50.8)),
    (5, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 reaches its last day with no deal",
     "Draft omits fossil fuels; $120bn adaptation gap unresolved on the "
     "final day. (UN News)",
     "Ongoing - UN News", "NO DEAL - FINAL DAY", "ANTALYA - COP31",
     (30.7, 36.9)),
    (6, "EASTERN POLAND", "EUROPE", "WAR",
     "Russian cruise missile lands in Poland",
     "Fell in a field; two airports paused. Crossed during the Kyiv "
     "barrage, minister said. (Reuters)",
     "Minister says - Reuters", "FELL IN A FIELD", "EASTERN POLAND - FIELD",
     (22.5, 51.2)),
    (7, "CENTRAL IRAQ", "MIDEAST", "CONFLICT",
     "Iraqi army enters militia stronghold",
     "Troops deploy to Jurf al-Sakhar in the first push into the town in "
     "years. (Reuters)",
     "Witnessed - Reuters", "JURF AL-SAKHAR", "CENTRAL IRAQ - DEPLOYMENT",
     (44.2, 32.9)),
    (8, "ITALY", "EUROPE", "LABOUR",
     "General strike over Italy's budget",
     "Workers and students march in about 100 squares in a 24-hour CGIL "
     "stoppage. (Reuters, AFP)",
     "Reported - Reuters", "SCIOPERO - 24H", "ITALY - 100 SQUARES",
     (12.5, 41.9)),
    (9, "TOKYO", "ASIA", "ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "Inflation hit 2.3% in October, up from 2.1% - above target a second "
     "month. (Reuters)",
     "Official data - Reuters", "CPI +2.3% OCT", "TOKYO - OCTOBER CPI",
     (139.7, 35.7)),
    (10, "SEOUL", "ASIA", "POLITICS",
     "Korea's ruling party to impeach top judge",
     "Party voted to impeach Chief Justice Cho Hee-dae after an overturned "
     "conviction. (Korea Herald)",
     "Party decision - Korea Herald", "CAUCUS VOTE", "SEOUL - ASSEMBLY",
     (127.0, 37.6)),
    (11, "TURKANA, KENYA", "AFRICA", "ENERGY",
     "Kenya starts drilling its first oil well",
     "The ceremony opened the Turkana field. First crude is due on "
     "1 December. (allAfrica)",
     "Ceremony held - allAfrica", "FIRST CRUDE 1 DEC",
     "TURKANA - FIRST WELL", (35.9, 3.1)),
    (12, "SAN SALVADOR", "AMERICAS", "POLITICS",
     "Bukele files to run for a third term",
     "He filed with the electoral tribunal on Friday. The vote is on "
     "28 February 2027. (AP)",
     "Filed - AP", "VOTE 28 FEB 2027", "SAN SALVADOR - TRIBUNAL",
     (-89.2, 13.7)),
    (13, "WELLINGTON", "OCEANIA", "CRICKET",
     "Phillips hits 118 against India",
     "Phillips 118, Nicholls 175, in a stand of 216. Hundreds in all three "
     "formats. (ICC)",
     "Scorecard - ICC", "118 - RECORD", "WELLINGTON - THE BASIN",
     (174.8, -41.3)),
]

BRIEFS = [
    (14, "Lviv", "A strike on a railway station kills two (BBC)"),
    (15, "Moscow", "Russia decries Estonia's border closure (Reuters)"),
    (16, "Berlin", "School pupils strike against military service (Al Jazeera)"),
    (17, "London", "General says UK runs cyber attacks abroad (Sky News)"),
    (18, "Beijing", "China holds its loan rates for an 18th month (Xinhua)"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day (Al Jazeera)"),
    (20, "Seoul", "Kospi index ends the week 7.9% lower (Anadolu)"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha (PTI)"),
    (22, "Lebanon", "Israeli air strikes hit the south and the east (Anadolu)"),
    (23, "Yemen", "Gunmen fire on a cargo ship off the coast (UKMTO)"),
    (24, "Abuja", "Court bars new evidence against Tinubu (Channels TV)"),
    (25, "Kampala", "Police told to enforce Ebola ban on rallies (allAfrica)"),
    (26, "Malawi", "Fuel crisis brings night-long petrol queues (Al Jazeera)"),
    (27, "New York", "Nasdaq futures fall 1.6% before the bell (24/7 Wall St)"),
    (28, "Washington", "Democrats query law firm's free work (Al Jazeera)"),
    (29, "Sydney", "Australian shares fall 1.6% in the sell-off (Reuters)"),
    (30, "Antalya", "Panama asks COP31 to cap world oil output (Al Jazeera)"),
    (31, "Antalya", "EU official calls the climate draft unacceptable (RTE)"),
    (32, "Turin", "ATP backs a plan to lift player pay past $350m (Anadolu)"),
    (33, "Bougainville", "Rio Tinto pledges $370m for Panguna mine cleanup (Reuters)"),
    (34, "Iowa", "US Army sets noon detonation of 68 unstable explosive barrels (AP)"),
    (35, "Hormuz", "Four attacks on vessels in 96 hours, maritime centre says (UKMTO)"),
    (36, "Jakarta", "Indonesia's parliament passes asset-forfeiture bill (Reuters)"),
    (37, "Barcelona", "Pancreatic cancer pill shrinks tumours 60.7% in early trial (Reuters)"),
    (38, "Mercury", "BepiColombo reaches Mercury after 8 years; orbit insertion set for Saturday (ESA, BBC)"),
]

# brief number -> (lon, lat, region) for the map dots
BRIEF_PINS = {
    14: (24.0, 49.8, "EUROPE"), 15: (37.6, 55.8, "EUROPE"),
    16: (13.4, 52.5, "EUROPE"), 17: (-0.1, 51.5, "EUROPE"),
    18: (116.4, 39.9, "ASIA"), 19: (139.7, 35.7, "ASIA"),
    20: (127.0, 37.6, "ASIA"), 21: (84.9, 19.3, "ASIA"),
    22: (35.5, 33.3, "MIDEAST"), 23: (43.3, 11.8, "MIDEAST"),
    24: (7.5, 9.1, "AFRICA"), 25: (32.6, 0.3, "AFRICA"),
    26: (33.8, -13.9, "AFRICA"),
    27: (-74.0, 40.7, "AMERICAS"), 28: (-77.0, 38.9, "AMERICAS"),
    29: (151.2, -33.9, "OCEANIA"),
    30: (30.7, 36.9, "GLOBAL"), 31: (30.7, 36.9, "GLOBAL"),
    32: (7.7, 45.1, "EUROPE"), 33: (155.9, -6.3, "OCEANIA"),
    34: (-93.6, 41.9, "AMERICAS"), 35: (56.3, 26.6, "MIDEAST"),
    36: (106.8, -6.2, "ASIA"), 37: (2.2, 41.4, "EUROPE"),
}

DATE_CHECK = (
    "Left out as Thursday 19 November's news: the World Court's ruling on "
    "Myanmar, the three-leader declaration in Shenzhen, the migrant boat "
    "lost off Senegal, Anthropic's $83bn IPO pricing, the GTA VI midnight "
    "launch, the $190.4m Van Gogh sale and the Senate's 48-51 Iran "
    "war-powers vote. Not yet happened, so not shown: COP31's final text "
    "and BepiColombo's entry into orbit around Mercury (set for Saturday)."
)

FOOTER_L = ("Every story here happened, or was first reported, on Friday "
            "20 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# --- Card strip scenes (flat layered shapes; area excludes caption band) ---
def scene_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 74, 107))          # night sky
    for sx, sy in ((0.12, 0.2), (0.55, 0.12), (0.85, 0.3)):         # stars
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3],
                  fill=MUTED)
    river_y = y + h - max(10, h // 4)
    d.rectangle([x, river_y, x + w, y + h], fill=(62, 111, 163))   # Dnipro
    for i in range(3):                                             # 3 bridges
        bx = x + int(w * (0.14 + 0.3 * i))
        bw = int(w * 0.24)
        by = river_y - 4
        d.arc([bx, by - h // 3, bx + bw, by + h // 3], 180, 360,
              fill=GOLD, width=3)
        d.line([bx, by, bx + bw, by], fill=GOLD, width=3)
        d.line([bx + bw // 2, by - h // 3, bx + bw // 2, by], fill=GOLD,
               width=2)
    for i in range(3):                                             # missile arcs
        ax = x + int(w * (0.2 + 0.28 * i))
        d.arc([ax, y + 2, ax + int(w * 0.2), y + h // 2], 200, 320,
              fill=ALERT, width=2)
        ex, ey = ax + int(w * 0.19), y + h // 3
        d.polygon([(ex, ey - 6), (ex + 3, ey - 1), (ex + 7, ey),
                   (ex + 3, ey + 2), (ex + 4, ey + 6), (ex, ey + 3),
                   (ex - 4, ey + 6), (ex - 3, ey + 2), (ex - 7, ey),
                   (ex - 3, ey - 1)], fill=GOLD)


def scene_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(51, 86, 110))          # storm sky
    cx, cy = x + w // 2, y + h // 2
    base = min(34, int(h * 0.46))
    for r in (base, int(base * 0.79), int(base * 0.58), int(base * 0.38)):
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], 20, 300,
              fill=CREAM, width=3)
    d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=GOLD)         # eye
    for i in range(6):                                             # rain
        rx = x + 8 + i * (w - 16) // 5
        d.line([rx, y + h - 14, rx - 5, y + h - 4], fill=MUTED, width=2)
    d.polygon([(x, y + h), (x + w // 3, y + h - 12), (x + w, y + h)],
              fill=(30, 132, 73))                                  # coast


def scene_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))           # board
    for i in range(1, 4):                                          # grid
        gy = y + h * i // 4
        d.line([x + 4, gy, x + w - 4, gy], fill=LINE, width=1)
    pts = [(x + 8, y + h * 0.22), (x + w * 0.3, y + h * 0.34),
           (x + w * 0.52, y + h * 0.3), (x + w * 0.74, y + h * 0.58),
           (x + w - 10, y + h * 0.8)]
    d.line(pts, fill=ALERT, width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 10, ey - 7), (ex - 3, ey - 12)], fill=ALERT)
    for px, py in pts[:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=CREAM)


def _flag_uk(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 110), outline=CREAM)
    d.line([x, y, x + w, y + h], fill=CREAM, width=3)
    d.line([x + w, y, x, y + h], fill=CREAM, width=3)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=CREAM, width=7)
    d.line([x, y + h // 2, x + w, y + h // 2], fill=CREAM, width=7)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(179, 32, 44), width=3)
    d.line([x, y + h // 2, x + w, y + h // 2], fill=(179, 32, 44), width=3)


def _flag_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 80, 160), outline=CREAM)
    import math
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 3
    for i in range(12):
        a = math.tau * i / 12
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def scene_flags(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 60, 92))
    fh = min(30, max(16, h - 18))
    fw = int(fh * 1.5)
    _flag_uk(x + w // 2 - fw - 6, y + 8, fw, fh)
    _flag_eu(x + w // 2 + 6, y + 8, fw, fh)
    d.line([x + w // 2 - fw - 6, y + 8 + fh, x + w // 2 + 6 + fw,
            y + 8 + fh], fill=GOLD, width=2)                       # table line


def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 62, 74))           # teal hall
    cx, cy = x + w // 2 - 14, y + h // 2
    r = min(h // 2 - 4, 34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(29, 111, 184),
              outline=CREAM, width=2)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=CREAM)
    d.line([cx - r, cy, cx + r, cy], fill=CREAM, width=1)
    d.line([cx - r, cy - r // 2, cx + r, cy - r // 2], fill=CREAM, width=1)
    d.line([cx - r, cy + r // 2, cx + r, cy + r // 2], fill=CREAM, width=1)
    tx = x + w - 30                                                # thermometer
    d.rectangle([tx, y + 8, tx + 7, y + h - 16], fill=CREAM)
    d.rectangle([tx + 1, y + 12, tx + 6, y + h - 16], fill=ALERT)
    d.ellipse([tx - 3, y + h - 22, tx + 10, y + h - 9], fill=ALERT)


def scene_poland(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 116, 62))          # field
    for i in range(4):                                             # furrows
        fy = y + 8 + i * (h - 16) // 4
        d.line([x + 4, fy, x + w - 4, fy - 4], fill=(56, 92, 46), width=2)
    mx0, my0 = x + w // 2 - 24, y + h // 2 - 6                     # missile
    d.polygon([(mx0, my0 + 8), (mx0 + 34, my0), (mx0 + 48, my0 + 3),
               (mx0 + 36, my0 + 10), (mx0 + 6, my0 + 14)],
              fill=(196, 200, 208))
    d.polygon([(mx0 + 40, my0 + 1), (mx0 + 52, my0 + 4), (mx0 + 41, my0 + 9)],
              fill=ALERT)
    d.line([x + w - 14, y + 4, x + w - 14, y + h - 4], fill=GOLD, width=2)
    for yy in range(y + 8, y + h - 4, 10):                         # border dashes
        d.line([x + w - 14, yy, x + w - 14, yy + 5], fill=PANEL_DK, width=2)


def scene_iraq(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 178, 110))        # desert
    d.ellipse([x + w - 34, y + 5, x + w - 12, y + 27], fill=GOLD)  # sun
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(186, 138, 74))
    for i, vx in enumerate((0.16, 0.55)):                          # vehicles
        bx = x + int(w * vx)
        by = y + h - 26
        d.rectangle([bx, by, bx + 42, by + 12], fill=(94, 84, 52))
        d.rectangle([bx + 8, by - 7, bx + 26, by], fill=(94, 84, 52))
        d.ellipse([bx + 5, by + 9, bx + 15, by + 19], fill=PANEL_DK)
        d.ellipse([bx + 27, by + 9, bx + 37, by + 19], fill=PANEL_DK)
        d.line([bx + 30, by - 7, bx + 44, by - 12], fill=PANEL_DK, width=2)

def scene_italy(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 84, 110))          # square
    bw = int(w * 0.44)                                             # banner
    bx, by = x + 4, y + 1        # top-left: clears the source tag (top-right)
                                 # and the data-label pill (bottom-left)
    bh = max(13, h // 4)
    d.rectangle([bx, by, bx + bw, by + bh], fill=CREAM)
    bf = fit("SCIOPERO", ARCH_B, bh - 3, bw - 8, floor=7)
    text(bx + bw // 2, by + bh // 2, "SCIOPERO", bf, fill=(179, 32, 44),
         anchor="mm")
    cols = max(6, w // 22)                                         # crowd
    for i in range(cols):
        for j in range(2):
            hx = x + 10 + i * 22 + (8 if j else 0)
            hy = y + h - 13 - j * 11
            if bx - 8 < hx < bx + bw + 8 and j == 1:
                continue
            d.ellipse([hx, hy, hx + 7, hy + 7], fill=(232, 200, 150))
            d.pieslice([hx - 2, hy + 5, hx + 9, hy + 13], 180, 360,
                       fill=(150, 60, 50) if (i + j) % 2 else (60, 90, 140))


def scene_japan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 68))
    base = y + h - 8
    d.line([x + 8, base, x + w - 8, base], fill=MUTED, width=2)
    vals = (0.42, 0.58, 0.82)                                      # rising bars
    bw = max(14, w // 7)
    for i, v in enumerate(vals):
        bx = x + w // 2 - bw - 10 + i * (bw + 10)
        bh = int((h - 18) * v)
        d.rectangle([bx, base - bh, bx + bw, base],
                    fill=GOLD if i == 2 else (29, 111, 184))
    d.line([x + w // 2 - bw - 14, base - int((h - 18) * 0.5),
            x + w // 2 + bw + 14, base - int((h - 18) * 0.5)],
           fill=ALERT, width=2)                                    # target line


def scene_seoul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 104, 128))         # stone hall
    cx = x + w // 2
    tw_ = int(w * 0.62)
    ped = max(8, h // 3)
    d.polygon([(cx - tw_ // 2, y + ped), (cx + tw_ // 2, y + ped),
               (cx, y + 2)], fill=CREAM)                           # pediment
    d.rectangle([cx - tw_ // 2, y + ped + 2, cx + tw_ // 2, y + ped + 5],
                fill=CREAM)
    for i in range(4):                                             # columns
        colx = cx - tw_ // 2 + 6 + i * (tw_ - 12) // 3
        d.rectangle([colx - 3, y + ped + 7, colx + 3, y + h - 6], fill=CREAM)
    d.rectangle([cx - tw_ // 2, y + h - 6, cx + tw_ // 2, y + h - 2],
                fill=CREAM)
    d.line([cx + tw_ // 4, y + h // 2, cx + tw_ // 4 + 10, y + h // 2 - 6],
           fill=GOLD, width=3)                                     # gavel hint


def scene_kenya(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 190, 120))        # savanna
    d.ellipse([x + 8, y + 5, x + 28, y + 25], fill=GOLD)
    d.rectangle([x, y + h - 9, x + w, y + h], fill=(170, 120, 60))
    cx = x + w // 2                                                # derrick
    top = y + 5
    bot = y + h - 9
    d.line([cx - 20, bot, cx, top], fill=PANEL_DK, width=3)
    d.line([cx + 20, bot, cx, top], fill=PANEL_DK, width=3)
    d.line([cx - 13, bot - (bot - top) // 2, cx + 13, bot - (bot - top) // 2],
           fill=PANEL_DK, width=2)
    d.line([cx, top, cx + 22, top + 6], fill=PANEL_DK, width=3)    # arm
    d.line([cx + 22, top + 6, cx + 22, top + 16], fill=PANEL_DK, width=2)
    d.ellipse([cx + 19, top + 16, cx + 25, top + 22], fill=ALERT)  # first drop


def scene_bukele(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 92, 140))          # hall blue
    cx = x + w // 2
    bw, bh = int(w * 0.4), max(20, h // 2)
    bx, by = cx - bw // 2, y + h - bh - 4
    d.rectangle([bx, by, bx + bw, by + bh], fill=(240, 236, 224),
                outline=PANEL_DK, width=2)                         # ballot box
    d.rectangle([bx + 8, by + 5, bx + bw - 8, by + 9], fill=PANEL_DK)
    d.polygon([(cx - 9, y + 4), (cx + 9, y + 4), (cx + 5, by + 7),
               (cx - 5, by + 7)], fill=CREAM)                      # paper slip
    d.rectangle([bx, by + bh - 8, bx + bw, by + bh], fill=(29, 111, 184))


def scene_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 122, 74))          # outfield
    pw = int(w * 0.3)
    px = x + (w - pw) // 2
    d.rectangle([px, y + 6, px + pw, y + h - 4], fill=(222, 198, 140))
    sx = px + pw - 16                                              # stumps
    for i in range(3):
        d.line([sx + i * 5, y + h - 22, sx + i * 5, y + h - 8],
               fill=(240, 220, 160), width=2)
    d.line([sx, y + h - 23, sx + 10, y + h - 23], fill=GOLD, width=2)
    bx = px + 12                                                   # bat
    d.polygon([(bx, y + h - 26), (bx + 6, y + h - 28), (bx + 12, y + h - 8),
               (bx + 4, y + h - 6)], fill=(196, 150, 90))
    d.ellipse([x + w - 30, y + 10, x + w - 20, y + 20], fill=(179, 32, 44))
    d.arc([x + w - 52, y + 4, x + w - 16, y + 30], 90, 200, fill=CREAM,
          width=2)                                                 # ball trail


SCENES = {1: scene_kyiv, 2: scene_cyclone, 3: scene_markets, 4: scene_flags,
          5: scene_cop, 6: scene_poland, 7: scene_iraq, 8: scene_italy,
          9: scene_japan, 10: scene_seoul, 11: scene_kenya,
          12: scene_bukele, 13: scene_cricket}

CAP_H = 16  # caption band height inside every strip


def draw_strip(card, x, y, w, h):
    """Illustrated strip: region rule, scene, source tag, data label, band."""
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    col = REGIONS[region]
    lead = w > 250
    d.rectangle([x, y, x + w, y + h], fill=PANEL_DK)
    d.rectangle([x, y, x + w, y + 3], fill=col)                    # region rule
    SCENES[no](x, y + 3, w, h - 3 - CAP_H)
    tf = F(ARCH_B, 9 if lead else 8)                               # source tag
    tag_w = tw(tag, tf) + 10
    tag_h = 14 if lead else 12
    d.rectangle([x + w - tag_w - 4, y + 5, x + w - 4, y + 5 + tag_h],
                fill=PANEL_DK)
    text(x + w - tag_w + 1, y + 5 + tag_h / 2, tag, tf, fill=CREAM,
         anchor="lm")
    lf = fit(label, ARCH_B, 13 if lead else 11, w - 14, floor=8)
    lw_ = tw(label, lf) + 12                                       # data label
    pill_h = 16 if lead else 15
    ly = y + h - CAP_H - (20 if lead else 16)
    d.rectangle([x + 5, ly, x + 5 + lw_, ly + pill_h], fill=PANEL_DK)
    text(x + 11, ly + pill_h / 2, label, lf, fill=GOLD, anchor="lm")
    d.rectangle([x, y + h - CAP_H, x + w, y + h], fill=PANEL_DK)   # band
    bf = fit(caption, ARCH_B, 10, w - 12, floor=7)
    text(x + w // 2, y + h - CAP_H // 2, caption, bf, fill=MUTED,
         anchor="mm")

# --- Header: kicker, masthead, timeline, numbers, region counts ------------
Y = 8
d.rectangle([MX, Y, MX + CW, Y + 21], fill=GOLD)
text(MX + 8, Y + 10, "THE OVERNIGHT EDITION", F(ARCH_B, 12),
     fill=PANEL_DK, anchor="lm")
text(MX + 252, Y + 10, "THE WORLD IN ONE DAY", F(ARCH_B, 12),
     fill=PANEL_DK, anchor="lm")
kr = "38 STORIES - 7 REGIONS - EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
text(MX + CW - 8, Y + 10, kr, fit(kr, ARCH_B, 12, 470), fill=PANEL_DK,
     anchor="rm")

Y = 36
mf = fit("Friday 20 November 2026", PLAYFAIR, 58, CW)
text(MX + CW // 2, Y, "Friday 20 November 2026", mf, fill=CREAM, anchor="ma")
Y += 66
deck_line = ("Kyiv's bridges hit - Akvan ashore in Odisha - an AI sell-off "
             "sweeps Asia - Britain and the EU seal a reset")
text(MX + CW // 2, Y, deck_line, fit(deck_line, ARCH_M, 14, CW),
     fill=MUTED, anchor="ma")

Y += 24                                                     # UTC timeline
panel(MX, Y, CW, 38)
cell = CW / 5.0
for i, (lab, ev) in enumerate(TIMELINE):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 5, cx0, Y + 33], fill=LINE, width=1)
    text(cx0 + 8, Y + 5, lab.upper(), F(ARCH_B, 10), fill=GOLD)
    for j, ln in enumerate(wrap(ev, F(ARCH_M, 10), cell - 14)[:2]):
        text(cx0 + 8, Y + 17 + j * 10, ln, F(ARCH_M, 10), fill=CREAM)

Y += 46                                                     # day in numbers
panel(MX, Y, CW, 56)
cell = CW / 6.0
text(MX + 8, Y + 2, "THE DAY IN NUMBERS", F(ARCH_B, 8), fill=MUTED)
for i, (num, cap) in enumerate(NUMBERS):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 8, cx0, Y + 52], fill=LINE, width=1)
    nf = fit(num, PLAYFAIR, 23, cell - 14)
    text(cx0 + 8, Y + 8, num, nf, fill=GOLD)
    for j, ln in enumerate(wrap(cap, F(ARCH_M, 9), cell - 14)[:2]):
        text(cx0 + 8, Y + 35 + j * 10, ln, F(ARCH_M, 9), fill=MUTED)

Y += 56                                                     # region counts
cx = MX
text(cx, Y + 10, "WHERE:", F(ARCH_B, 10), fill=MUTED, anchor="lm")
cx += int(tw("WHERE:", F(ARCH_B, 10))) + 10
for name, n in REGION_COUNTS:
    label = "%s %d" % (name, n)
    lf = F(ARCH_B, 11)
    wch = int(tw(label, lf)) + 24
    d.rectangle([cx, Y, cx + wch, Y + 20], fill=PANEL)
    d.ellipse([cx + 6, Y + 6, cx + 14, Y + 14], fill=REGIONS[name])
    text(cx + 18, Y + 10, label, lf, fill=CREAM, anchor="lm")
    cx += wch + 8

# --- Lead row: cards 1-3 ----------------------------------------------------
LEAD_Y = 250
LEAD_W = 325
for i, card in enumerate(CARDS[:3]):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    cx0 = MX + i * (LEAD_W + 8)
    panel(cx0, LEAD_Y, LEAD_W, 215)
    draw_strip(card, cx0 + 6, LEAD_Y + 6, LEAD_W - 12, 84)
    ry = LEAD_Y + 94
    text(cx0 + 8, ry, "%d  %s - %s - %s" % (no, place, region, topic),
         F(ARCH_B, 11), fill=REGIONS[region])
    hy = ry + 14
    for ln in wrap(headline, F(PLAYFAIR, 21), LEAD_W - 16)[:2]:
        text(cx0 + 8, hy, ln, F(PLAYFAIR, 21), fill=CREAM)
        hy += 23
    dy = hy + 2
    for ln in wrap(deck, F(ARCH_M, 12), LEAD_W - 16)[:4]:
        text(cx0 + 8, dy, ln, F(ARCH_M, 12), fill=MUTED)
        dy += 14.5

# --- Feature grid: cards 4-13, 2 rows x 5 -----------------------------------
FEAT_Y = 473
FEAT_W = 194
ROW_H = 137
for k, card in enumerate(CARDS[3:]):
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    cx0 = MX + (k % 5) * (FEAT_W + 5)
    cy0 = FEAT_Y + (k // 5) * (ROW_H + 8)
    panel(cx0, cy0, FEAT_W, ROW_H)
    draw_strip(card, cx0 + 5, cy0 + 5, FEAT_W - 10, 48)
    ry = cy0 + 56
    text(cx0 + 7, ry, "%d  %s - %s" % (no, place, region), F(ARCH_B, 9),
         fill=REGIONS[region])
    hy = ry + 12
    for ln in wrap(headline, F(ARCH_B, 14), FEAT_W - 14)[:2]:
        text(cx0 + 7, hy, ln, F(ARCH_B, 14), fill=CREAM)
        hy += 14
    dy = hy + 1
    for ln in wrap(deck, F(ARCH_M, 11), FEAT_W - 14)[:3]:
        text(cx0 + 7, dy, ln, F(ARCH_M, 11), fill=MUTED)
        dy += 11.5

# --- Bottom row: map panel + also-on panel ----------------------------------
BOT_Y = 763
BOT_H = 204
panel(MX, BOT_Y, 330, BOT_H)
text(MX + 8, BOT_Y + 6, "WHERE IT HAPPENED", F(ARCH_B, 12), fill=GOLD)

MAP_X, MAP_Y, MAP_W, MAP_H = MX + 8, BOT_Y + 26, 314, 122
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=PANEL_DK)


def proj(lon, lat):
    return (MAP_X + (lon + 180.0) / 360.0 * MAP_W,
            MAP_Y + (82.0 - lat) / 140.0 * MAP_H)


for _name, rings in WORLD.items():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(proj(float(lo), float(la)))
        if len(pts) > 2:
            d.polygon(pts, fill=LAND)

for no, (lo, la, reg) in BRIEF_PINS.items():                       # dots
    px, py = proj(lo, la)
    d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REGIONS[reg])

for card in CARDS:                                                 # pins
    no, place, region, topic, headline, deck, tag, label, caption, pin = card
    px, py = proj(pin[0], pin[1])
    r = 8
    d.ellipse([px - r, py - r, px + r, py + r], fill=REGIONS[region],
              outline=CREAM, width=1)
    text(px, py, str(no), F(ARCH_B, 9), fill=(255, 255, 255), anchor="mm")

ly = MAP_Y + MAP_H + 8
legend = "Numbered pins = the 13 pictured stories - small dots = the briefs"
for ln in wrap(legend, F(ARCH_M, 10), 314):
    text(MX + 8, ly, ln, F(ARCH_M, 10), fill=MUTED)
    ly += 12
ey = ly + 6                                                        # exit arrow
for sx in range(MX + 8, MX + 52, 7):
    d.line([sx, ey + 4, sx + 4, ey + 4], fill=GOLD, width=2)
d.polygon([(MX + 54, ey), (MX + 64, ey + 4), (MX + 54, ey + 8)], fill=GOLD)
text(MX + 70, ey + 4, "38 -> to Mercury", F(ARCH_B, 11), fill=GOLD,
     anchor="lm")

AO_X = MX + 330 + 8
AO_W = W - MX - AO_X
panel(AO_X, BOT_Y, AO_W, BOT_H)
ao_title = "ALSO ON FRIDAY 20 NOVEMBER - 25 MORE STORIES"
text(AO_X + 8, BOT_Y + 6, ao_title, fit(ao_title, ARCH_B, 12, AO_W - 16),
     fill=GOLD)

BF = F(ARCH_M, 10)
BNF = F(ARCH_B, 10)
COL_W = (AO_W - 16 - 14) // 2
brief_lines = []
for no, place, body in BRIEFS:
    num_w = tw("%d " % no, BNF)
    lines = wrap("%s %s" % (place, body), BF, COL_W - num_w)
    brief_lines.append((no, num_w, lines))
total_lines = sum(len(ls) for _, _, ls in brief_lines)
half = (total_lines + 1) // 2
cols, cur, count = [[], []], 0, 0
for item in brief_lines:
    if cur == 0 and count + len(item[2]) > half and count > 0:
        cur = 1
    cols[cur].append(item)
    count += len(item[2]) if cur == 0 else 0
for ci, col in enumerate(cols):
    bx = AO_X + 8 + ci * (COL_W + 14)
    by = BOT_Y + 24
    for no, num_w, lines in col:
        text(bx, by, "%d" % no, BNF, fill=GOLD)
        for ln in lines:
            text(bx + num_w, by, ln, BF, fill=(230, 224, 205))
            by += 10.6
        by += 0.8

# --- Date check + footer ------------------------------------------------------
DC_Y = BOT_Y + BOT_H + 6
d.rectangle([MX, DC_Y, MX + CW, DC_Y + 36], outline=ALERT, width=2)
lab = "DATE CHECK"
lab_w = tw(lab, F(ARCH_B, 10)) + 8
text(MX + 8, DC_Y + 5, lab, F(ARCH_B, 10), fill=ALERT)
# wrap the body with a narrower first line (it shares the line with the label)
words = DATE_CHECK.split()
first, rest = [], []
cur_w = CW - 16 - lab_w
for wd in words:
    trial = " ".join(first + [wd])
    if tw(trial, F(ARCH_M, 9)) <= cur_w or not first:
        first.append(wd)
    else:
        rest.append(wd)
text(MX + 8 + lab_w, DC_Y + 5, " ".join(first), F(ARCH_M, 9), fill=MUTED)
yy = DC_Y + 15
for ln in wrap(" ".join(rest), F(ARCH_M, 9), CW - 16)[:2]:
    text(MX + 8, yy, ln, F(ARCH_M, 9), fill=MUTED)
    yy += 10

FY = DC_Y + 41
text(MX, FY, FOOTER_L, F(ARCH_M, 9), fill=MUTED)
text(MX + CW, FY, FOOTER_R, F(ARCH_M, 9), fill=MUTED, anchor="ra")

img.save(OUT)
print("saved", OUT, img.size)
