# 檢閱與驗證 · 2026-11-05

本批44張新PNG全部為candidate；金盆D直接引用既有核准原圖。沒有新的核准紀錄、approved manifest、App整合或推送。

## 已完成的檢查

- 42次image_gen生成皆成功，每次附上三張實際原圖；額外2張Expand依使用者授權機械翻轉。
- 44張均1254×1254 RGBA，alpha 0–255，主體alpha128 bbox四周約8%留白；尺寸、alpha、bbox與SHA-256逐張記錄於catalog及METADATA。
- Collapse／Expand的完整RGBA矩陣逐像素上下翻轉相等，不只輪廓相似。Expand的原始輸出欄位明列是Collapse模型來源的逐位元複本，不宣稱獨立模型生成。
- 既有核准圖、核准manifest與核准紀錄，均與生成前protected-hashes.json一致。
- 人工查看14張操作符號：Play向右、Pause兩柱、Stop實心無洞、SkipBack左側立線加兩個向左三角、SkipForward兩個向右三角加右側立線、Check標準勾、Close標準叉。唯讀形狀測量亦確認Skip各三個主要連通塊及三角質心方向、Stop的alpha128遮罩沒有內洞，見control-shape-measurements.json。
- 瀏覽器364個圖片引用全部解碼，沒有頁面腳本錯誤；所有圓寬40px，兩條懸浮列各16顆、圖示24／28px；兩張地圖各右側9顆、頂欄2顆、更多1顆、圖示32px。Collapse／Expand連動與ReturnToApp切換通過，見browser-layout-check.json。
- 無文字辨識區44張，圖像沒有用途文字，答案在獨立檔案且頁內預設收合；沒有做真人盲測。

## 視覺觀察

Auto沿用目前核准C「果實＋金色循環箭頭」；GoldBasin沿用D「金盆＋珊瑚紅向下箭頭」。ReturnToApp A是紅菇＋紅色向左回頭箭頭，B是葉屋＋紅色回頭箭頭，主體與箭頭方向皆有差異。A在24dp時回頭箭頭與菇柄距離較近；是否容易辨識，請用semantic-distinction.png及無文字頁比較，不宣稱所有使用者必然不會混淆。

Collapse／Expand A方向較直接；B更像捲葉，方向較依賴整體語境。Locate A有草地芽苗，Teleport A有金色光圈；32dp較能保留這個差異。More A/B都是三個橫排物件，沒有變成直排。

全套使用同樣霧面體積與柔和明暗。低alpha模型邊緣按原始輸出保留，尚未做Android實機檢查。PNG檢閱板的縮放僅供比較，HTML的CSS尺寸與xxxhdpi原尺寸輸出才是本次版型檢閱依據。
