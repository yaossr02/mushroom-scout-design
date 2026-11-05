> 最新核准 · 2026-11-05：Auto A、Tasks A、Records A、Favorites B、Scan A；GoldBasin沿用D。其餘五張仍candidate。以下首稿與方向確認說明保留審閱歷史，正式來源見 [核准manifest](approved/batch1/manifest.json)，程式交接見 [CLAUDE-HANDOFF.md](CLAUDE-HANDOFF.md)。

# 插圖風功能圖示 · 第一批候選

2026-11-05（Asia/Taipei）。系列規範先建立於 [ILLUSTRATED-STYLE.md](ILLUSTRATED-STYLE.md)。以核准 D 金盆與 v0.5 紅菇兩張實際附圖，生成 Auto／Tasks／Records／Favorites／Scan，各 A、B 共10張；全部為 **candidate**，沒有新核准紀錄、沒有改 App 或覆蓋核准素材。

| 功能 | A | B |
|---|---|---|
| Auto 自動 | 循環箭頭金盆 | 發條花苗 |
| Tasks 任務 | 綠緞帶紙卷 | 葉籤木牌 |
| Records 紀錄 | 紅菇圖鑑 | 蘑菇收藏盒 |
| Favorites 常用地點 | 插旗紅菇 | 金色星花 |
| Scan 掃描 | 放大鏡紅菇 | 草叢掃描弧 |

## 檢閱

- [完整互動頁](review/index.html)：先做無文字辨識，再展開答案；可個別切換5項的A／B，預覽地圖右側直排。切換不代表核准，不會儲存任何核准狀態。
- [全部候選總覽](review/overview.png)：10張新圖與兩張核准參考同畫布大小。
- 每功能一張：[Auto](review/Auto.png)／[Tasks](review/Tasks.png)／[Records](review/Records.png)／[Favorites](review/Favorites.png)／[Scan](review/Scan.png)。
- [無文字辨識圖](review/blind-test.png) 與 [獨立答案](review/blind-answers.md)。沒有做真人盲測，辨識是否成立由使用者審閱。
- 32／48／64px縮圖、80／96px樣本、深底與棋盤底均直接引用候選原PNG。
- `review/right-column-{A|B}-{map|grass}-{20|24}dp-xxxhdpi.png`：360×320dp模擬畫面，以@4x輸出1440×1280px；5顆圓在右側，40dp圓=160px、圖示20／24dp=80／96px、間距12dp。PNG檢閱板會縮放，請以HTML的40／20／24 CSS px為實際佈局檢閱。
- 暖白圓 #FFFCF6、奶油地圖 #EFEBE3。草地沿用既有image_gen模擬背景，並非遊戲截圖；沒有做Android實機測試。

## 來源與規格

每張在 `candidates/<ID>-<A|B>-v1/` 保留 `generated-original.png`、`generation.json`、`PROMPT.json`、`icon.png`、`METADATA.json`。完整實際prompt與兩張附圖路徑逐張記錄；日期、實際尺寸、alpha範圍、非零／alpha128 bbox、SHA-256彙整於 [catalog.json](catalog.json)。此為本系列候選清單，不取代全域正式來源。

只以 `prepare_review.py` 做必要的等比尺寸、完整畫布平移與透明留白整理，讓alpha128主體約留8%安全邊；不做限色、補畫、描邊、加粗或形狀修正。原始生成PNG完全保留。模型低alpha邊緣可能仍需正式輸出前檢查，bbox不可視為形狀核准。

`references/` 是兩張核准原圖的逐位元複本，以及標示為模擬的草地背景。生成前保存 `protected-source-hashes.json`，交付前檢查所有既有核准素材與核准紀錄未變。

使用者逐項選A／B或要求修改後，才建立 `brand/approvals/<日期>-illustrated-v1-batch1.md`。新系列、新圖或整套並排不會自動繼承金盆的核准；本次不準備正式App匯入包。

## 方向已確認 · 2026-11-05

使用者回覆「對! 這些都是我要的」，確認本系列插圖風格。後續沿此方向；本批各功能A／B尚待選定，10張仍為candidate，不建立個別核准或App匯入紀錄。
