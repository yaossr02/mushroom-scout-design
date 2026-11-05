# 候選與設計歷史

2026-11-05，使用者要求「全部推送」，因此將原先只留在本機的候選、原始生成圖、完整prompt、尺寸與透明度紀錄、程式及比較頁一併保存。

**發佈不等於核准。** 本頁是歷史入口，不是App匯入清單。正式28項只用 [illustrated-v1/approved/active-sets.json](illustrated-v1/approved/active-sets.json)，程式交接見 [CLAUDE-HANDOFF.md](illustrated-v1/CLAUDE-HANDOFF.md)。歷史頁的標籤代表生成／檢閱當時狀態；與最新清單不同時以正式清單為準。不要將舊C-v2或未選候選混入正式插圖系列。

## 插圖系列探索

- [金盆插圖v1：四個候選與v0.5紅菇對照](candidates/gold-planter-illustrated-v1/index.html)；D後來獲核准。
- [地圖主要五功能：首輪A/B](illustrated-v1/review/index.html)。
- [Auto v2：三個新概念](illustrated-v1/review/auto-v2/index.html)；C後來獲核准。
- [懸浮列／地圖：首輪44張](illustrated-v1/review/batch2-batch3-v1/index.html)。
- [問卷退回六組：v2重畫14張](illustrated-v1/review/batch2-batch3-rework-v2/index.html)。
- [最後四項：v3重畫8張](illustrated-v1/review/floatbar-final-four-v3/index.html)。
- [最後三項：v4定向融合改稿](illustrated-v1/review/floatbar-last-three-v4/index.html)；三張後來全部獲核准。

## 舊懸浮列風格探索

- [A粗線雙色](v0.7-botanical/candidates/floatbar-A-v1/index.html)。
- [B實心剪影](v0.7-botanical/candidates/floatbar-B-v1/index.html)。
- [C圓角貼紙v1](v0.7-botanical/candidates/floatbar-C-v1/index.html)。
- [C金盆貼紙v2](v0.7-botanical/candidates/floatbar-C-v2/index.html)；其歷史核准不代表仍是目前浮列方向。
- [跨風格／背景與Phosphor對照](v0.7-botanical/candidates/floatbar-review-v1/index.html)。上游Phosphor素材與LICENSE一併保留。

## 檔案保存與檢閱

候選PNG、PROMPT.json、原始模型輸出、generation及metadata均保留原狀；沒有因本次上傳而改寫為approved。歷史metadata中的本機生成來源路徑只供追溯，不代表遠端可取得那個絕對路徑。

[ARCHIVE-INVENTORY.json](ARCHIVE-INVENTORY.json) 記錄本次任務開始時1,381個未追蹤設計檔的路徑、大小及SHA-256；不包含清單自身和本次新加的導覽說明。圖板和HTML只是設計／尺寸示意，不代表Android實機測試。

GitHub可直接開PNG；互動HTML建議以repo根目錄的本機靜態HTTP開啟，例如 `python -m http.server 8000`，再瀏覽對應路徑。部分歷史頁使用 `/brand/...` 絕對網站路徑，因此須以repo根目錄為伺服器根目錄。
