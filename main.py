#!/usr/bin/env python3
"""The World Today - front page for Monday 23 November 2026.

Draws a newspaper front page summing up the day's world news, using only
the Python standard library and Pillow. Deterministic: no randomness, no
network, no timestamps. Writes /output/entry.png (1024x1024, <= 1 MiB).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
PATH = os.path.join(OUT, "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit within width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill, leading=None):
    """Draw a wrapped paragraph; returns y after the last line."""
    if leading is None:
        leading = fnt.size + 5
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=(20, 20, 20)):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_scene(draw, x, y, w, h):
    """Stylised illustration for the COP31 story: a globe above a summit
    hall, with a crack running through the globe and a broken deal ribbon."""
    # sky
    draw.rectangle([x, y, x + w, y + h], fill=(38, 64, 96))
    # stars
    for sx, sy, r in [(60, 22, 2), (150, 48, 2), (240, 18, 3), (330, 40, 2),
                      (430, 16, 2), (520, 44, 2), (610, 20, 3), (700, 46, 2),
                      (790, 24, 2), (880, 40, 2), (940, 18, 2)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                     fill=(240, 235, 210))
    # ground / hall
    draw.rectangle([x, y + h - 62, x + w, y + h], fill=(24, 28, 34))
    # hall columns
    for cx in range(60, w - 40, 110):
        draw.rectangle([x + cx, y + h - 118, x + cx + 26, y + h - 62],
                       fill=(210, 205, 185))
    draw.rectangle([x + 30, y + h - 128, x + w - 30, y + h - 118],
                   fill=(210, 205, 185))
    # globe
    gx, gy, gr = x + w // 2, y + 78, 62
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(96, 160, 110))
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(240, 235, 210),
                 width=3)
    # continents (simple blobs)
    draw.ellipse([gx - 42, gy - 34, gx - 6, gy - 4], fill=(52, 110, 66))
    draw.ellipse([gx + 4, gy + 2, gx + 40, gy + 34], fill=(52, 110, 66))
    draw.ellipse([gx - 18, gy + 18, gx + 12, gy + 44], fill=(52, 110, 66))
    # crack through the globe
    crack = [(gx - 10, gy - 62), (gx + 6, gy - 30), (gx - 8, gy - 4),
             (gx + 10, gy + 26), (gx - 4, gy + 62)]
    draw.line([(px, py) for px, py in crack], fill=(240, 235, 210), width=4)
    # "NO DEAL" ribbon across the hall
    rx0, ry = x + 30, y + h - 52
    draw.polygon([(rx0, ry), (rx0 + 190, ry), (rx0 + 178, ry + 30),
                  (rx0 - 12, ry + 30)], fill=(178, 34, 34))
    draw.text((rx0 + 22, ry + 4), "NO DEAL", font=font(SANS_B, 20),
              fill=(255, 255, 255))
    # caption
    draw.text((x + w - 330, y + h - 30),
              "The summit hall in Antalya, Turkey",
              font=font(SERIF_I, 15), fill=(220, 215, 195))


def main():
    img = Image.new("RGB", (W, H), (247, 243, 232))
    d = ImageDraw.Draw(img)
    ink = (18, 18, 18)
    red = (158, 28, 28)
    mx = 30                      # side margin
    rx = W - mx                  # right edge

    # ---- top strip -------------------------------------------------------
    rule(d, mx, 16, rx, 3)
    d.text((mx, 24), "EST. 2026  ·  THE WORLD IN ONE DAY",
           font=font(SANS_B, 13), fill=ink)
    d.text((rx - 250, 24), "No. 327  ·  FREE TO READ", font=font(SANS_B, 13),
           fill=ink)
    # masthead
    mast = font(SERIF_B, 84)
    d.text((W // 2, 44), "THE WORLD TODAY", font=mast, fill=ink, anchor="ma")
    rule(d, mx, 138, rx, 2)
    d.text((W // 2, 146), "MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=red, anchor="ma")
    d.text((W // 2, 168), "The day's biggest stories, from every continent, on one page",
           font=font(SERIF_I, 16), fill=(70, 70, 70), anchor="ma")
    rule(d, mx, 196, rx, 4)

    # ---- lead story: COP31 ----------------------------------------------
    y = 210
    d.text((mx, y), "CLIMATE  ·  ANTALYA, TURKEY", font=font(SANS_B, 15),
           fill=red)
    y += 24
    head = font(SERIF_B, 58)
    d.text((mx, y), "CLIMATE TALKS COLLAPSE", font=head, fill=ink)
    y += 66
    sub = ("COP31 ends with no deal at all, two days past its deadline, after "
           "the European Union and others reject a draft that says nothing "
           "about fossil fuels.")
    y = para(d, mx, y, rx - mx, sub, font(SERIF, 19), ink, leading=25)
    y += 6
    draw_lead_scene(d, mx, y, rx - mx, 168)
    y += 168 + 10
    lead_body = ("The United Nations climate summit in Antalya broke up on "
                 "Sunday without an agreement, leaving the world with no new "
                 "plan to cut emissions as extreme weather worsens. Delegates "
                 "said the talks had been fractious from the start, and "
                 "activists called the outcome a failure years in the making.")
    y = para(d, mx, y, rx - mx, lead_body, font(SERIF, 16), ink, leading=21)
    rule(d, mx, y + 8, rx, 2)

    # ---- secondary stories, two columns ----------------------------------
    col_w = (rx - mx - 24) // 2
    left_x, right_x = mx, mx + col_w + 24
    sy = y + 20
    kick = font(SANS_B, 13)
    hfont = font(SERIF_B, 23)
    bfont = font(SERIF, 15)

    stories_left = [
        ("GULF  ·  BAHRAIN", "Iran strikes Bahrain site; two hurt",
         "Iranian projectiles hit an industrial site in Bahrain, injuring "
         "two people, as Gulf states condemn the attack and tensions rise "
         "around the Strait of Hormuz."),
        ("MEXICO  ·  SINALOA", "Cartel boss \u2018El Chapo Isidro\u2019 captured; 11 killed",
         "Special forces seize Fausto Isidro Meza Flores in a bloody raid in "
         "Sinaloa. Eleven people died, including four soldiers."),
        ("UKRAINE  ·  NEAR KYIV", "Drone hits flats; 14 missing",
         "A Russian drone strikes a five-storey apartment block in Dymer, "
         "north of Kyiv. A missile on Kryvyi Rih kills two and wounds 60."),
    ]
    stories_right = [
        ("INDONESIA  ·  BANTEN", "Factory fire kills 3; 37 missing",
         "A blaze at a candy factory in Cikande leaves three workers dead "
         "and dozens unaccounted for as rescuers search the ruins."),
        ("SPACE  ·  MERCURY", "BepiColombo reaches Mercury",
         "Two spacecraft enter orbit around Mercury after an eight-year "
         "journey, opening a new chapter in the study of the innermost "
         "planet."),
        ("TRADE  ·  BRUSSELS", "EU and Indonesia sign trade deal",
         "After almost ten years of talks, the two sides scrap tariffs on up "
         "to 98.5% of goods in a landmark agreement."),
    ]

    def column(x, stories, start_y):
        cy = start_y
        for kicker, headline, body in stories:
            d.text((x, cy), kicker, font=kick, fill=red)
            cy += 19
            for line in wrap(d, headline, hfont, col_w):
                d.text((x, cy), line, font=hfont, fill=ink)
                cy += 28
            cy = para(d, x, cy + 2, col_w, body, bfont, (50, 50, 50),
                      leading=19)
            cy += 12
            rule(d, x, cy, x + col_w, 1, fill=(150, 145, 130))
            cy += 12
        return cy

    ly = column(left_x, stories_left, sy)
    ry = column(right_x, stories_right, sy)
    bottom = max(ly, ry)

    # ---- footer ticker ----------------------------------------------------
    ty = H - 62
    rule(d, mx, ty - 8, rx, 2)
    d.rectangle([mx, ty, rx, H - 26], fill=(18, 18, 18))
    ticker = ("ALSO TODAY:  Boat capsizes in Nigeria, 24 dead  ·  "
              "Settlers torch West Bank vehicles  ·  "
              "Democrats take 258 House seats")
    d.text((W // 2, ty + 10), ticker, font=font(SANS_B, 13),
           fill=(245, 242, 230), anchor="ma")
    d.text((W // 2, H - 20), "THE WORLD TODAY  ·  Monday 23 November 2026",
           font=font(SANS, 11), fill=(90, 85, 75), anchor="ma")

    os.makedirs(OUT, exist_ok=True)
    img.save(PATH, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
