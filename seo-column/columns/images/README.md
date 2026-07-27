# 画像リスト（このフォルダに入れる画像）

`fukuoka-hana-seikei.html` は、**同じ階層にある この `images/` フォルダ**の画像を参照します。
下記のファイル名で画像を入れてください。**入れた画像は自動で表示**されます（入っていない箇所は「配置場所を示すプレースホルダ」が表示されます）。

## 必須（症例・アイキャッチ）

| ファイル名 | 用途 | 推奨サイズ・比率 | 備考 |
|---|---|---|---|
| `hero.jpg` | 記事トップのアイキャッチ | 1200×675px（16:9） | JPG/WebP。人物や施術イメージ |
| `case-dango-front.jpg` | お悩み①団子鼻 症例・**正面**（術前｜術後） | 縦長 4:5（例 1080×1350） | Before/After合成でOK |
| `case-dango-oblique.jpg` | お悩み①団子鼻 症例・**斜め**（術前｜術後） | 縦長 4:5 | 同上 |
| `case-dango-side.jpg` | お悩み①団子鼻 症例・**横**（術前｜術後） | 縦長 4:5 | 同上 |
| `case-ryubi-front.jpg` | お悩み②鼻筋の低さ 症例・**正面** | 縦長 4:5 | 用意でき次第 |
| `case-ryubi-oblique.jpg` | お悩み②鼻筋の低さ 症例・**斜め** | 縦長 4:5 | 用意でき次第 |
| `case-ryubi-side.jpg` | お悩み②鼻筋の低さ 症例・**横** | 縦長 4:5 | 用意でき次第 |
| `case-tiplift-front.jpg` | お悩み③鼻先を高く 症例・**正面** | 縦長 4:5 | 用意でき次第 |
| `case-tiplift-oblique.jpg` | お悩み③鼻先を高く 症例・**斜め** | 縦長 4:5 | 用意でき次第 |
| `case-tiplift-side.jpg` | お悩み③鼻先を高く 症例・**横** | 縦長 4:5 | 用意でき次第 |

## 任意（図解イラスト。無ければ省略可＝該当のfigureごと削除でもOK）

| ファイル名 | 用途 | 推奨サイズ |
|---|---|---|
| `illust-closed-incision.png` | クローズド法の切開位置の図解 | 横長 1200×675px |
| `illust-closed-vs-open.png` | クローズド法 vs オープン法の切開位置比較 | 横長 1200×675px |
| `illust-graft-cartilage.png` | 軟骨（肋軟骨・耳介・鼻中隔）の採取部位 | 横長 1200×675px |

## SNSシェア用（任意）

| ファイル名 | 用途 | 推奨サイズ |
|---|---|---|
| `ogp.jpg` | SNSでシェアされた時のサムネイル（OGP） | 1200×630px |

---

## 管理人さんへの依頼（そのまま渡せます）

1. `fukuoka-hana-seikei.html` と、この `images/` フォルダを **同じ位置関係のまま** サーバーにアップしてください。
2. 症例写真（ビフォーアフター）は医療広告ガイドライン上、**施術内容・料金・主なリスク／副作用の明記が必須**です。HTML内にすでに記載欄があります。数値だけ最新に更新してください。
3. HTML冒頭コメントの `[ ]`（電話番号・住所・予約URL・LINE URL）と、`canonical`／OGP のURL（`https://zetithbeautyclinic.com/columns/...`）を、実際の公開URLに差し替えてください。

## WordPressで運用している場合

画像はメディアライブラリにアップし、HTML内の `src="images/xxx.jpg"` を、アップ後のURL
（`https://zetithbeautyclinic.com/wp-content/uploads/...`）に置き換えてください。
