# illustrated-v1 · Claude正式交接

2026-11-05：懸浮列16項、地圖12項，共28個語意ID皆已逐項核准。只交付設計資產，沒有修改App。

**先讀 [全系列正式索引](approved/active-sets.json)**。它列出現行三個素材清單與全部28個ID、固定路徑、SHA-256、用途及尺寸。不要用歷史partial manifest或候選目錄。

- [完整懸浮列16項](approved/batch2-floatbar/completion-v4/manifest.json) · [24／28dp檢閱](approved/batch2-floatbar/completion-v4/index.html)。
- [地圖主要5項](approved/current-manifest.json)：Auto C、Tasks A、Records A、Favorites B、Scan A。
- [地圖其他7項](approved/batch3-map/current-manifest.json) · [32dp完整檢閱](approved/batch3-map/current-preview.html)。
- [全部核准組合圖](approved/complete-set-v1.png)。

## 匯入規格

原圖均1254×1254透明RGBA。保持完整畫布等比縮放，不依bbox裁滿、不套單色tint、不重描、不改為貼紙。40dp暖白 #FFFCF6 圓底：地圖圖示32dp（xxxhdpi128px），懸浮列圖示24／28dp（96／112px）。互動狀態用容器處理，圖像不變；Android實際觸控區依App規則。

完整懸浮列請整套採此插圖系列，不混入舊C-v2。ready_for_full_replacement只代表核准設計資產完整，不代表App已匯入、部署或實機驗證已通過。尚需App端測試透明邊、不同背景、觸控與小尺寸辨識。

## 關鍵語意

- Auto：完整紅蘋果＋金色循環箭頭。Feed：**咬一口的紅蘋果＋金色循環箭頭**，要保留大咬痕；兩者不是同圖。
- GoldBasin：原D金盆＋珊瑚紅向下箭頭，直接沿用核准PNG。
- ReturnToApp：金框綠底蘑菇程式＋黃色彎曲向左返回箭頭。GameReturn：同款底板／返回箭頭，中央為遊戲手把；不要擅自改回向右直箭頭。
- HideFloat：A v3功能眼睛＋斜線；不是擬人化五官。
- Collapse／Expand：B v2綠色雙尖括號，完整RGBA精確上下翻轉，不另行變形。
- 標準操作採無葉A；Play向右、Pause兩柱、Stop實心無洞、SkipBack左側立線＋雙向左三角、SkipForward雙向右三角＋右側立線、Check綠勾、Close紅叉。

## 來源與核准

每張原始模型輸出、完整實際prompt、引用附圖、日期及metadata保存於各核准批次的provenance；candidate字樣是生成歷史，現行核准以active-sets與對應approval_record為準。未選候選沒有隨正式包推送。新功能延伸須另行核准；使用者已授權核准後自動推送設計repo。

| ID | 核准來源（repo root相對路徑） | 用途 |
|---|---|---|
| GoldBasin | brand/ui/approved/gold-planter-illustrated-v1/icon.png | floatbar |
| Feed | brand/ui/illustrated-v1/approved/batch2-floatbar/completion-v4/Feed.png | floatbar |
| Dispatch | brand/ui/illustrated-v1/approved/batch2-floatbar/Dispatch.png | floatbar |
| LightSpeed | brand/ui/illustrated-v1/approved/batch2-floatbar/LightSpeed.png | floatbar |
| Ticket | brand/ui/illustrated-v1/approved/batch2-floatbar/Ticket.png | floatbar |
| FloatMenu | brand/ui/illustrated-v1/approved/batch2-floatbar/FloatMenu.png | floatbar |
| ReturnToApp | brand/ui/illustrated-v1/approved/batch2-floatbar/completion-v4/ReturnToApp.png | floatbar |
| GameReturn | brand/ui/illustrated-v1/approved/batch2-floatbar/completion-v4/GameReturn.png | floatbar |
| HideFloat | brand/ui/illustrated-v1/approved/batch2-floatbar/hide-v3/HideFloat.png | floatbar |
| Play | brand/ui/illustrated-v1/approved/batch2-floatbar/Play.png | floatbar |
| Pause | brand/ui/illustrated-v1/approved/batch2-floatbar/Pause.png | floatbar |
| Stop | brand/ui/illustrated-v1/approved/batch2-floatbar/Stop.png | floatbar |
| SkipBack | brand/ui/illustrated-v1/approved/batch2-floatbar/SkipBack.png | floatbar |
| SkipForward | brand/ui/illustrated-v1/approved/batch2-floatbar/SkipForward.png | floatbar |
| Check | brand/ui/illustrated-v1/approved/batch2-floatbar/Check.png | floatbar |
| Close | brand/ui/illustrated-v1/approved/batch2-floatbar/Close.png | floatbar |
| Auto | brand/ui/illustrated-v1/approved/auto-C-v2/icon.png | map |
| Tasks | brand/ui/illustrated-v1/approved/batch1/Tasks.png | map |
| Records | brand/ui/illustrated-v1/approved/batch1/Records.png | map |
| Favorites | brand/ui/illustrated-v1/approved/batch1/Favorites.png | map |
| Scan | brand/ui/illustrated-v1/approved/batch1/Scan.png | map |
| Collapse | brand/ui/illustrated-v1/approved/batch3-map/completion-v2/Collapse.png | map |
| Expand | brand/ui/illustrated-v1/approved/batch3-map/completion-v2/Expand.png | map |
| Locate | brand/ui/illustrated-v1/approved/batch3-map/Locate.png | map |
| Teleport | brand/ui/illustrated-v1/approved/batch3-map/Teleport.png | map |
| Layers | brand/ui/illustrated-v1/approved/batch3-map/completion-v2/Layers.png | map |
| Settings | brand/ui/illustrated-v1/approved/batch3-map/Settings.png | map |
| More | brand/ui/illustrated-v1/approved/batch3-map/More.png | map |
