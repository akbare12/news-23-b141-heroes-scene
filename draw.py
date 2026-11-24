#!/usr/bin/env python3
"""news-23 b141 heroes-scene: draw THE WORLD TODAY, Monday 23 November 2026."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (169, 28, 34)
DARKRED = (140, 20, 26)
NAVY = (20, 38, 74)
GOLD = (176, 141, 40)
GOLDLT = (201, 162, 39)
GREEN = (30, 107, 58)
TEAL = (14, 116, 116)
PURPLE = (128, 60, 140)
MAPGREEN = (198, 220, 178)
MAPLINE = (120, 160, 110)
GREY = (90, 90, 90)
LIGHT = (238, 232, 216)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, font_path, size, max_w, min_size=11):
    s = size
    while s > min_size:
        f = F(font_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return F(font_path, min_size)


def chip(draw, x, y, text, fill):
    f = F(SANS_B, 10)
    w = int(draw.textlength(text, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- frame ----
d.rectangle([0, 0, W - 1, H - 1], outline=GOLD, width=3)
d.rectangle([6, 6, W - 7, H - 7], outline=GOLD, width=1)

# ---- masthead ----
d.text((14, 12), "THE WORLD TODAY", font=F(SERIF_B, 46), fill=INK)
d.text((1010, 30), "MONDAY 23 NOVEMBER 2026", font=F(SANS_B, 15),
       fill=GOLD, anchor="ra")

# ---- kicker (red bar) ----
d.rectangle([10, 66, 1014, 90], fill=RED)
kicker = "AI rout hits Asia   \u00b7   UN chief urges AI rules   \u00b7   " \
         "US lead over China at record low   \u00b7   Anthropic IPO $107.3B"
d.text((512, 71), kicker, font=F(SANS_B, 14), fill=(255, 255, 255), anchor="ma")

# ---- number strip: 2 rows x 5 cols ----
nums = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
col_w = 1004 // 5
for i, (val, lab) in enumerate(nums):
    r, c = divmod(i, 5)
    x = 10 + c * col_w + 4
    y = 94 + r * 30
    d.text((x, y), val, font=F(SANS_B, 19), fill=INK)
    d.text((x, y + 19), lab, font=F(SANS, 9), fill=GREY)
    if c < 4:
        d.line([10 + (c + 1) * col_w, 96 + r * 30, 10 + (c + 1) * col_w,
                118 + r * 30], fill=(200, 192, 170), width=1)

# ---- region bar ----
regions = [("ASIA-PACIFIC 7", 227, NAVY), ("AMERICAS 8", 259, RED),
           ("MIDDLE EAST 6", 194, PURPLE), ("EUROPE 5", 162, TEAL),
           ("AFRICA 3", 97, GREEN), ("WORLD 2", 65, GOLD)]
x = 10
for name, wdt, col in regions:
    d.rectangle([x, 156, x + wdt, 176], fill=col)
    d.text((x + wdt / 2, 160), name, font=F(SANS_B, 11),
           fill=(255, 255, 255), anchor="ma")
    x += wdt

# ---- UTC strip ----
d.text((14, 180), "THE DAY IN UTC", font=F(SANS_B, 10), fill=INK)
utc = "~00:00 Kospi dives   ~05:30 Guterres opens   ~09:00 Power Index   " \
      "~12:00 Paris 2% tax   ~15:00 Kyiv missiles"
d.text((150, 180), utc, font=F(SANS, 10), fill=GREY)
d.text((1010, 180), "~ APPROX", font=F(SANS, 10), fill=GREY, anchor="ra")

# ---- hero scenes ----
HX = [10, 348, 686]
HW = 328
HY = 196
SCENE_H = 148


def hero_scene_kospi(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 28, 54))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x0 + 8
    while bx < x0 + w - 30:
        bw = rnd.randint(22, 34)
        bh = rnd.randint(52, 96)
        by = y0 + h - 26 - bh
        d.rectangle([bx, by, bx + bw, y0 + h - 26], fill=(28, 48, 84))
        for wy in range(by + 6, y0 + h - 30, 10):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 110))
        bx += bw + 6
    # descending chart line
    pts = [(x0 + 120, y0 + 46), (x0 + 160, y0 + 58), (x0 + 210, y0 + 62),
           (x0 + 262, y0 + 82), (x0 + 310, y0 + 96)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 6), "-3.3%", font=F(SANS_B, 34), fill=(255, 255, 255))
    d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(0, 0, 0))
    d.text((x0 + 8, y0 + h - 22), "KOSPI 4,708.54 \u00b7 -161 PTS \u00b7 SAMSUNG -3.1%",
           font=F(SANS_B, 11), fill=(255, 214, 110))


def hero_scene_guterres(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 90, 52))
    # globe on the right, clipped to a circle
    cx, cy, r = x0 + w - 62, y0 + 62, 48
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r - x0, cy - r - y0, cx + r - x0, cy + r - y0], fill=255)
    globe = Image.new("RGB", (w, h), (24, 90, 52))
    gd = ImageDraw.Draw(globe)
    gd.ellipse([cx - r - x0, cy - r - y0, cx + r - x0, cy + r - y0],
               fill=(190, 225, 200))
    for k in range(-2, 3):
        gd.arc([cx - r - x0 + 12 * abs(k), cy - r - y0,
                cx + r - x0 - 12 * abs(k), cy + r - y0],
               270 if k >= 0 else 90, 90 if k >= 0 else 270,
               fill=(120, 170, 130), width=1)
    for yy in (-24, 0, 24):
        gd.line([cx - r - x0, cy + yy - y0, cx + r - x0, cy + yy - y0],
                fill=(120, 170, 130), width=1)
    img.paste(globe, (x0, y0), mask)
    d.text((x0 + 10, y0 + 8), "150", font=F(SANS_B, 40), fill=(255, 214, 110))
    gold_lines = ["DELEGATES", "BACK A RISK", "FRAMEWORK"]
    yy = y0 + 52
    for ln in gold_lines:
        d.text((x0 + 10, yy), ln, font=F(SANS_B, 17), fill=(255, 214, 110))
        yy += 22
    d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(0, 0, 0))
    d.text((x0 + 8, y0 + h - 22), "BRIDGETOWN SUMMIT, BARBADOS",
           font=F(SANS_B, 11), fill=(255, 214, 110))


def hero_scene_power(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(250, 244, 224))
    d.text((x0 + 10, y0 + 6), "NARROWEST SINCE 2018", font=F(SANS_B, 12), fill=INK)
    d.text((x0 + w - 10, y0 + 6), "GAP 5.3", font=F(SANS_B, 12),
           fill=RED, anchor="ra")
    bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 236),
            ("40.5", "INDIA", GOLD, 130)]
    yy = y0 + 30
    for val, name, col, bw in bars:
        d.text((x0 + 10, yy), val, font=F(SANS_B, 15), fill=INK)
        bx = x0 + 62
        d.rectangle([bx, yy + 2, bx + bw, yy + 16], fill=col)
        lab_f = F(SANS_B, 11)
        tw = d.textlength(name, font=lab_f)
        d.text((bx + bw - tw - 6, yy + 3), name, font=lab_f,
               fill=(255, 255, 255))
        yy += 26
    d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(0, 0, 0))
    d.text((x0 + 8, y0 + h - 22), "ASIA POWER INDEX 2026 \u00b7 LOWY INSTITUTE",
           font=F(SANS_B, 11), fill=(255, 214, 110))


heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
     "Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", hero_scene_kospi),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit.",
     "UNITED NATIONS", hero_scene_guterres),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest "
     "since 2018. India third at 40.5.",
     "LOWY INSTITUTE", hero_scene_power),
]
for i, (head, body, src, scene_fn) in enumerate(heroes):
    x0 = HX[i]
    scene_fn(x0, HY, HW, SCENE_H)
    ty = HY + SCENE_H + 6
    hf = fit_one_line(d, head, SERIF_B, 17, HW - 4)
    d.text((x0, ty), head, font=hf, fill=INK)
    by = ty + 22
    blines = wrap(d, body, F(SANS, 12), HW - 4)
    for ln in blines[:2]:
        d.text((x0, by), ln, font=F(SANS, 12), fill=INK)
        by += 15
    sy = HY + SCENE_H + 6 + 22 + 30
    d.text((x0, sy), src, font=F(SANS, 10), fill=GREY)
    chip(d, x0 + HW - 78, sy - 1, "REPORTED", NAVY)

# ---- black bar: more of the day ----
d.rectangle([10, 452, 1014, 474], fill=(0, 0, 0))
d.text((14, 457), "MORE OF THE DAY  \u2014  10 STORIES", font=F(SANS_B, 13),
       fill=(255, 255, 255))

# ---- cards: 5 cols x 2 rows ----
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
     "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.",
     "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME",
     "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.",
     "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.",
     "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.",
     "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.",
     "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
     "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "Kyiv: 3 Kh-101s crossed.",
     "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
     "Reuters", "CLAIM"),
]
CW = 1004 // 5
for i, (num, cat, head, body, src, tag) in enumerate(cards):
    r, c = divmod(i, 5)
    x0 = 10 + c * CW
    y0 = 478 + r * 84
    d.text((x0 + 4, y0), num, font=F(SANS_B, 12), fill=RED)
    cat_f = F(SANS_B, 10)
    num_w = d.textlength(num, font=F(SANS_B, 12))
    d.text((x0 + 8 + num_w, y0 + 1), cat, font=cat_f, fill=GREY)
    hlines = wrap(d, head, F(SANS_B, 12), CW - 10)
    hy = y0 + 18
    for ln in hlines[:2]:
        d.text((x0 + 4, hy), ln, font=F(SANS_B, 12), fill=INK)
        hy += 14
    d.text((x0 + 4, y0 + 50), body, font=F(SANS, 11), fill=INK)
    d.text((x0 + 4, y0 + 66), src, font=F(SANS, 10), fill=GREY)
    chip(d, x0 + CW - 82, y0 + 64, tag, NAVY if tag == "REPORTED" else RED)
    if c < 4:
        d.line([x0 + CW, y0 + 2, x0 + CW, y0 + 80], fill=(210, 202, 180), width=1)

# ---- black bar: where it happened ----
d.rectangle([10, 646, 1014, 668], fill=(0, 0, 0))
d.text((14, 651), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=(255, 255, 255))

# ---- map (left) ----
MAPX, MAPY, MAPW, MAPH = 10, 672, 340, 128
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(232, 240, 224))
# Americas blob
d.polygon([(36, 700), (70, 682), (130, 676), (180, 690), (196, 720),
           (170, 768), (120, 792), (66, 780), (40, 748)], fill=MAPGREEN,
          outline=MAPLINE)
# Eurasia blob
d.polygon([(216, 700), (250, 684), (300, 680), (336, 694), (340, 716),
           (310, 730), (262, 728), (222, 722)], fill=MAPGREEN, outline=MAPLINE)
# Africa blob
d.polygon([(246, 736), (286, 732), (312, 744), (306, 776), (280, 796),
           (258, 782), (244, 758)], fill=MAPGREEN, outline=MAPLINE)
pins = [(330, 700, "1"), (70, 792, "2"), (312, 690, "3"), (78, 724, "4"),
        (108, 706, "5"), (288, 710, "6"), (238, 706, "7"), (236, 694, "8"),
        (272, 692, "9"), (220, 704, "10"), (292, 742, "11"), (288, 760, "12"),
        (270, 790, "13")]
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255))
    d.text((px, py - 6), n, font=F(SANS_B, 9), fill=(255, 255, 255), anchor="ma")
d.text((14, 803), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 "
       "4 Washington", font=F(SANS, 9), fill=INK)
d.text((14, 815), "5 New York \u00b7 6 Kyiv \u00b7 7 Paris \u00b7 8 London \u00b7 "
       "9 Warsaw", font=F(SANS, 9), fill=INK)
d.text((14, 827), "10 Manchester \u00b7 11 Beirut \u00b7 12 Gaza \u00b7 13 Khartoum",
       font=F(SANS, 9), fill=INK)

# ---- ALSO (right of map) ----
d.text((366, 674), "ALSO ON MONDAY", font=F(SANS_B, 13), fill=INK)
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: Antalya pact rejected", False),
    ("18. Israel unity talks resume", False),
    ("19. Gaza: two killed in Israeli strike", False),
    ("20. West Bank settler attacks", False),
    ("21. Iran war: no deal in sight", False),
    ("22. Lebanon seizes 264 kg explosives", False),
    ("23. Bahrain: strike hits plant, 2 hurt", False),
    ("24. Benghazi: UN demands probe", True),
    ("25. Sudan: defences down drones", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits over AI exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
for i, (txt, is_claim) in enumerate(also):
    col = i // 9
    row = i % 9
    x = 366 + col * 330
    y = 694 + row * 16
    d.text((x, y), txt, font=F(SANS, 11), fill=INK)
    if is_claim:
        tw = d.textlength(txt, font=F(SANS, 11))
        d.text((x + tw + 4, y), "[CLAIM]", font=F(SANS_B, 10), fill=RED)

# ---- DATE CHECK red box ----
d.rectangle([10, 840, 1014, 916], outline=RED, width=2)
d.text((18, 846), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  "
       "STORIES DATED 23 NOV ONLY", font=F(SANS_B, 12), fill=RED)
d.text((18, 864), "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  "
       "Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7",
       font=F(SANS, 11), fill=INK)
d.text((18, 880), "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  "
       "\u00b7  ICJ Myanmar ruling (19 Nov)", font=F(SANS, 11), fill=INK)
d.text((18, 896), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  "
       "4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  "
       "WHO evacuating trapped Ebola staff", font=F(SANS, 11), fill=INK)

# ---- footer ----
d.text((14, 924), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 "
       "Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute "
       "(Asia Power Index 2026).", font=F(SANS, 10), fill=GREY)
d.text((14, 940), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one "
       "side's claim, independently unconfirmed \u00b7 ONGOING = still "
       "developing.", font=F(SANS, 10), fill=GREY)
d.text((14, 956), "All times UTC. Figures as reported 23 Nov 2026. Scenes are "
       "drawn illustrations, not photographs.", font=F(SANS, 10), fill=GREY)
d.line([10, 976, 1014, 976], fill=GOLD, width=2)
d.text((512, 984), "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  "
       "31 stories  \u00b7  6 regions", font=F(SANS_B, 12), fill=GOLD,
       anchor="ma")

img.save("entry.png")
print("saved entry.png", img.size)
