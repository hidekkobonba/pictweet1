# -*- coding: utf-8 -*-
"""ゼティス羽根 鼻整形シリーズ Instagram 3列グリッド（表紙）モックアップ生成"""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

# ---- レイアウト ----
COLS = 3
TILE = 360
GAP = 5
MARGIN = 26
HEADER_H = 250
FOOTER_H = 70

# カテゴリ色（上品・くすみトーン / 白orクリーム文字）
CAT = {
    "導入":   ("#423D38", "#F4ECE0"),
    "鼻先":   ("#B98C8C", "#FFFFFF"),
    "鼻筋":   ("#B49A6E", "#FFFFFF"),
    "小鼻系": ("#8FA088", "#FFFFFF"),
    "周辺":   ("#A28DA6", "#FFFFFF"),
    "まとめ": ("#8A7866", "#F4ECE0"),
}

# 投稿順（フィードに並ぶ順）: (番号, カテゴリ, タイトル行リスト)
POSTS = [
    ("01", "導入",   ["クローズド法"]),
    ("02", "導入",   ["オープン法"]),
    ("03", "鼻先",   ["鼻尖形成"]),
    ("04", "鼻先",   ["軟骨移植"]),
    ("05", "鼻先",   ["ストラット"]),
    ("06", "鼻先",   ["鼻中隔延長", "（耳軟骨）"]),
    ("07", "鼻先",   ["鼻中隔延長", "（肋軟骨）"]),
    ("08", "鼻筋",   ["プロテーゼ"]),
    ("09", "鼻筋",   ["自家組織", "隆鼻"]),
    ("10", "鼻筋",   ["骨切り", "幅寄せ"]),
    ("11", "鼻筋",   ["鷲鼻削り", "ハンプ切除"]),
    ("12", "小鼻系", ["鼻翼縮小"]),
    ("13", "小鼻系", ["鼻孔縁挙上"]),
    ("14", "小鼻系", ["鼻孔縁下降"]),
    ("15", "小鼻系", ["鼻翼挙上"]),
    ("16", "小鼻系", ["鼻柱下降"]),
    ("17", "周辺",   ["貴族手術", "ゴアテックス"]),
    ("18", "周辺",   ["貴族手術", "（肋軟骨）"]),
    ("19", "周辺",   ["猫手術"]),
    ("20", "まとめ", ["軟骨の", "使い分けMAP"]),
    ("21", "まとめ", ["鼻整形", "用語辞典"]),
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


# ---------- ヘッダー（プロフィール風） ----------
gold = "#B49A6E"
dark = "#423D38"
# アカウント行
cx = MARGIN + 55
cy = 70
d.ellipse([MARGIN, cy - 50, MARGIN + 100, cy + 50], outline=gold, width=3)
f_logo = font(40)
d.text((MARGIN + 50, cy), "Z", font=f_logo, fill=gold, anchor="mm")
d.text((MARGIN + 125, 45), "zetith_hane", font=font(34), fill=dark)
d.text((MARGIN + 125, 90), "ゼティス羽根 / 鼻整形", font=font(24), fill="#8A7866")
# シリーズ見出し
d.text((MARGIN, 155), "鼻整形シリーズ｜術式編", font=font(38), fill=dark)
d.text((MARGIN, 205), "色＝部位カテゴリ　数字＝投稿順", font=font(22), fill="#8A7866")
# 凡例（右側）
lx = W - MARGIN - 250
ly = 150
for name in ["導入", "鼻先", "鼻筋", "小鼻系", "周辺", "まとめ"]:
    bg, _ = CAT[name]
    d.rectangle([lx, ly, lx + 22, ly + 22], fill=bg)
    d.text((lx + 32, ly + 11), name, font=font(20), fill=dark, anchor="lm")
    ly += 0
    lx += 0
    # 横並び2列に
# （凡例は縦に並べ直す）
d.rectangle([W - MARGIN - 260, 145, W - MARGIN, 240], outline="#E3D8C7", width=0)
# 上の凡例描画を消して整然と描き直し
d.rectangle([W - MARGIN - 262, 143, W - MARGIN + 2, 242], fill="#FBF8F3")
items = ["導入", "鼻先", "鼻筋", "小鼻系", "周辺", "まとめ"]
for i, name in enumerate(items):
    col = i % 2
    row = i // 2
    bx = W - MARGIN - 260 + col * 135
    by = 150 + row * 32
    bg, _ = CAT[name]
    d.rectangle([bx, by, bx + 22, by + 22], fill=bg)
    d.text((bx + 30, by + 11), name, font=font(20), fill=dark, anchor="lm")


def fit_font(lines, maxw, start=46, minsz=22):
    sz = start
    while sz > minsz:
        f = font(sz)
        if all(text_w(l, f) <= maxw for l in lines):
            return f
        sz -= 2
    return font(minsz)


# ---------- タイル ----------
for idx, (num, cat, lines) in enumerate(POSTS):
    r = idx // COLS
    c = idx % COLS
    x = MARGIN + c * (TILE + GAP)
    y = HEADER_H + r * (TILE + GAP)
    bg, fg = CAT[cat]
    d.rectangle([x, y, x + TILE, y + TILE], fill=hx(bg))
    # 内枠
    d.rectangle([x + 14, y + 14, x + TILE - 14, y + TILE - 14], outline=hx(fg), width=2)
    # 番号バッジ
    d.text((x + 30, y + 34), num, font=font(26), fill=fg, anchor="lm")
    # カテゴリラベル（上中央）
    d.text((x + TILE / 2, y + 60), cat, font=font(22), fill=fg, anchor="mm")
    # 区切り線
    d.line([x + TILE / 2 - 30, y + 86, x + TILE / 2 + 30, y + 86], fill=fg, width=1)
    # タイトル（中央）
    f = fit_font(lines, TILE - 70, start=52, minsz=26)
    asc = (f.getbbox("あ")[3] - f.getbbox("あ")[1])
    lh = asc + 16
    total = lh * len(lines)
    ty = y + TILE / 2 - total / 2 + asc / 2 + 6
    for l in lines:
        d.text((x + TILE / 2, ty), l, font=f, fill=fg, anchor="mm")
        ty += lh
    # ロゴ（下中央）
    d.text((x + TILE / 2, y + TILE - 36), "ZETITH HANE", font=font(16), fill=fg, anchor="mm")

# ---------- フッター ----------
d.text((W / 2, H - FOOTER_H / 2), "※表紙イメージ（仮）｜数値・症例・最終デザインは医師監修で確定",
       font=font(20), fill="#8A7866", anchor="mm")

out = "/home/user/pictweet1/instagram-content/grid_mockup_術式編.png"
img.save(out)
print("saved", out, img.size)
