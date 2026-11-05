# 懸浮功能列 · 三方向候選 v1

本次共 48 張獨立 image_gen 候選：每方向 9 項主功能＋7 項控制，全部 status=candidate，尚未核准。本次未修改 App、catalog、active_reference 或 v6 核准原圖，也未提交／推送。

> 目前為候選初稿，尚未全數通過硬性幾何門檻。尤其金盆為保住 v6 盆形，撤回會讓盆口與箭頭黏合的過度加粗；其線寬／箭頭寬度警示仍保留。不能把這組視為全部可直接匯入的達標素材。

## 開啟檢閱

從設計 repo 根目錄啟動靜態 HTTP，開啟本目錄 index.html。overview.png 可直接看三方向比較；各方向 index.html／review.png 是完整檢閱。

- ../floatbar-A-v1/：粗線雙色，Ink＋一塊 Coral 或 LeafFill。
- ../floatbar-B-v1/：實心剪影，Ink 大塊面＋Cream 留白＋Coral。
- ../floatbar-C-v1/：圓角貼紙，Ink 主體＋Cream 輪廓＋Coral，外側 Ink keyline 避免奶油融入圓底。

每張子資料夾包含 icon.png、PROMPT.json、metadata.json、generated-original.png、previews/。曾因辨識問題重生的項目另有 attempts/first/，僅供追溯，不是另外的有效候選。icon.png 是目前用於比較的候選；generated-original.png 保留圖像模型原稿。metadata 記錄尺寸、alpha、bbox、SHA-256、實際色票與量測資料。

## 顯示比例

每格為 40 CSS px 暖白 #FFFCF6 圓，圖示分別為 20／24 CSS px，視為 dp 佈局比例；下方為深色膠囊短標籤。另有 2 倍放大示意、32／48／64px 縮圖與逐項 Phosphor 對照。

每方向 20dp-xxxhdpi-scene.png、24dp-xxxhdpi-scene.png 為 DPR4 擷取；圖示分別佔 80／96 實體像素。每張圖的 previews/80px.png 與 96px.png 也對應這兩種 xxxhdpi 尺寸。瀏覽器 CSS px 對應佈局 dp 的模型，不等於已測試 Android 實機密度。

## 已確認的取捨與資料限制

- 使用者明確選擇保留 STYLE 的珊瑚紅 #F36C63，搭配 Ink 邊界；純珊瑚紅對暖白的對比為 2.874:1，未達 3:1，此為已接受的例外。
- Ink #2E3A2F 對暖白為 11.636:1；Leaf #4A6650 為 6.200:1；LeafFill #6E8F5E 為 3.564:1。因此主體使用 Ink，LeafFill 僅作點綴。
- 附件 1、2 尚未收到。遊戲背景為 image_gen 產生的模擬草地／花／蘑菇場景，不是實機截圖，無法宣稱比例或背景與附件完全一致。
- Phosphor 使用官方 @phosphor-icons/core@2.1.1 Bold（MIT），檔案和授權位於 phosphor-reference/。依使用者讀取限制未讀 App 資源，所以是逐一語意對照，尚未確認與目前 App 的圖形完全一致。GoldBasin 的暫用 Locate 以 crosshair 作語意參考。
- 使用者允許 Python 做限色與規格整理；本次保留 image_gen 原稿，做色票量化、alpha 邊緣清理、統一安全邊與等量像素邊緣加粗，不以程式新增語意部件或重畫圖示。
- 來源 icon.png 為最多 3 色、二元 alpha；抗鋸齒預覽及瀏覽器縮放會產生顯示用混色。

## 品質檢查

validation.json 逐張列出格式、安全邊、色票、對比、光學佔比、點綴面積及幾何篩檢。線寬使用距離場中軸的 p10／p50／p90 作診斷，不能等同精確的最細筆畫認證；尖角、交叉和密集細節仍需視覺複核。金盆另估算向下箭頭軸寬。各卡上直接列出未達門檻或需人工檢閱的旗標，未把它們隱藏或視為通過。

挑定風格不代表整套圖示已核准。所有原稿與後續整理稿均為 candidate；沒有 approval.json。

## 重建

從 repo 根目錄執行本目錄的 prepare_candidates.py（保留原稿、機械規格整理），再執行 build_reviews.py（量測與 HTML），最後 node render_reviews.cjs（Chromium 擷取與瀏覽器檢查）。需要 Python/Pillow/numpy/scipy，以及 Node/Playwright/Chromium。只處理本次四個新候選目錄，不讀全 repo。

## 最終篩檢結果
格式檢查48／48通過：1254×1254 RGBA、透明背景、最多3個不透明色票、約8%安全邊、hash一致。這不是所有硬性幾何規格的通過認證。
仍有5張幾何警示：
- A／GoldBasin：ink_ridge_p10_below_1.75dp_review_required, gold_basin_arrow_shaft_below_3dp
- B／GoldBasin：ink_ridge_p10_below_1.75dp_review_required, gold_basin_arrow_shaft_below_3dp
- B／Pause：ink_ridge_p10_below_1.75dp_review_required
- B／Stop：ink_ridge_p10_below_1.75dp_review_required
- C／GoldBasin：ink_ridge_p10_below_1.75dp_review_required, largest_accent_bbox_min_edge_below_3dp, gold_basin_arrow_shaft_below_3dp, gold_basin_arrow_gap_not_clear

瀏覽器通過3份完整檢閱、48張卡片、144個縮圖尺寸樣本與20／24dp佈局檢查；DPR4場景截圖已保存。沒有實際Android overlay測試，沒有實機附件背景驗證。
