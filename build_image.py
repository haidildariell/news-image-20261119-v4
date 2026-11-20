#!/usr/bin/env python3
"""Build entry.png (1024x1024) for news-image-20261119 v4.
All artwork drawn from Pillow primitives. No external assets, no network,
fully deterministic (no timestamps, no randomness).
Every story carries its own source tag inside the image.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (22, 40, 63)
INK = (22, 24, 29)
RED = (176, 42, 33)
GOLD = (201, 162, 39)
CREAM = (230, 215, 186)
SEA = (196, 208, 220)
GRAY = (107, 111, 118)
WHITE = (255, 255, 255)
CARD = (252, 249, 242)

REGION_COLORS = {
    "ASIA": (176, 42, 33),
    "EUROPE": (46, 95, 138),
    "MIDDLE EAST": (46, 125, 79),
    "AMERICAS": (122, 79, 157),
    "AFRICA": (199, 116, 20),
    "OCEANIA": (31, 122, 140),
    "GLOBAL": (107, 111, 118),
}

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# Leads: (num, kicker, region, headline, desc ending with source tag)
LEADS = [
    (1, "SHENZHEN · SUMMIT", "ASIA", "Trump, Xi & Putin Share One Table",
     "First-ever three-way summit: 90 minutes, a 4-point declaration (UN reform, "
     "refined-oil supply, ICC limits, \u201ca nuclear war cannot be won\u201d). No Ukraine "
     "deal; Trump\u2013Putin bilateral ran ~40 min. \u2014 USA Today \u00b7 Le Monde \u00b7 Breitbart"),
    (2, "NEW YORK · MARKETS", "AMERICAS", "Anthropic's Record $81.3bn IPO Debut",
     "Anthropic lists on Nasdaq as ANT: priced $83, raises $81.3bn from 980m shares \u2014 "
     "the largest IPO on record, above SpaceX's $75bn. Opens $111.50 (+34%), closes "
     "$97.17 (+17%), worth ~$2tn at the open. \u2014 Reuters \u00b7 AP \u00b7 Invezz"),
    (3, "THE HAGUE · LAW", "EUROPE", "World Court: Genocide in Myanmar",
     "ICJ rules Myanmar committed genocide against the Rohingya, 9\u20136: ~10,000 killed; "
     "reparations and return ordered. First world-court genocide ruling on the "
     "Rohingya. \u2014 Reuters \u00b7 Al Jazeera \u00b7 Just Security"),
]

# Mids: (num, kicker, region, headline, desc ending with source tag, icon key)
MIDS = [
    (4, "ANTALYA · CLIMATE", "EUROPE", "COP31 Drops Fossil Fuel",
     "[FORECAST] Draft drops fossil fuels + $120bn target; admits >1.5\u00b0C. "
     "\u2014 Reuters \u00b7 The Hindu", "globe"),
    (5, "ODISHA · STORM", "ASIA", "Akvan Nears India Coast",
     "[FORECAST] 80,000+ evacuated; landfall Fri near Gopalpur, 90\u2013100 km/h. "
     "\u2014 Hindu BusinessLine \u00b7 IMD", "cyclone"),
    (6, "SEOUL · EDUCATION", "ASIA", "551,864 Sit Suneung",
     "551,864 sit the exam at 1,312 sites; flights halted 13:10\u201313:35. "
     "\u2014 AJP \u00b7 Korea MoE", "exam"),
    (7, "CRIMEA · WAR", "EUROPE", "Crimea Bridge Hit Again",
     "Ukraine hits the bridge a 3rd time in a week; traffic halted. "
     "\u2014 BBC \u00b7 Reuters", "bridge"),
    (8, "RIYADH · WAR", "MIDDLE EAST", "Missile Targets Riyadh",
     "[CLAIM] Houthi missile targets Riyadh; PIF Tower hit by debris. "
     "\u2014 NYT \u00b7 TASS", "tower"),
    (9, "COPENHAGEN · SECURITY", "EUROPE", "Arctic Pact Backed 109\u20130",
     "Denmark backs the Arctic pact with the US 109\u20130; Greenland stays Danish. "
     "\u2014 AP \u00b7 Reuters", "shield"),
    (10, "CANBERRA · ECONOMY", "OCEANIA", "Jobless Rate Hits 4.9%",
     "Jobless rate jumps to 4.9%, a five-year high; 43,500 jobs lost. "
     "\u2014 ABS \u00b7 Reuters", "bars"),
    (11, "DHAKA · UNREST", "ASIA", "Bangladesh Erupts",
     "Awami League lockdown bites: 4 killed, 28 districts hit; minister's home "
     "torched. \u2014 Reuters \u00b7 PTI", "flame"),
    (12, "WASHINGTON · POLITICS", "AMERICAS", "Senate Rejects Iran Curb",
     "Senate rejects Iran war-powers limits 51\u201348; three GOP defectors. "
     "\u2014 Reuters \u00b7 AP", "capitol"),
    (13, "WORLDWIDE · GAMES", "GLOBAL", "GTA VI Out Worldwide",
     "On sale worldwide at midnight, NZ first; Metacritic 99, IGN 10/10. "
     "\u2014 Le Monde \u00b7 Polygon", "game"),
]

# Briefs: (num, place, region, text, source small-caps)
BRIEFS = [
    (14, "Bogot\u00e1", "AMERICAS", "Union strike vs rescue law", "COLOMBIA REPORTS \u00b7 RIO TIMES"),
    (15, "Jakarta", "ASIA", "Asset-seizure law passed after 18 yrs", "REUTERS \u00b7 ANTARA"),
    (16, "Seoul", "ASIA", "Han term partly voided 9\u20133; retrial ordered", "YONHAP \u00b7 AP"),
    (17, "Nairobi", "AFRICA", "Jepchirchir banned 3 yrs for EPO", "AIU \u00b7 ATHLETICS WEEKLY"),
    (18, "Florida", "AMERICAS", "Floods shut Broward, Miami-Dade schools", "AP \u00b7 CBS MIAMI"),
    (19, "Paris", "EUROPE", "Greens open door to M\u00e9lenchon pact", "PARTICLE"),
    (20, "Gaza", "MIDDLE EAST", "Israeli tanks push past truce line", "JUST SECURITY"),
    (21, "Amman", "MIDDLE EAST", "589m children in conflict zones 2025", "RELIEFWEB \u00b7 DW"),
    (22, "Rome", "EUROPE", "Writer Corrado Augias dies at 91", "LA REPUBBLICA \u00b7 LAPRESSE"),
    (23, "Mogadishu", "AFRICA", "UAE envoy expelled in 72h", "AL JAZEERA \u00b7 PRESSTV"),
    (24, "Pretoria", "AFRICA", "SARB holds 7.25% in 4\u20133 vote", "REUTERS \u00b7 WSJ"),
    (25, "Wellington", "OCEANIA", "Pay-equity overhaul broke women's rights", "REUTERS"),
    (26, "Zurich", "EUROPE", "Diallo, Tashima vs Infantino", "FLASHSCORE \u00b7 NEUSROOM"),
    (27, "Krasnodar", "EUROPE", "Kyiv claims Ilsky, Afipsky refinery hits", "EURONEWS"),
    (28, "Washington", "AMERICAS", "Trump: \u201csee what happens\u201d on Iran", "REUTERS"),
    (29, "Tokyo", "ASIA", "Takaichi\u2013Putin talks; keep talking", "JUST SECURITY"),
    (30, "Sanaa", "MIDDLE EAST", "[CLAIM] Saudi strikes; Houthis say 15 dead", "TASS"),
    (31, "Shenzhen", "ASIA", "APEC adopts Shenzhen Outlook", "CHINA DAILY \u00b7 SED"),
    (32, "London", "EUROPE", "\u00a3100m UK\u2013Norway boats for Ukraine", "GOV.UK \u00b7 NO GOVT"),
    (33, "Belgrade", "EUROPE", "\u010cupi\u0107 elected speaker, 140 votes", "CONNECTING REGION"),
    (34, "Mexico City", "AMERICAS", "Banxico minutes: long rate pause", "MORNINGSTAR"),
    (35, "Berlin", "EUROPE", "Call for Black Sea, energy ceasefire", "BOSPHORUS NEWS"),
    (36, "Tonga", "OCEANIA", "Drought emergency, 27 days", "US EMBASSY \u00b7 GOVT OF TONGA"),
    (37, "Cook Islands", "OCEANIA", "[FORECAST] Xavier weakens, Cat 4", "FIJI MET"),
    (38, "Gaza", "MIDDLE EAST", "Aid groups score peace plan 4 of 26", "RELIEFWEB \u00b7 AL JAZEERA"),
    (39, "Moscow", "EUROPE", "Putin rules out Black Sea truce", "REUTERS"),
    (40, "Auckland", "OCEANIA", "NZ first to play GTA VI at midnight", "LE MONDE \u00b7 ASIATODAY"),
    (41, "Yenne, Senegal", "AFRICA", "Missing-boat search resumes", "REUTERS \u00b7 BBC"),
    (42, "Da Nang", "ASIA", "Tu-95s leave Vietnam; Taiwan tracks", "AP \u00b7 DEFENCE BLOG"),
    (43, "Tokyo", "ASIA", "India\u2013Japan 4th 2+2 dialogue held", "GLOBAL NEWSWIRE"),
    (44, "Washington", "AMERICAS", "US seeks SCOTUS aid on Venezuela TPS", "APPISTOS"),
    (45, "Berlin", "EUROPE", "UK pledges 1,000 long-range drones", "GOV.UK \u00b7 BYTES EU"),
    (46, "Shenzhen", "ASIA", "China pledges $20m for APEC fund", "CHINA DAILY"),
    (47, "Brussels", "EUROPE", "EU delays methane rules by 2 yrs", "COUNCIL OF EU"),
    (48, "Kyiv", "EUROPE", "Russia fires 98 drones; 69 downed", "UKRINFORM \u00b7 INTERFAX \u00b7 ISW"),
]

STATS = [
    ("3", "presidents at one table"),
    ("99", "Metacritic \u2014 GTA VI"),
    ("$81.3bn", "Anthropic's record IPO"),
    ("9\u20136", "ICJ genocide ruling"),
    ("109\u20130", "Arctic pact vote"),
    ("4.9%", "Australia jobless rate"),
]

HOURS = ("00:00 Auckland GTA VI opens \u00b7 08:40 Seoul Suneung \u00b7 10:00 Hague ICJ ruling \u00b7 "
         "11:50 NY ANT $111.50 \u00b7 14:10 Antalya COP31 draft \u00b7 Evening Shenzhen summit \u00b7 "
         "Night DC Senate 51\u201348")

DATECHECK = ("EU \u20ac45bn Ukraine loan plan (18 Nov) \u00b7 Van Gogh sells for $190.4m record (18 Nov) \u00b7 Nvidia results "
             "(18 Nov) \u00b7 Jeffries named US speaker (18 Nov) \u00b7 Sudan court sentences RSF chief Hemedti (18 Nov) \u00b7 "
             "Canada\u2013China $400m tariff relief (18 Nov) \u00b7 Gas Husky tanker sunk off Bulgaria (17 Nov) \u00b7 "
             "San Francisco rain record 2.28in (18 Nov)")

# lon/lat per story number for the map
COORDS = {
    1: (114, 22), 2: (-74, 40), 3: (4, 52), 4: (30, 36), 5: (85, 20),
    6: (127, 37), 7: (34, 44), 8: (46, 24), 9: (12, 55), 10: (149, -35),
    11: (90, 23), 12: (-77, 38), 13: (-30, 26),
    14: (-74, 4), 15: (106, -6), 16: (129, 35), 17: (36, -1), 18: (-80, 26),
    19: (2, 48), 20: (34, 31), 21: (36, 32), 22: (12, 41), 23: (45, 2),
    24: (28, -25), 25: (174, -41), 26: (8, 47), 27: (38, 45), 28: (-75, 40),
    29: (139, 35), 30: (44, 15), 31: (116, 24), 32: (0, 51), 33: (20, 44),
    34: (-99, 19), 35: (13, 52), 36: (-175, -21), 37: (-160, -21), 38: (36, 29),
    39: (37, 55), 40: (176, -37), 41: (-17, 14), 42: (108, 16), 43: (141, 37),
    44: (-79, 36), 45: (15, 50), 46: (112, 20), 47: (4, 50), 48: (30, 50),
}
REGIONS = {}
for _n, _k, _r, *_ in LEADS:
    REGIONS[_n] = _r
for _n, _k, _r, *_ in MIDS:
    REGIONS[_n] = _r
for _n, _p, _r, *_ in BRIEFS:
    REGIONS[_n] = _r

# Hand-drawn landmass mask (60 cols x 30 rows), '#' = land
MASK = [
    "                                                            ",
    "      #####                                  ##########     ",
    "    #########   ##        #                 ############    ",
    "   ########### #####     ###               ##############   ",
    "    #########  ######   #####    ##       ################  ",
    "     ########  #####   ###############################      ",
    "      #######   ###     ############################        ",
    "       ######    ##      #########################          ",
    "        #####            #######################            ",
    "        ######    ##      ####################              ",
    "         #####   ####      #################                ",
    "         #####  ######      ##############                  ",
    "          ####   ####        ############                   ",
    "          #####   ##          ##########                    ",
    "           ####                ########                     ",
    "           #####                ######                      ",
    "           ######                ####                       ",
    "            #####                ###                        ",
    "            ######               ##                         ",
    "             #####                                          ",
    "             ######                      #########          ",
    "              #####                     ###########         ",
    "              ####                       #########          ",
    "              ###                         #######           ",
    "              ##                           #####            ",
    "              #                             ###          #  ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
]


# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def num_badge(d, cx, cy, n, r=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = F(DEJA, 10 if n < 10 else 9)
    s = str(n)
    d.text((cx - tw(d, s, f) / 2, cy - 6), s, font=f, fill=WHITE)


# ---------------------------------------------------------------- illustrations
def ill_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 58, 84))
    # flags: US (stripes), China (red+star dots), Russia (white/blue/red)
    fw, fh = 52, 30
    fx = [x + 18, x + w // 2 - fw // 2, x + w - 18 - fw]
    for i, fx0 in enumerate(fx):
        d.rectangle([fx0, y + 8, fx0 + fw, y + 8 + fh], fill=WHITE, outline=(10, 10, 10))
    for i in range(4):
        d.rectangle([fx[0], y + 10 + i * 7, fx[0] + fw, y + 13 + i * 7], fill=RED)
    d.rectangle([fx[0], y + 8, fx[0] + 22, y + 22], fill=NAVY)
    d.rectangle([fx[1], y + 8, fx[1] + fw, y + 8 + fh], fill=(200, 30, 30))
    for sx, sy in [(6, 5), (16, 3), (18, 9), (16, 15), (11, 19)]:
        d.ellipse([fx[1] + sx, y + 8 + sy, fx[1] + sx + 3, y + 11 + sy], fill=GOLD)
    d.rectangle([fx[2], y + 8, fx[2] + fw, y + 18], fill=WHITE)
    d.rectangle([fx[2], y + 18, fx[2] + fw, y + 28], fill=(46, 95, 138))
    d.rectangle([fx[2], y + 28, fx[2] + fw, y + 38], fill=(200, 30, 30))
    # three leaders: heads + suits
    names = ["TRUMP", "XI", "PUTIN"]
    suits = [(30, 40, 70), (90, 25, 25), (45, 45, 55)]
    skins = [(240, 200, 160), (245, 210, 170), (238, 205, 175)]
    for i in range(3):
        cx = x + w // 4 + i * (w // 4) - (w // 8 if i == 0 else 0) + (0 if i else 0)
        cx = x + int(w * (0.22 + 0.28 * i))
        hy = y + h - 42
        d.ellipse([cx - 11, hy - 22, cx + 11, hy], fill=skins[i])
        d.rectangle([cx - 17, hy, cx + 17, hy + 26], fill=suits[i])
        d.polygon([(cx - 4, hy + 2), (cx + 4, hy + 2), (cx, hy + 14)], fill=WHITE)
        d.line([cx, hy + 4, cx, hy + 16], fill=RED, width=2)
    # table + name plates
    d.rectangle([x + 14, y + h - 18, x + w - 14, y + h - 4], fill=(120, 84, 40))
    pf = F(SANSB, 9)
    for i, nm in enumerate(names):
        cx = x + int(w * (0.22 + 0.28 * i))
        d.rectangle([cx - 24, y + h - 16, cx + 24, y + h - 6], fill=WHITE)
        d.text((cx - tw(d, nm, pf) / 2, y + h - 15), nm, font=pf, fill=INK)


def ill_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 62, 40))
    # grid + rising candlesticks
    for gx in range(x + 14, x + w - 10, 26):
        d.line([gx, y + 8, gx, y + h - 26], fill=(30, 90, 58), width=1)
    pts = []
    n = 9
    for i in range(n):
        cx = x + 16 + i * ((w - 90) // n)
        base = y + h - 34 - int((h - 48) * (i / (n - 1)) ** 1.4)
        d.line([cx + 6, base - 8, cx + 6, base + 16], fill=(90, 220, 130), width=2)
        d.rectangle([cx, base, cx + 12, base + 12], fill=(90, 220, 130))
        pts.append((cx + 6, base - 4))
    d.line(pts, fill=(160, 255, 180), width=2)
    bf = F(DEJA, 30)
    d.text((x + w - 148, y + 12), "$97.17", font=bf, fill=WHITE)
    sf = F(SANSB, 15)
    d.text((x + w - 148, y + 46), "+17% CLOSE", font=sf, fill=(140, 240, 170))
    lf = F(SANSB, 11)
    d.text((x + 12, y + h - 20), "ANT \u00b7 NASDAQ", font=lf, fill=(200, 240, 210))


def ill_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 84, 104))
    # pediment + columns
    bx = x + 26
    d.polygon([(bx, y + 16), (bx + 150, y + 16), (bx + 75, y + 2)], fill=CREAM)
    d.rectangle([bx, y + 18, bx + 150, y + 24], fill=CREAM)
    for i in range(5):
        cx = bx + 8 + i * 32
        d.rectangle([cx, y + 26, cx + 14, y + h - 22], fill=CREAM)
    d.rectangle([bx - 4, y + h - 20, bx + 154, y + h - 12], fill=CREAM)
    # scales
    sx, sy = x + w - 62, y + 22
    d.line([sx, sy, sx, sy + 44], fill=GOLD, width=3)
    d.line([sx - 26, sy + 6, sx + 26, sy + 6], fill=GOLD, width=3)
    for px in (sx - 26, sx + 26):
        d.line([px, sy + 6, px - 9, sy + 24], fill=GOLD, width=1)
        d.line([px, sy + 6, px + 9, sy + 24], fill=GOLD, width=1)
        d.arc([px - 11, sy + 18, px + 11, sy + 32], 0, 180, fill=GOLD, width=2)
    d.rectangle([sx - 10, sy + 44, sx + 10, sy + 48], fill=GOLD)
    # 9-6 badge
    bf = F(DEJA, 17)
    d.ellipse([x + w - 62, y + h - 40, x + w - 6, y + h - 6], fill=RED)
    s = "9\u20136"
    d.text((x + w - 34 - tw(d, s, bf) / 2, y + h - 32), s, font=bf, fill=WHITE)


def mid_icon(d, x, y, w, h, key):
    bg = {
        "globe": (210, 228, 240), "cyclone": (200, 220, 235), "exam": (240, 230, 200),
        "bridge": (215, 205, 190), "tower": (225, 215, 200), "shield": (205, 220, 235),
        "bars": (235, 220, 215), "flame": (240, 215, 195), "capitol": (215, 220, 230),
        "game": (60, 40, 80),
    }[key]
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    if key == "globe":
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=(46, 95, 138), width=3)
        d.line([cx - 15, cy, cx + 15, cy], fill=(46, 95, 138), width=2)
        d.line([cx, cy - 15, cx, cy + 15], fill=(46, 95, 138), width=2)
        d.rectangle([cx + 22, cy - 14, cx + 27, cy + 12], outline=RED, width=2)
        d.ellipse([cx + 20, cy + 10, cx + 29, cy + 17], fill=RED)
    elif key == "cyclone":
        for r in (5, 10, 15):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(46, 95, 138), width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    elif key == "exam":
        d.rectangle([cx - 26, cy + 4, cx + 26, cy + 10], fill=(120, 84, 40))
        d.rectangle([cx - 18, cy - 8, cx + 6, cy + 3], fill=WHITE, outline=GRAY)
        d.line([cx - 14, cy - 4, cx + 2, cy - 4], fill=GRAY, width=1)
        d.line([cx - 14, cy, cx + 2, cy], fill=GRAY, width=1)
        d.polygon([(cx + 12, cy - 12), (cx + 30, cy - 6), (cx + 14, cy - 2)], fill=GOLD)
        d.polygon([(cx - 30, cy - 14), (cx - 20, cy - 16), (cx - 24, cy - 8)], fill=NAVY)
    elif key == "bridge":
        d.line([x + 8, cy + 10, x + w - 8, cy + 10], fill=NAVY, width=3)
        for px in (x + 26, x + w - 26):
            d.line([px, cy - 14, px, cy + 10], fill=NAVY, width=3)
            d.line([px, cy - 14, cx, cy + 10], fill=NAVY, width=1)
        for i in range(8):
            a = i * 45
            import math
            ex = cx + int(11 * math.cos(math.radians(a)))
            ey = cy - 4 + int(11 * math.sin(math.radians(a)))
            d.line([cx, cy - 4, ex, ey], fill=(230, 140, 20), width=2)
        d.ellipse([cx - 4, cy - 8, cx + 4, cy], fill=RED)
    elif key == "tower":
        d.polygon([(cx - 8, cy + 16), (cx - 4, cy - 18), (cx + 4, cy - 18), (cx + 8, cy + 16)], fill=NAVY)
        d.line([cx - 44, cy - 16, cx - 6, cy - 2], fill=RED, width=2)
        d.ellipse([cx - 9, cy - 5, cx - 3, cy + 1], fill=(230, 140, 20))
    elif key == "shield":
        d.polygon([(cx, cy - 17), (cx + 15, cy - 11), (cx + 15, cy + 4), (cx, cy + 18),
                   (cx - 15, cy + 4), (cx - 15, cy - 11)], outline=NAVY, width=3)
        d.rectangle([cx - 24, cy - 12, cx - 10, cy - 2], fill=RED)
        d.rectangle([cx + 10, cy - 12, cx + 24, cy - 2], fill=(46, 95, 138))
        d.line([cx + 10, cy - 12, cx + 24, cy - 2], fill=WHITE, width=1)
    elif key == "bars":
        hs = [20, 15, 10, 5]
        for i, bh in enumerate(hs):
            bx = cx - 30 + i * 16
            d.rectangle([bx, cy + 14 - bh, bx + 11, cy + 14], fill=RED if i == 3 else NAVY)
        d.line([cx - 32, cy - 12, cx + 30, cy + 8], fill=RED, width=2)
    elif key == "flame":
        d.rectangle([cx - 20, cy - 2, cx + 14, cy + 16], fill=(120, 110, 100))
        d.rectangle([cx - 14, cy + 4, cx - 6, cy + 10], fill=(60, 60, 60))
        d.polygon([(cx - 2, cy - 18), (cx + 8, cy - 4), (cx + 14, cy - 12),
                   (cx + 16, cy + 2), (cx + 2, cy + 6), (cx - 6, cy - 2)], fill=(230, 120, 20))
        d.polygon([(cx + 3, cy - 6), (cx + 9, cy + 2), (cx + 2, cy + 5)], fill=GOLD)
    elif key == "capitol":
        d.arc([cx - 16, cy - 16, cx + 16, cy + 14], 180, 360, fill=NAVY, width=3)
        d.line([cx, cy - 17, cx, cy - 22], fill=NAVY, width=2)
        d.rectangle([cx - 26, cy + 6, cx + 26, cy + 10], fill=NAVY)
        for i in range(5):
            px = cx - 22 + i * 11
            d.line([px, cy - 2, px, cy + 6], fill=NAVY, width=2)
        d.rectangle([cx - 28, cy + 12, cx + 28, cy + 15], fill=NAVY)
    elif key == "game":
        d.rounded_rectangle([cx - 30, cy - 12, cx + 30, cy + 12], 10, outline=WHITE, width=3)
        d.line([cx - 20, cy, cx - 10, cy], fill=WHITE, width=3)
        d.line([cx - 15, cy - 5, cx - 15, cy + 5], fill=WHITE, width=3)
        for dx, dy in [(16, -4), (24, 2), (16, 6)]:
            d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=GOLD)
        gf = F(SANSB, 12)
        d.text((cx - 8, cy - 22), "VI", font=gf, fill=(255, 150, 80))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 16
    CW = W - 2 * MX

    # region counts from data + assert
    counts = {}
    for r in REGIONS.values():
        counts[r] = counts.get(r, 0) + 1
    total = sum(counts.values())
    assert total == 48, f"story total {total} != 48"
    assert len(LEADS) + len(MIDS) + len(BRIEFS) == 48
    print("region counts:", counts, "total:", total)

    # ---- masthead (y 8..100)
    kf = F(SANSB, 12)
    d.text((MX, 10), "THE WORLD IN ONE DAY", font=kf, fill=(150, 116, 20))
    df = F(SERIF, 47)
    d.text((MX, 26), "Thursday 19 November 2026", font=df, fill=NAVY)
    sf = F("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", 14)
    d.text((MX, 80), "Trump, Xi and Putin share one table \u00b7 Anthropic's record $81.3bn debut \u00b7 "
                     "World Court finds genocide in Myanmar", font=sf, fill=RED)
    # top-right box
    bx, by, bw, bh = W - MX - 196, 10, 196, 62
    d.rectangle([bx, by, bx + bw, by + bh], outline=NAVY, width=2)
    bf1 = F(DEJA, 19)
    s = "48 STORIES"
    d.text((bx + bw / 2 - tw(d, s, bf1) / 2, by + 7), s, font=bf1, fill=NAVY)
    bf2 = F(SANSB, 11)
    s2 = "6 CONTINENTS \u00b7 ONE PAGE"
    d.text((bx + bw / 2 - tw(d, s2, bf2) / 2, by + 36), s2, font=bf2, fill=RED)
    d.line([MX, 100, W - MX, 100], fill=NAVY, width=2)

    # ---- region strip (y 104..126)
    order = ["ASIA", "EUROPE", "MIDDLE EAST", "AMERICAS", "OCEANIA", "AFRICA", "GLOBAL"]
    x = MX
    y0 = 104
    rf = F(SANSB, 12)
    minw = {"GLOBAL": 74, "AFRICA": 84, "OCEANIA": 96, "MIDDLE EAST": 118}
    widths = {r: max(CW * counts[r] // 48, minw.get(r, 0)) for r in order}
    extra = sum(widths.values()) - CW
    for r in ("EUROPE", "ASIA", "AMERICAS"):  # trim the excess from the widest segments
        cut = min(extra, widths[r] - 90)
        widths[r] -= cut
        extra -= cut
    widths["GLOBAL"] += (MX + CW) - (MX + sum(widths.values()))
    for r in order:
        seg_w = widths[r]
        d.rectangle([x, y0, x + seg_w, y0 + 22], fill=REGION_COLORS[r])
        label = f"{r} {counts[r]}"
        d.text((x + seg_w / 2 - tw(d, label, rf) / 2, y0 + 4), label, font=rf, fill=WHITE)
        x += seg_w

    # ---- stat strip (y 130..166)
    y0 = 130
    cell = CW // 6
    nf, cf = F(DEJA, 21), F(SANS, 10)
    for i, (num, cap) in enumerate(STATS):
        cx0 = MX + i * cell
        d.text((cx0 + 6, y0), num, font=nf, fill=RED if i % 2 == 0 else NAVY)
        lines = wrap(d, cap, cf, cell - 12)
        yy = y0 + 25
        for ln in lines[:1]:
            d.text((cx0 + 6, yy), ln, font=cf, fill=INK)
        if i > 0:
            d.line([cx0, y0 + 2, cx0, y0 + 32], fill=(200, 190, 165), width=1)
    d.line([MX, 168, W - MX, 168], fill=NAVY, width=1)

    # ---- leads (y 172..430)
    y0 = 172
    gap = 8
    cardw = (CW - 2 * gap) // 3
    cardh = 256
    ill = {1: ill_summit, 2: ill_ipo, 3: ill_icj}
    kf2, hf, df2 = F(SANSB, 10), F(SERIF, 26), F(SANS, 13)
    for i, (n, kick, reg, head, desc) in enumerate(LEADS):
        cx0 = MX + i * (cardw + gap)
        d.rectangle([cx0, y0, cx0 + cardw, y0 + cardh], fill=CARD, outline=(205, 195, 170))
        ill[n](d, cx0 + 4, y0 + 4, cardw - 8, 92)
        yy = y0 + 102
        d.rectangle([cx0 + 8, yy + 1, cx0 + 14, yy + 11], fill=REGION_COLORS[reg])
        d.text((cx0 + 18, yy), kick, font=kf2, fill=RED)
        num_badge(d, cx0 + cardw - 16, yy + 6, n)
        yy += 15
        yy = text_block(d, cx0 + 8, yy, head, hf, NAVY, cardw - 16, 28, max_lines=2)
        yy += 2
        text_block(d, cx0 + 8, yy, desc, df2, INK, cardw - 16, 15)

    # ---- mids (y 434..630), 2 rows x 5
    y0 = 434
    mgap = 6
    mcardw = (CW - 4 * mgap) // 5
    mcardh = 96
    mkf, mhf, mdf = F(SANSB, 8), F(SANSB, 15), F(SANS, 11)
    for idx, (n, kick, reg, head, desc, icon) in enumerate(MIDS):
        r_, c_ = divmod(idx, 5)
        cx0 = MX + c_ * (mcardw + mgap)
        cy0 = y0 + r_ * (mcardh + 4)
        d.rectangle([cx0, cy0, cx0 + mcardw, cy0 + mcardh], fill=CARD, outline=(205, 195, 170))
        mid_icon(d, cx0 + 3, cy0 + 3, mcardw - 6, 32, icon)
        d.ellipse([cx0 + 4, cy0 + 4, cx0 + 20, cy0 + 20], fill=RED, outline=WHITE, width=1)
        nf_b = F(DEJA, 9 if n < 10 else 8)
        ns = str(n)
        d.text((cx0 + 12 - tw(d, ns, nf_b) / 2, cy0 + 6), ns, font=nf_b, fill=WHITE)
        yy = cy0 + 37
        assert tw(d, head, mhf) <= mcardw - 10, f"mid headline too wide: {head}"
        d.text((cx0 + 5, yy), head, font=mhf, fill=NAVY)
        yy += 18
        text_block(d, cx0 + 5, yy, desc, mdf, INK, mcardw - 10, 13, max_lines=3)

    # ---- bottom band (y 636..920): map left, briefs right
    y0 = 636
    tf = F(SANSB, 13)
    d.text((MX, y0), "WHERE IT HAPPENED", font=tf, fill=NAVY)
    mapx, mapy, mapw, maph = MX, y0 + 20, 260, 218
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=SEA)
    cols, rows = 60, 30
    cw_, ch_ = mapw / cols, maph / rows
    for ri, row in enumerate(MASK):
        for ci, ch in enumerate(row.ljust(cols)[:cols]):
            if ch == "#":
                d.rectangle([mapx + ci * cw_, mapy + ri * ch_,
                             mapx + (ci + 1) * cw_ + 0.6, mapy + (ri + 1) * ch_ + 0.6], fill=CREAM)
    def proj(lon, lat):
        return (mapx + (lon + 170) / 360 * mapw, mapy + (78 - lat) / 140 * maph)
    # brief dots first, then numbered 1-13 on top
    for n in range(14, 49):
        px, py = proj(*COORDS[n])
        col = REGION_COLORS[REGIONS[n]]
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=col)
    nf2 = F(DEJA, 8)
    for n in range(1, 14):
        px, py = proj(*COORDS[n])
        col = REGION_COLORS[REGIONS[n]]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=WHITE, width=1)
        s = str(n)
        d.text((px - tw(d, s, nf2) / 2, py - 5), s, font=nf2, fill=WHITE)
    # legend (2 rows under map)
    lf = F(SANS, 9)
    lx, ly = MX, mapy + maph + 5
    for i, r in enumerate(order):
        col_i, row_i = i % 4, i // 4
        ex = lx + col_i * 66
        ey = ly + row_i * 13
        d.rectangle([ex, ey + 1, ex + 8, ey + 9], fill=REGION_COLORS[r])
        d.text((ex + 11, ey), r.title() if r != "MIDDLE EAST" else "Mid. East", font=lf, fill=INK)

    # briefs right: 2 columns
    bx0 = MX + 276
    bw2 = W - MX - bx0
    colw = (bw2 - 10) // 2
    d.text((bx0, y0), "ALSO ON THURSDAY 19 NOVEMBER", font=tf, fill=NAVY)
    nf3, pf, tf3, srcf = F(DEJA, 10), F(SANSB, 11), F(SANS, 11), F(SANSB, 8)
    per_col = 18
    for ci in range(2):
        cx0 = bx0 + ci * (colw + 10)
        yy = y0 + 22
        for (n, place, reg, txt, src) in BRIEFS[ci * per_col:(ci + 1) * per_col]:
            ns = f"{n}."
            d.text((cx0, yy), ns, font=nf3, fill=RED)
            xcur = cx0 + tw(d, ns, nf3) + 2
            ps = place + " "
            d.text((xcur, yy), ps, font=pf, fill=INK)
            xcur += tw(d, ps, pf)
            ts = "\u2014 " + txt + " "
            # trim at a word boundary if the whole line would overflow the column
            avail = cx0 + colw - xcur - tw(d, src, srcf) - 1
            if tw(d, ts, tf3) > avail:
                while tw(d, ts, tf3) > avail and " " in ts[:-1]:
                    ts = ts[:ts.rfind(" ", 0, len(ts) - 1)] + "\u2026 "
            d.text((xcur, yy), ts, font=tf3, fill=INK)
            xcur += tw(d, ts, tf3)
            d.text((xcur, yy + 2), src, font=srcf, fill=GRAY)
            yy += 15

    # ---- by hours (y 926..946)
    y0 = 926
    d.rectangle([MX, y0, W - MX, y0 + 20], fill=NAVY)
    hf2 = F(SANSB, 10)
    d.text((MX + 6, y0 + 4), "THE DAY BY HOURS", font=hf2, fill=GOLD)
    hx = MX + 6 + tw(d, "THE DAY BY HOURS", hf2) + 10
    htxt = HOURS
    hf3 = F(SANS, 10)
    if tw(d, htxt, hf3) > W - MX - hx - 6:
        hf3 = F(SANS, 9)
    while tw(d, htxt, hf3) > W - MX - hx - 6 and " " in htxt[:-1]:
        htxt = htxt[:htxt.rfind(" ", 0, len(htxt) - 1)]
    d.text((hx, y0 + 5), htxt, font=hf3, fill=WHITE)

    # ---- date check (y 948..984)
    y0 = 948
    d.rectangle([MX, y0, W - MX, y0 + 36], outline=RED, width=1)
    dcf = F(SANSB, 10)
    d.text((MX + 6, y0 + 3), "DATE CHECK \u2014 NOT 19 NOV, LEFT OUT ON PURPOSE:", font=dcf, fill=RED)
    dcf2 = F(SANS, 9)
    lines = wrap(d, DATECHECK, dcf2, CW - 12)
    yy = y0 + 15
    for ln in lines[:2]:
        d.text((MX + 6, yy), ln, font=dcf2, fill=INK)
        yy += 10

    # ---- footer (y 988..1014)
    y0 = 988
    ff = F(SANS, 10)
    d.text((MX, y0), "Every story above happened, or was first reported, on Thursday 19 November 2026 "
                     "(any time zone). Claims are attributed, not stated as fact.", font=ff, fill=INK)
    d.text((MX, y0 + 13), "Pictures and map: original, drawn in code. Wires: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 "
                          "Al Jazeera \u00b7 Yonhap \u00b7 Euronews \u00b7 Ukrinform \u00b7 IMD \u00b7 ABS \u00b7 gov.uk \u00b7 ReliefWeb \u00b7 ISW",
           font=ff, fill=GRAY)

    img = img.quantize(colors=256, dither=Image.Dither.FLOYDSTEINBERG)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
