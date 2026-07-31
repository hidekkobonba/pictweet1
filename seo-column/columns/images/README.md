# 画像フォルダ（images/）— 現状インデックス

このフォルダは **コラム全10ページ（一覧＋記事9本）が共通で参照**します。
各HTMLは相対パス `src="images/xxx.jpg"` で読み込み、入っている画像は自動表示されます。

> 運用・命名・最適化・症例併記のルールは **`seo-column/コラム制作ガイド.md`（§5・§6・§12）が正**です。
> このREADMEは「今フォルダに入っている画像の一覧」に絞ります。

## 命名規則（ガイド§5）
- アイキャッチ：`hero.jpg`（16:9）／SNSシェア：`ogp.jpg`（1200×630）
- 医師：`hane.jpg`
- 図解：`illust-<topic>.jpg`（横長。図中に説明文あり＝`<figcaption>`は付けない）
- 症例：`case-<topic>-front|oblique|side.jpg`（縦長 4:5＝1080×1350、無加工。タブ＝正面／斜め／横）

## 現在入っている画像

### 共通
| ファイル | 用途 |
|---|---|
| `hero.jpg` | 記事トップのアイキャッチ |
| `ogp.jpg` | OGP（SNSシェア用・1200×630） |
| `hane.jpg` | 監修医師 羽根和秀 院長の顔写真 |

### 症例（case-*）
| ファイル | 記事 |
|---|---|
| `case-dango-front / -oblique / -side` | 団子鼻（`dango-hana-fukuoka.html`） |
| `case-tiplift-front / -oblique / -side` | 鼻中隔延長（`bichukaku-encho-fukuoka.html`） |
| `case-kizoku-front / -oblique / -side` | 貴族手術（`kizoku-shujutsu-fukuoka.html`） |
| `case-neko-front / -side / -side2` | 猫手術（`neko-shujutsu-fukuoka.html`。3タブ=正面/斜め/横） |
| `case-ryubi-front / -oblique / -side` | 隆鼻・自家組織（`ryubi-fukuoka.html`） |
| `case-ryubi-pro-front / -oblique / -side` | 隆鼻・プロテーゼ（`ryubi-fukuoka.html`） |

### 図解（illust-*）
| ファイル | 用途 |
|---|---|
| `illust-closed-incision` | クローズド法の切開位置 |
| `illust-closed-vs-open` | クローズド法 vs オープン法の切開比較 |
| `illust-graft-cartilage` | 軟骨（肋・耳介・鼻中隔）の採取部位 |
| `illust-kizoku` | 貴族手術の図解 |
| `illust-neko` | 猫手術の総合図解（1400×788） |
| `illust-ryubi-tip` | 隆鼻の図解 |
| `illust-kobana` | 小鼻の整え方の総合図解（1400×933）＝鼻翼縮小（内側法・外側法）と鼻孔縁挙上の切除場所。`kobana-shukusho-fukuoka.html` のSection 02に設置。図解はこの1枚のみ |

---

## 公開先・管理人さんへの依頼
- **公開先（確定）：`/ja-jp/clinics/fukuoka/columns/`**（福岡院配下）。canonical・og:url・JSON-LDは絶対パスで統一済み。
- HTML・`assets/`・`images/` は**同じ位置関係のまま**まるごと設置（バラすと崩れる）。
- 症例写真は医療広告ガイドライン上、**施術内容・料金・主なリスク／副作用の併記が必須**（各HTMLに記載欄あり。数値のみ最新に）。
- 詳しい設置手順は同梱の **`管理人向け_設置手順.txt`** を参照。
