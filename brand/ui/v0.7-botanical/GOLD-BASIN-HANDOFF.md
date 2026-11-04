# Claude App 實作交接：拉金盆

> 更新：遊戲懸浮列已改採核准的 C 金盆圓角貼紙 v2 整套。浮列請優先讀 [FLOATBAR-CLAUDE-HANDOFF.md](FLOATBAR-CLAUDE-HANDOFF.md)，使用 `approved/floatbar-C-v2/GoldBasin.png`。下文保留為先前單張v6交接歷史，不是目前浮列匯入來源。

本文件對應使用者於 2026-11-04 明確核准的 v6，其他金盆歷史候選不可代用。

- 設計 repo：yaossr02/mushroom-scout-design，遠端 main。
- 素材 ID：gold-planter-swipe-down-v6；語意 ID：GoldBasin。
- 原圖：brand/ui/v0.7-botanical/candidates/gold-planter-swipe-down-v6/icon.png（目錄名 candidates 為迭代保存位置；此檔已核准）。
- 格式：1254×1254 RGBA 透明 PNG，非 SVG／VectorDrawable。
- SHA-256：567eb40708da42e83b882d1e2491cfa56ee0a1bdc0bb0f18f773a4166b736aee。

請以同目錄 approval.json 的 sha256 驗證 v6 原檔，核准紀錄為 brand/approvals/2026-11-04-gold-planter-swipe-down-v6.md。

App 目標：scan/FloatMenu.kt 的 functionEntries「拉金盆」，目前暫用 AppIcon.Locate。新增獨立 GoldBasin 圖示用途並僅替換該功能入口；保留共用 Locate 的其他用途。兩態共用原圖，選取沿既有奶油容器／綠框／圓點方式；深色使用奶油承托底。

圖示內容：遊戲參考改製的圓腹金色花盆、土壤、單葉幼苗、右側珊瑚紅向下滑動箭頭，沒有手部。匯入時不要重新生成、替換成上箭頭、或套用其他候選。平台密度與光學留白可在 App 匯入流程處理，驗證實際懸浮鈕顯示；本設計 repo 尚未修改 App。
