# -*- coding: utf-8 -*-
"""ゼティス羽根 鼻整形シリーズ Instagram フィード サムネイル再設計
3テンプレ(術式表紙 / 症例解説 / 悩み別導入)を (row+col)%3 で配置しモザイク化。
色: 黒・白・ベージュ・深緑・ダスティローズ・グレージュ。"""
from PIL import Image, ImageDraw, ImageFont

JP = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
SF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

COLS, TILE, GAP, MARGIN = 3, 480, 6, 30
HEADER_H, FOOTER_H = 280, 78

# ---- パレット ----
P = dict(
    black="#171513", ink="#211E1A", white="#FFFFFF", cream="#F6EFE3",
    beige="#E7DAC6", beige_d="#CDB68F", greige="#B3A99B", greige_d="#8C8377",
    green="#2E3D34", green_d="#202B25", rose="#C2938E", rose_d="#A1726D",
)

# カテゴリ アクセント色
ACC = {
    "導入": P["green"], "鼻先": P["rose"], "鼻筋": P["beige_d"],
    "小鼻系": P["green"], "周辺": P["greige_d"], "まとめ": P["ink"],
}
# テンプレA背景(カテゴリで明暗を散らす)
A_BG = {
    "導入": P["ink"], "鼻先": P["cream"], "鼻筋": P["beige"],
    "小鼻系": P["green"], "周辺": P["greige_d"], "まとめ": P["black"],
}

# (番号, カテゴリ, タイトル行, ラテン, 悩みフレーズ, 解決ラベル)
POSTS = [
    ("01", "導入", ["クローズド法"], "CLOSED RHINOPLASTY", ["傷あとを", "残したくない"], "クローズド法"),
    ("02", "導入", ["オープン法"], "OPEN RHINOPLASTY", ["しっかり", "形を変えたい"], "オープン法"),
    ("03", "鼻先", ["鼻尖形成"], "NASAL TIP PLASTY", ["丸い鼻先を", "すっきり"], "鼻尖形成"),
    ("04", "鼻先", ["軟骨移植"], "CARTILAGE GRAFT", ["鼻先に", "高さがほしい"], "軟骨移植"),
    ("05", "鼻先", ["ストラット"], "COLUMELLAR STRUT", ["鼻先を", "長持ちさせたい"], "ストラット"),
    ("06", "鼻先", ["鼻中隔延長", "（耳軟骨）"], "SEPTAL EXTENSION", ["上向きの鼻を", "下げたい"], "鼻中隔延長"),
    ("07", "鼻先", ["鼻中隔延長", "（肋軟骨）"], "SEPTAL EXTENSION", ["短い鼻を", "大きく変えたい"], "鼻中隔延長"),
    ("08", "鼻筋", ["プロテーゼ"], "SILICONE IMPLANT", ["鼻筋を", "高くしたい"], "プロテーゼ"),
    ("09", "鼻筋", ["自家組織", "隆鼻"], "AUTOLOGOUS GRAFT", ["異物を", "入れたくない"], "自家組織隆鼻"),
    ("10", "鼻筋", ["骨切り", "幅寄せ"], "OSTEOTOMY", ["鼻筋を", "細くしたい"], "骨切り幅寄せ"),
    ("11", "鼻筋", ["鷲鼻削り", "ハンプ切除"], "HUMP REMOVAL", ["横顔の", "出っぱりが気になる"], "ハンプ切除"),
    ("12", "小鼻系", ["鼻翼縮小"], "ALAR REDUCTION", ["小鼻を", "小さくしたい"], "鼻翼縮小"),
    ("13", "小鼻系", ["鼻孔縁挙上"], "ALAR RIM LIFT", ["鼻の穴が", "目立つ"], "鼻孔縁挙上"),
    ("14", "小鼻系", ["鼻孔縁下降"], "ALAR RIM LOWERING", ["鼻の穴が", "見えすぎる"], "鼻孔縁下降"),
    ("15", "小鼻系", ["鼻翼挙上"], "ALAR LIFT", ["笑うと小鼻が", "目立つ"], "鼻翼挙上"),
    ("16", "小鼻系", ["鼻柱下降"], "COLUMELLAR SHOW", ["鼻の下の", "バランス"], "鼻柱下降"),
    ("17", "周辺", ["貴族手術", "ゴアテックス"], "PARANASAL AUG.", ["口元の凹みが", "気になる"], "貴族手術"),
    ("18", "周辺", ["貴族手術", "（肋軟骨）"], "PARANASAL AUG.", ["自家組織で", "しっかり"], "貴族手術"),
    ("19", "周辺", ["猫手術"], "NOSTRIL REFINE", ["笑った時の", "鼻まわり"], "猫手術"),
    ("20", "まとめ", ["軟骨の", "使い分けMAP"], "CARTILAGE GUIDE", ["どの軟骨を", "使うの？"], "完全ガイド"),
    ("21", "まとめ", ["鼻整形", "用語辞典"], "GLOSSARY", ["専門用語を", "まるわかり"], "用語辞典"),
]

TYPE_NAME = {0: "術式表紙", 1: "症例解説", 2: "悩み別導入"}


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lum(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def jp(sz):
    return ImageFont.truetype(JP, sz)


def sf(sz, bold=False, ital=False):
    return ImageFont.truetype(SFB if bold else (SFI if ital else SF), sz)


PROFILE = [
    (0.42, 0.05), (0.55, 0.07), (0.63, 0.14), (0.665, 0.23),
    (0.63, 0.29), (0.665, 0.33), (0.82, 0.46),
    (0.665, 0.50), (0.71, 0.53), (0.675, 0.56), (0.71, 0.595),
    (0.66, 0.65), (0.60, 0.73), (0.585, 0.83), (0.57, 0.97),
    (0.30, 0.97), (0.27, 0.66), (0.24, 0.42), (0.27, 0.24), (0.33, 0.115),
]


def profile_poly(x, y, w, h, facing="right"):
    pts = []
    for px, py in PROFILE:
        if facing == "left":
            px = 1 - px
        pts.append((x + px * w, y + py * h))
    return pts


def vgrad(dr, box, ctop, cbot):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        dr.line([(x0, y0 + i), (x1, y0 + i)], fill=lerp(ctop, cbot, i / h))


def tracked(dr, x, y, text, font, fill, tr=3, center_w=None):
    widths = [dr.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tr * (len(text) - 1)
    if center_w is not None:
        x = x + (center_w - total) / 2
    cx = x
    for ch, w in zip(text, widths):
        dr.text((cx, y), ch, font=font, fill=fill)
        cx += w + tr
    return total


def fit_jp(dr, lines, maxw, start, minsz, stroke=0):
    sz = start
    while sz > minsz:
        f = jp(sz)
        if all(dr.textlength(l, font=f) + 2 * stroke <= maxw for l in lines):
            return f
        sz -= 2
    return jp(minsz)


def wrap_jp(dr, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if dr.textlength(cur + ch, font=font) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


# =========================================================
# テンプレA : 術式表紙 (エディトリアル)
# =========================================================
def tpl_cover(tile, post):
    num, cat, title, en, _, _ = post
    bg = hx(A_BG[cat])
    acc = hx(ACC[cat])
    fg = hx(P["cream"]) if lum(bg) < 130 else hx(P["ink"])
    sub = lerp(fg, bg, 0.45)
    d = ImageDraw.Draw(tile)
    # 背景＋微グラデで奥行き
    vgrad(d, (0, 0, TILE, TILE), lerp(bg, hx(P["white"]), 0.06 if lum(bg) > 130 else 0.0),
          lerp(bg, hx(P["black"]), 0.18 if lum(bg) < 130 else 0.0) if lum(bg) < 130 else lerp(bg, hx(P["greige_d"]), 0.10))
    # 透かしの横顔
    d.polygon(profile_poly(TILE * 0.34, TILE * 0.04, TILE * 0.72, TILE * 0.92, "right"),
              fill=lerp(bg, acc, 0.16))
    # 左の縦アクセントバー
    d.rectangle([34, 150, 42, TILE - 150], fill=acc)
    # 上: ラテン overline + 番号
    tracked(d, 60, 54, en, sf(22, ital=False), sub, tr=4)
    d.text((TILE - 60, 50), num, font=sf(30, bold=True), fill=acc, anchor="ra")
    d.line([60, 92, TILE - 60, 92], fill=lerp(fg, bg, 0.7), width=1)
    # 大タイトル(左下寄り)
    f = fit_jp(d, title, TILE - 130, 92, 46, stroke=1)
    asc = f.getbbox("あ")[3] - f.getbbox("あ")[1]
    lh = asc + 22
    ty = TILE - 150 - lh * len(title)
    for l in title:
        d.text((60, ty), l, font=f, fill=fg, stroke_width=1, stroke_fill=fg)
        ty += lh
    # フッター
    d.line([60, TILE - 92, 200, TILE - 92], fill=acc, width=2)
    tracked(d, 60, TILE - 72, "ZETITH HANE", sf(19), sub, tr=3)
    d.text((TILE - 60, TILE - 70), "鼻整形・術式", font=jp(18), fill=sub, anchor="ra")


# =========================================================
# テンプレB : 症例解説 (フォトフォワード)
# =========================================================
def tpl_case(tile, post):
    num, cat, title, en, _, _ = post
    acc = hx(ACC[cat])
    d = ImageDraw.Draw(tile)
    photo_h = int(TILE * 0.66)
    # 写真エリア(duotone)
    base = lerp(acc, hx(P["black"]), 0.35)
    vgrad(d, (0, 0, TILE, photo_h), lerp(base, hx(P["white"]), 0.10), lerp(base, hx(P["black"]), 0.25))
    # 横顔シルエット(明色)
    sil = lerp(acc, hx(P["cream"]), 0.78)
    px0, pw = TILE * 0.16, TILE * 0.74
    d.polygon(profile_poly(px0, photo_h * 0.10, pw, photo_h * 1.02, "right"), fill=sil)
    # 鼻先ハイライト円
    nx, ny = px0 + 0.82 * pw, photo_h * 0.10 + 0.46 * photo_h * 1.02
    d.ellipse([nx - 46, ny - 46, nx + 46, ny + 46], outline=hx(P["white"]), width=3)
    # CASE チップ
    d.rectangle([26, 26, 150, 64], fill=acc)
    tracked(d, 40, 33, "CASE " + num, sf(20, bold=True), hx(P["white"]), tr=2)
    # 写真プレースホルダ注記
    d.text((TILE - 26, 34), "症例写真", font=jp(18), fill=lerp(base, hx(P["white"]), 0.6), anchor="ra")
    d.text((TILE - 26, 58), "PHOTO", font=sf(15), fill=lerp(base, hx(P["white"]), 0.5), anchor="ra")
    # 下部 解説ストリップ
    d.rectangle([0, photo_h, TILE, TILE], fill=hx(P["cream"]))
    d.rectangle([0, photo_h, 10, TILE], fill=acc)
    f = fit_jp(d, title, TILE - 80, 56, 34, stroke=1)
    asc = f.getbbox("あ")[3] - f.getbbox("あ")[1]
    lh = asc + 14
    ty = photo_h + 34
    for l in title:
        d.text((40, ty), l, font=f, fill=hx(P["ink"]), stroke_width=1, stroke_fill=hx(P["ink"]))
        ty += lh
    # 医療的注釈
    d.line([40, TILE - 64, TILE - 40, TILE - 64], fill=hx(P["beige_d"]), width=1)
    d.text((40, TILE - 54), "症例｜30代・女性", font=jp(17), fill=hx(P["greige_d"]))
    d.text((40, TILE - 30), "＊効果・経過には個人差があります", font=jp(15), fill=hx(P["greige_d"]))


# =========================================================
# テンプレC : 悩み別導入 (タイポ主役)
# =========================================================
def tpl_concern(tile, post):
    num, cat, _, en, concern, sol = post
    acc = hx(ACC[cat])
    bg = hx(P["cream"]) if cat not in ("導入", "まとめ") else hx(P["white"])
    d = ImageDraw.Draw(tile)
    d.rectangle([0, 0, TILE, TILE], fill=bg)
    # 右下に横顔アクセント(薄)
    d.polygon(profile_poly(TILE * 0.52, TILE * 0.40, TILE * 0.60, TILE * 0.70, "right"),
              fill=lerp(bg, acc, 0.18))
    # セリフ "Q." 大
    d.text((46, 36), "Q.", font=sf(78, bold=True, ital=True), fill=acc)
    # 「お悩み」チップ
    d.rectangle([TILE - 150, 56, TILE - 40, 92], outline=acc, width=2)
    d.text((TILE - 95, 74), "お悩み", font=jp(20), fill=acc, anchor="mm")
    # 大きな悩みフレーズ
    text = "".join(concern)
    f = jp(58)
    lines = wrap_jp(d, text, f, TILE - 90)
    while len(lines) > 3 and f.size > 36:
        f = jp(f.size - 3)
        lines = wrap_jp(d, text, f, TILE - 90)
    asc = f.getbbox("あ")[3] - f.getbbox("あ")[1]
    lh = asc + 18
    ty = 168
    for i, l in enumerate(lines):
        d.text((46, ty), l, font=f, fill=hx(P["ink"]), stroke_width=1, stroke_fill=hx(P["ink"]))
        ty += lh
    # 太アンダーライン アクセント
    uw = min(TILE - 90, d.textlength(lines[-1], font=f))
    d.rectangle([46, ty - lh + asc + 6, 46 + uw * 0.62, ty - lh + asc + 16], fill=acc)
    # 解決導線
    d.line([46, TILE - 96, TILE - 46, TILE - 96], fill=lerp(bg, acc, 0.5), width=1)
    d.text((46, TILE - 82), "→ " + sol + " で解決", font=jp(22), fill=acc)
    tracked(d, 46, TILE - 46, "ZETITH HANE", sf(17), hx(P["greige_d"]), tr=3)
    d.text((TILE - 46, TILE - 48), num, font=sf(24, bold=True), fill=acc, anchor="ra")


RENDER = {0: tpl_cover, 1: tpl_case, 2: tpl_concern}

rows = (len(POSTS) + COLS - 1) // COLS
W = MARGIN * 2 + COLS * TILE + (COLS - 1) * GAP
H = HEADER_H + rows * TILE + (rows - 1) * GAP + FOOTER_H
img = Image.new("RGB", (W, H), hx(P["cream"]))
D = ImageDraw.Draw(img)

# ===== ヘッダー =====
ink = hx(P["ink"]); gold = hx(P["beige_d"])
D.rectangle([0, 0, W, HEADER_H], fill=hx(P["white"]))
D.rectangle([0, HEADER_H - 2, W, HEADER_H], fill=gold)
tracked(D, MARGIN + 4, 40, "ZETITH HANE", sf(50, bold=True), ink, tr=6)
D.text((MARGIN + 6, 108), "鼻整形シリーズ｜フィード設計（表紙イメージ）", font=jp(26), fill=hx(P["greige_d"]))
# カードタイプ凡例
lx = MARGIN + 6
for t in [0, 1, 2]:
    D.text((lx, 156), "● " + TYPE_NAME[t], font=jp(22), fill=ink)
    lx += D.textlength("● " + TYPE_NAME[t], font=jp(22)) + 36
D.text((MARGIN + 6, 196), "3スタイルを (行+列) で配置し斜めにモザイク化／色＝部位カテゴリ", font=jp(20), fill=hx(P["greige_d"]))
# 右側 カテゴリ凡例
items = list(ACC.keys())
for i, name in enumerate(items):
    col = i % 3; row = i // 3
    bx = W - MARGIN - 470 + col * 160; by = 150 + row * 40
    D.rectangle([bx, by, bx + 26, by + 26], fill=hx(ACC[name]))
    D.text((bx + 34, by + 13), name, font=jp(20), fill=ink, anchor="lm")

# ===== タイル配置 =====
for idx, post in enumerate(POSTS):
    r, c = divmod(idx, COLS)
    t = (r + c) % 3
    tile = Image.new("RGB", (TILE, TILE), hx(P["cream"]))
    RENDER[t](tile, post)
    # 細い額縁
    ImageDraw.Draw(tile).rectangle([0, 0, TILE - 1, TILE - 1], outline=hx(P["beige_d"]), width=1)
    x = MARGIN + c * (TILE + GAP); y = HEADER_H + r * (TILE + GAP)
    img.paste(tile, (x, y))

# ===== フッター =====
D.rectangle([0, H - FOOTER_H, W, H], fill=hx(P["white"]))
D.text((W / 2, H - FOOTER_H / 2),
       "※表紙イメージ（仮）｜症例写真はプレースホルダ・実写差込予定／数値・症例・最終表現は医療広告ガイドライン遵守のうえ医師監修で確定",
       font=jp(19), fill=hx(P["greige_d"]), anchor="mm")

out = "/home/user/pictweet1/instagram-content/feed_design_v2.png"
img.save(out)
print("saved", out, img.size)
