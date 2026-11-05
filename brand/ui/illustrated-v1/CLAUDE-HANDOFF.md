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

全部1254×1254透明RGBA。保持完整畫布等比縮放，不依bbox裁成滿版，不套單色tint，不重描或改成貼紙。40dp暖白 #FFFCF6 圓鈕，圖示先依20／24dp比較；xxxhdpi對應80／96px。一般／選取共用核准原PNG，互動狀態由容器處理，不改圖像。40dp是視覺容器，Android實際觸控區依App既有規則處理。

[已選組合圖](approved/current-set.png)；[已選地圖預覽](approved/current-preview.html)；[風格規範](ILLUSTRATED-STYLE.md)。軟陰影與透明邊緣不得用限色破壞；20dp細節合併、低alpha邊緣與實機對比須由App端驗證。本repo未改App、未做實機驗證；本次只提供素材與交接。

原始輸出、完整生成prompt、附圖來源及實測metadata存於provenance/。其中status=candidate是生成當時歷史紀錄，現行核准以manifest為準。新功能延伸依同畫法生成，必須另行核准。
