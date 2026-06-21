# -*- coding: utf-8 -*-
"""ゼティス羽根 鼻整形シリーズ お悩み編 3列グリッド（表紙）モックアップ
お渡し資料「お悩み・印象 目次」5カテゴリ準拠 / 1行＝1カテゴリで色を揃える(B案)"""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

COLS = 3
TILE = 360
GAP = 5
MARGIN = 26
HEADER_H = 250
FOOTER_H = 70

CAT = {
    "鼻先":     ("#B98C8C", "#FFFFFF"),
    "鼻筋":     ("#B49A6E", "#FFFFFF"),
    "小鼻・鼻の穴": ("#8FA088", "#FFFFFF"),
    "全体・横顔":  ("#A28DA6", "#FFFFFF"),
    "専門・顔立":  ("#423D38", "#F4ECE0"),
}

# (番号, カテゴリ, タイトル行, 解決術式の小ラベル)
POSTS = [
    ("01", "鼻先",     ["団子鼻"],            "鼻尖形成＋軟骨移植"),
    ("02", "鼻先",     ["鼻先が", "丸い"],     "鼻尖形成"),
    ("03", "鼻先",     ["鼻先が", "大きい"],    "鼻尖形成＋移植"),
    ("04", "鼻筋",     ["鼻筋が", "低い"],     "プロテーゼ/自家組織"),
    ("05", "鼻筋",     ["わし鼻"],            "ハンプ切除"),
    ("06", "鼻筋",     ["鼻筋が", "太い"],     "骨切り幅寄せ"),
    ("07", "小鼻・鼻の穴", ["小鼻が", "大きい"],   "鼻翼縮小"),
    ("08", "小鼻・鼻の穴", ["鼻の穴が", "目立つ"], "鼻翼縮小/鼻孔縁挙上"),
    ("09", "小鼻・鼻の穴", ["四角い鼻"],          "鼻尖形成＋小鼻"),
    ("10", "全体・横顔",  ["豚鼻・", "短い鼻"],   "鼻中隔延長"),
    ("11", "全体・横顔",  ["横顔の", "バランス"], "鼻中隔延長/鼻柱下降"),
    ("12", "全体・横顔",  ["のっぺり", "鼻"],     "隆鼻＋鼻尖形成"),
    ("13", "専門・顔立",  ["左右差・", "曲がり鼻"], "骨切り＋鼻中隔"),
    ("14", "専門・顔立",  ["先天的・", "難症例"],  "肋軟骨 構造手術"),
    ("15", "専門・顔立",  ["トータル", "デザイン"], "全顔バランス相談"),
]

rows = (len(POSTS) + COLS - 1) // COLS
W = MARGIN * 2 + COLS * TILE + (COLS - 1) * GAP
H = HEADER_H + rows * TILE + (rows - 1) * GAP + FOOTER_H

img = Image.new("RGB", (W, H), "#FBF8F3")
d = ImageDraw.Draw(img)


def font(sz):
    return ImageFont.truetype(FONT, sz)


def text_w(s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


gold = "#B49A6E"
dark = "#423D38"
cy = 70
d.ellipse([MARGIN, cy - 50, MARGIN + 100, cy + 50], outline=gold, width=3)
d.text((MARGIN + 50, cy), "Z", font=font(40), fill=gold, anchor="mm")
d.text((MARGIN + 125, 45), "zetith_hane", font=font(34), fill=dark)
d.text((MARGIN + 125, 90), "ゼティス羽根 / 鼻整形", font=font(24), fill="#8A7866")
d.text((MARGIN, 155), "鼻整形シリーズ｜お悩み編", font=font(38), fill=dark)
d.text((MARGIN, 205), "1行＝1カテゴリ（お渡し資料準拠）", font=font(22), fill="#8A7866")

items = list(CAT.keys())
for i, name in enumerate(items):
    col = i % 2
    row = i // 2
    bx = W - MARGIN - 290 + col * 150
    by = 145 + row * 30
    bg, _ = CAT[name]
    d.rectangle([bx, by, bx + 20, by + 20], fill=hx(bg))
    d.text((bx + 28, by + 10), name, font=font(18), fill=dark, anchor="lm")


def fit_font(lines, maxw, start=52, minsz=26):
    sz = start
    while sz > minsz:
        f = font(sz)
        if all(text_w(l, f) <= maxw for l in lines):
            return f
        sz -= 2
    return font(minsz)


for idx, (num, cat, lines, sol) in enumerate(POSTS):
    r = idx // COLS
    c = idx % COLS
    x = MARGIN + c * (TILE + GAP)
    y = HEADER_H + r * (TILE + GAP)
    bg, fg = CAT[cat]
    d.rectangle([x, y, x + TILE, y + TILE], fill=hx(bg))
    d.rectangle([x + 14, y + 14, x + TILE - 14, y + TILE - 14], outline=hx(fg), width=2)
    d.text((x + 30, y + 34), num, font=font(26), fill=fg, anchor="lm")
    d.text((x + TILE / 2, y + 58), "お悩み", font=font(20), fill=fg, anchor="mm")
    d.line([x + TILE / 2 - 26, y + 80, x + TILE / 2 + 26, y + 80], fill=fg, width=1)
    f = fit_font(lines, TILE - 70, start=56, minsz=28)
    asc = (f.getbbox("あ")[3] - f.getbbox("あ")[1])
    lh = asc + 16
    total = lh * len(lines)
    ty = y + TILE / 2 - total / 2 + asc / 2
    for l in lines:
        d.text((x + TILE / 2, ty), l, font=f, fill=fg, anchor="mm")
        ty += lh
    # 解決術式の小ラベル（下部）
    d.text((x + TILE / 2, y + TILE - 58), "→ " + sol, font=font(17), fill=fg, anchor="mm")
    d.text((x + TILE / 2, y + TILE - 32), "ZETITH HANE", font=font(15), fill=fg, anchor="mm")

d.text((W / 2, H - FOOTER_H / 2), "※表紙イメージ（仮）｜悩み→術式編へ誘導　数値・症例は医師監修で確定",
       font=font(20), fill="#8A7866", anchor="mm")

out = "/home/user/pictweet1/instagram-content/grid_mockup_お悩み編.png"
img.save(out)
print("saved", out, img.size)
