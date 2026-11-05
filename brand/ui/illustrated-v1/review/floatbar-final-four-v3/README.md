# 懸浮列最後四項 · v3候選

2026-11-05。使用者明確要求：Feed要餵食動作；ReturnToApp不要書、要蘑菇程式；GameReturn要遊戲圖示；HideFloat要眼睛看不到。依此各出A/B，共8張新candidate。

地圖補齊三張已核准並自動推送main（14a1523），地圖其他七項現在全部核准。此前11張懸浮列及D金盆保持原檔；本次只重畫最後四項，不改App。

| 項目 | A | B |
|---|---|---|
| Feed | 木匙將果肉送入葉碟 | 餵食杓將果肉倒入食碗 |
| ReturnToApp | 蘑菇程式方塊＋回頭箭頭 | 綠底蘑菇App方塊＋向內箭頭 |
| GameReturn | 遊戲手把＋前進箭頭 | 遊戲App方塊＋前進箭頭 |
| HideFloat | 睜眼＋斜線 | 閉眼＋斜線 |

[候選比較](concepts.png) · [完整懸浮列／32dp地圖／深淺底HTML](index.html) · [縮圖](thumbnails.png) · [無文字圖](blind-test.png) · [答案](blind-answers.md) · [語意區分](semantic-distinction.png) · [實測與SHA-256](catalog.json)

每次image_gen仍附D金盆、v0.5紅菇與最接近用途的已核准batch1原圖。完整prompt、三個引用路徑、日期、原始模型輸出、1254×1254 RGBA規格、alpha、bbox與SHA-256保留於 `../../candidates/<ID>-<A|B>-v3/`。

只以Python做等比尺寸、畫布平移與透明留白，不描邊、加粗、補畫或改形狀。新稿未核准／未推送；已核准PNG與歷史manifest不覆蓋。懸浮列40dp圓、24／28dp插圖；地圖使用完整已核准7項及原5項，40dp圓／32dp插圖。草地為既有image_gen模擬背景，沒有Android實機測試。

功能性的眼睛是使用者本輪明確要求，僅作UI隱藏符號，不在蘑菇、金盆或角色上加五官。蘑菇App與遊戲App方塊也是本輪明確指定的題材修訂，不再用書本／葉門代替。
