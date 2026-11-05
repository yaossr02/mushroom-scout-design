# 問卷重畫 v2 · 六組新候選

2026-11-05。使用者已選定的15張已核准並推送main（4f43683）；本目錄只包含仍待選的6組、7個語意ID，共14張新candidate，沒有推送或新增核准。

| 題目 | A | B |
|---|---|---|
| Feed 餵果 | 果肉＋花蜜滴 | 花蜜餵食瓶 |
| ReturnToApp 回App | 合起的蘑菇圖鑑＋回頭箭頭 | 葉蓋圖鑑套＋回頭箭頭 |
| GameReturn 回遊戲 | 草地路徑＋前進箭頭 | 打開的葉門＋前進路徑 |
| HideFloat 隱藏 | 葉子收納袋 | 滑動遮藏蓋 |
| Collapse／Expand | 金色單尖括號 | 綠色雙尖括號 |
| Layers 圖層 | 三片地形層 | 三層剖面地塊 |

[全部新稿](concepts.png) · [完整組合／原尺寸HTML](index.html) · [32/48/64縮圖](thumbnails.png) · [無文字辨識](blind-test.png) · [答案](blind-answers.md) · [Auto／金盆／回App／回遊戲／隱藏比較](semantic-distinction.png) · [完整實測](catalog.json)

每次image_gen都附D金盆、v0.5紅菇與最接近用途的已核准batch1圖。原始輸出、完整prompt、日期、引用來源、1254×1254 RGBA實際規格、alpha、bbox及SHA-256保留於 `../../candidates/<ID>-<A|B>-v2/`。

Python只整理等比尺寸與透明畫布；Collapse／Expand沿用使用者已授權的精確完整RGBA上下翻轉，不重畫形狀。Expand保存的原始模型輸出是Collapse來源的逐位元複本，generation明確標示不是另一次模型輸出。

預覽已套用剛核准的15張及原金盆D，只有這7個ID切換v2候選。懸浮列40dp圓／24、28dp圖示；地圖40dp圓／32dp圖示，右側9顆，頂欄Layers／Settings，More另放。草地是既有image_gen模擬圖，未做Android實機測試。A/B選單只改預覽，不記錄核准。

使用者本次沒有提供退回原因；新方向是依功能辨識與上一輪差異提出，仍待選定。已核准PNG、manifest與Claude交接不得因生成本批候選而改動。
