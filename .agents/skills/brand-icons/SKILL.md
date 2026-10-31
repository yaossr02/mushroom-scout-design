---
name: brand-icons
description: 依 Mushroom Scout 的 Cream Gumdrop 品牌規範建立、比較與交接圖示候選。
---

1. 讀取根目錄 `AGENTS.md`、`brand/STYLE.md`、`brand/catalog.json`。檢查工作目錄與 Git 變更，保留既有工作。
2. 確定圖示 ID、用途、尺寸與要維持的角色特徵。沒有指定時按現有圖示盤點選題，不把未啟用功能誤認成必須新增。

功能 glyph 沿用 Phosphor 時，先讀 `brand/ui/v0.6/README.md` 與其 catalog，使用固定版上游 SVG／XML 匯出與用途映射流程，不用圖片模型重畫既有向量。v0.6 是獨立待確認交付包，不能套用 v0.5 蘑菇核准；MIT 授權必須保留。
3. 在 catalog 尋找符合最新 STYLE、且非 active_reference:false 的 approved 同類參考並查看圖片。v0.5 全套已核准，優先附上 brand/approved/v0.5/ 中對應原圖，紅菇為主參考；禁止退回帶臉 B 圖板與歷史角色。文字規範不能取代附圖參考。
4. 使用 `brand/prompts/TEMPLATE.md`，固定角色、材質、光線與構圖欄位，只調整題材。紀錄實際完整提示詞與引用檔案。不要承諾 seed 或跨模型逐像素一致。
5. 用實際可用的圖片生成／編輯工具生成透明背景獨立圖示。缺少工具時，交付 brief 並清楚說明，不能假造完成。保留原始輸出，新檔存入新的候選版本。
6. 讀取實際尺寸、模式、alpha 範圍、主體 bbox 與 SHA-256，寫入 catalog。提示詞中的尺寸只是要求，不是已完成規格。
7. 比較圖板可用圖片工具製作，但要標為示意；另提供直接引用原圖的 HTML 32／48／64 px 檢閱頁、淺深色與棋盤底及地圖定位示意。不要擷取圖板充當正式資產。
8. 執行 `python tools/validate_assets.py`，再人工檢閱角色比例、表情、帽型、光線、細節與透明邊緣。自動通過不是視覺核准。
9. 交付具體候選、差異與限制讓使用者選擇。只有明確核准才變更 approved 記錄。不要為完成任務而自動核准。
10. 依任務授權提交／推送設計 repo；不自動修改 App repo 或匯入候選。每次交接提供 repo、分支、commit、素材 ID 與狀態。
