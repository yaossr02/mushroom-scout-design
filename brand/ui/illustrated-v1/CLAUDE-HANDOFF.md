# 插圖功能圖示 · Claude 交接

2026-11-05，使用者確認的固定組合如下。前五張來源在 [現行 manifest](approved/current-manifest.json)，GoldBasin沿用其獨立核准；必須按manifest的SHA-256核對，不從候選比較圖裁切。

| 語意 ID | 核准概念 | 正式來源（repo root 相對路徑） |
|---|---|---|
| Auto | C 循環果實 v2 | brand/ui/illustrated-v1/approved/auto-C-v2/icon.png |
| Tasks | A 緞帶紙卷 | brand/ui/illustrated-v1/approved/batch1/Tasks.png |
| Records | A 紅菇圖鑑 | brand/ui/illustrated-v1/approved/batch1/Records.png |
| Favorites | B 金色星花 | brand/ui/illustrated-v1/approved/batch1/Favorites.png |
| Scan | A 放大鏡紅菇 | brand/ui/illustrated-v1/approved/batch1/Scan.png |
| GoldBasin | D 雙葉金盆＋粗下箭頭 | brand/ui/approved/gold-planter-illustrated-v1/icon.png |

前五張用於地圖右側五個主要功能；GoldBasin對應拉金盆，兩者不可混淆：Auto是果實＋循環箭頭，GoldBasin是向下箭頭。其他功能圖示沒有因此被重新設計或核准。

全部1254×1254透明RGBA。保持完整畫布等比縮放，不依bbox裁成滿版，不套單色tint，不重描或改成貼紙。40dp暖白 #FFFCF6 圓鈕，地圖插圖畫32dp（xxxhdpi128px），懸浮列以24／28dp檢閱（96／112px）。一般／選取共用核准原PNG，互動狀態由容器處理，不改圖像。40dp是視覺容器，Android實際觸控區依App既有規則處理。

[已選組合圖](approved/current-set.png)；[已選地圖預覽](approved/current-preview.html)；[風格規範](ILLUSTRATED-STYLE.md)。軟陰影與透明邊緣不得用限色破壞；20dp細節合併、低alpha邊緣與實機對比須由App端驗證。本repo未改App、未做實機驗證；本次只提供素材與交接。

原始輸出、完整生成prompt、附圖來源及實測metadata存於provenance/。其中status=candidate是生成當時歷史紀錄，現行核准以manifest為準。新功能延伸依同畫法生成，必須另行核准。

## 2026-11-05 問卷新增核准（部分完成）

- [懸浮列固定清單](approved/batch2-floatbar/manifest.json)：11張新核准，另沿用D金盆。Feed、ReturnToApp、GameReturn、HideFloat還要重畫。
- [地圖其他圓鈕固定清單](approved/batch3-map/manifest.json)：Locate B、Teleport A、Settings A、More A已核准；Collapse／Expand與Layers還要重畫。
- 新核准圖都在對應批次目錄的 `<ID>.png`；不得從比較板裁切，依manifest的SHA-256取圖。
- 本次兩批皆 `ready_for_full_replacement:false`。使用者要求整套插圖化，懸浮列不能以舊C-v2或被退回的候選補齊、宣稱全套完成；先保管已核准資產，待剩餘項核准後再做整套替換。
- 40dp暖白圓容器；地圖圖示32dp，懸浮列24／28dp。前五項地圖功能及Auto C仍依現行清單。未改App，未做Android實機測試。
- 本問卷的標準操作全部選無葉A：保留清楚的Play／Pause／Stop／Skip／Check／Close形狀，不額外添加葉片或道具。
