# 拉金盆插圖候選 v1

2026-11-05 · 全部 **candidate**，尚未核准；不改 App、既有核准素材或全域設計方向。

以 v6 金盆保持圓腹、厚盆口、土壤、幼苗、短圈足與右側獨立下箭頭；畫法參考已核准 v0.5 紅菇／火菇的霧面立體插圖。每次 image_gen 都附上這三張原圖。`references/` 是原圖逐位元複本，來源與 SHA-256 記於 `manifest.json`。

| 候選 | 生成變因 |
|---|---|
| A-single-leaf | 單葉、圓腹、中等粗箭頭 |
| B-two-leaves | 雙葉、圓腹、中等粗箭頭 |
| C-wide-belly | 單葉、略扁圓腹、較細箭頭 |
| D-bold-arrow | 雙葉、圓腹、較粗箭頭 |

變因是生成要求；實際差異請以原圖判斷，未宣稱幾何或畫法逐像素一致。

## 檢閱

- [互動檢閱頁](index.html)：各候選與原紅菇同畫布尺寸並排、32/48/64 px、80/96 px、透明棋盤與深底；40 CSS px 圓搭 20/24 CSS px 圖示。
- [總覽圖](review-board.png)：同時包含 v6 與現行 C-v2 金盆。
- `map-20dp-xxxhdpi.png`、`map-24dp-xxxhdpi.png`、`grass-20dp-xxxhdpi.png`、`grass-24dp-xxxhdpi.png`：每個圓 160 px（40 dp @4x），圖示 80/96 px（20/24 dp @4x）。PNG 閱覽器縮放會影響視覺大小，以 HTML 的 CSS 尺寸為準。
- 地圖背景為 #EFEBE3，圓底 #FFFCF6；草地沿用既有 image_gen 模擬圖，非 Pikmin Bloom 實機截圖。以上皆為尺寸模擬，未做 Android overlay 實機測試。

每個候選保留 `generated-original.png`、完整 `PROMPT.json`、`generation.json`、交付 `icon.png` 和 `METADATA.json`（實際尺寸、模式、alpha 範圍、非零／128 bbox、SHA-256）。`manifest.json` 彙整全部實測。

`prepare.py` 只用 Pillow 做必要的等比尺寸／透明畫布整理和檢閱排版；保留明暗與原 alpha，不限色、不描邊、不加粗、不修改形狀。低 alpha 邊緣仍保留；正式交付前須再檢查。主體約有 8% 安全邊，以 alpha128 bbox 為尺寸依據。

初步小尺寸觀察：盆腹與獨立箭頭仍可辨識，但土壤、盆口和低葉叢在 20 dp 會合併，24 dp 較清楚。D 的箭頭較有存在感，A 的單葉語意最單純。這些觀察不是核准。

使用者選定並核准後才另建 approval 紀錄及 Claude 交接；本目錄沒有 approval.json，也未更新 catalog 或 active_reference。

## 後續核准 · 2026-11-05

使用者已選D。上方candidate說明與比較板保留生成當時紀錄；D正式狀態與固定原圖見 [核准版本](../../approved/gold-planter-illustrated-v1/approval.json)。A/B/C仍待審核。
