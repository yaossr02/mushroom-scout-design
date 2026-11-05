> 問卷結果：15張已核准並推送；Feed、ReturnToApp、GameReturn、HideFloat、Collapse/Expand、Layers需重畫。此頁以下保留第一輪歷史，[新稿見v2](../batch2-batch3-rework-v2/index.html)。

# illustrated-v1 · 懸浮列與地圖其他圓鈕候選

2026-11-05（Asia/Taipei）。共42張image_gen來源、2張精確翻轉的Expand，共44張新candidate。懸浮列15組A/B新圖，另將既有核准D金盆原圖直接放入兩組檢閱，不重畫、不繼承核准。

每次生成都附三張實際原圖：D金盆、v0.5紅菇、最接近用途的已核准batch1 PNG。來源路徑與完整prompt逐張存於 `../../candidates/<ID>-<A|B>-v1/PROMPT.json`；同目錄保存原始模型輸出、generation記錄、icon.png、尺寸、alpha、bbox與SHA-256。

## 檢閱入口

- [完整HTML](index.html)：無文字辨識／獨立答案、逐項A/B切換、24／28dp懸浮列、32dp地圖圓鈕、32／48／64px與深底／棋盤底。
- 懸浮列：[A/B概念總覽](floatbar-concepts.png)、[A組](floatbar-A.png)、[B組](floatbar-B.png)。
- 地圖：[A/B概念總覽](map-concepts.png)、[整體排版](map-comparison.png)。
- [全部縮圖](thumbnails.png)、[無文字圖](blind-test.png)、[獨立答案](blind-answers.md)。
- [Auto／GoldBasin／ReturnToApp區分](semantic-distinction.png)。Auto使用目前核准C循環果實，未回退首批A金盆。
- [全部候選實測](catalog.json)、[懸浮列清單](catalog.floatbar.json)、[地圖清單](catalog.map.json)。均為candidate catalog，沒有approved manifest。

## 尺寸與來源

圖檔1254×1254透明RGBA。Python只做等比尺寸、畫布平移和透明留白整理，不描邊、加粗、補畫或改形狀。使用者本次額外明確允許一次機械垂直翻轉：Expand A/B為最終Collapse A/B完整RGBA的精確上下翻轉，包含明暗與alpha。Expand保存的原始模型輸出是Collapse來源的逐位元複本，generation.json明列不是第二次模型生成。

懸浮列：每組16顆40dp暖白 #FFFCF6 圓，圖示24／28dp，間距8dp；完整單列784dp，可在HTML橫向捲動。xxxhdpi原尺寸PNG每圓160px、圖示96／112px。

地圖：390×620dp模擬viewport，右側9顆含Collapse、Expand、Auto、Tasks、Records、Favorites、Scan、Locate、Teleport；Layers／Settings在頂欄，More另放左下。全部40dp圓／32dp插圖（xxxhdpi160／128px）。Auto及其餘四個首批功能沿用目前已核准來源。

奶油地圖底 #EFEBE3；高飽和草地沿用 `references/simulated-grass.png`，為image_gen模擬背景，非遊戲實機截圖。檢閱板縮放僅供比較，HTML的CSS尺寸不等於Android實機測試。未進行真人無文字辨識實驗。

## 核准範圍

本次只出candidate，不建立 `approved/batch2-floatbar/` 或 `approved/batch3-map/`，不寫新核准紀錄或改CLAUDE-HANDOFF.md，不覆蓋舊核准檔、不改App。使用者逐項選A/B或要求修改後，才依既有持續授權完成核准交接並自動推送。
