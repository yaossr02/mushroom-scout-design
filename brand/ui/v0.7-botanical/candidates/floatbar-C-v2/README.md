# C 金盆風格 · 全套重設計 v2

使用者指示：「請參考C的金盆，其他圖示全部重新設計」。本輪保留 C-v1 金盆原檔不變，其餘15個語意均重新使用 image_gen 生成，每張都以同一金盆附圖作風格參考，沒有沿用舊圖示。本套已獲使用者明確核准，見下方核准紀錄與固定manifest；沒有修改App、全域catalog、active_reference或既有核准PNG。

[全套總覽](overview.png) · [完整檢閱](index.html) · [完整PNG](review.png) · [20dp xxxhdpi](20dp-xxxhdpi-scene.png) · [24dp xxxhdpi](24dp-xxxhdpi-scene.png)

同套語彙：Ink #2E3A2F 實心主體、連續 Cream #FFF1DB 貼紙輪廓、Ink外緣、單一 Coral #F36C63 點綴。使用者已選擇保留珊瑚紅，其對暖白2.874:1為接受的例外。只做機械限色、alpha清理與1254px安全邊整理；沒有大幅加粗、覆蓋奶油邊或程式重畫造型。原始輸出另存 generated-original.png。

每個語意子資料夾有 icon.png、PROMPT.json、metadata.json、previews/。金盆以 hash 驗證與 C-v1 完全相同；它仍保留先前幾何限制，此次完整16張的核准來自使用者最後明確選用，而不是先前被選作參考。其餘新圖的線寬與點綴篩檢結果見 validation.json 和各張檢閱卡；未宣稱全數達到硬性幾何門檻。

檢閱背景沿用模擬草地／花／蘑菇場景，附件實機截圖仍未收到。每格40 CSS px對應40dp佈局模型，圖示20／24 CSS px；DPR4擷取對應80／96實體像素。Phosphor是官方語意參考，未讀App內資源。不將瀏覽器檢閱當成Android實機測試。

重建：在repo根目錄執行本目錄 prepare_review.py，再 node render_review.cjs。只會處理本新目錄，金盆不經像素處理。

## 已核准與固定交付（2026-11-04）

使用者已明確核准完整16張。前文為候選製作歷程；現在以 approval.json、各圖metadata與正式 manifest為準。正式來源在 ../../approved/floatbar-C-v2/，Claude請讀 ../../FLOATBAR-CLAUDE-HANDOFF.md；設計方式已保存為 ../../FLOATBAR-STYLE.md。原PNG像素未修改；所有幾何警示仍保留。prepare_review.py 已加核准hash防護，重建檢閱不會重寫核准圖檔。
