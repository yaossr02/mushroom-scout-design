# 設計檢閱工具

目前使用 v0.5 的 `build_review_v05.py`、`render_review_v05.cjs` 與 `validate_v05.py`；v0.4 工具保留供歷史追溯，不用來製作新版。新版會排除 active_reference:false 的歷史素材。`validate_assets.py` 同時檢查新版參考政策，但不以程式判定圖中是否有臉。

這些工具只讀取 PNG 原檔，建立 HTML 與瀏覽器截圖，不透過程式重畫或修改角色。

- `validate_assets.py`：Pillow；檢查 catalog hash、實際尺寸、alpha 政策與核准紀錄。
- `build_review_v04.py`：Python 標準函式庫；從 catalog 與系統 tokens 重建 v0.4 原檔檢閱頁。
- `render_review_v04.cjs`：Node、Playwright 與 Chromium；對靜態 HTTP 提供的設計 repo 執行互動檢查並截取三區圖板。可用 `CHROMIUM_PATH` 與 `REVIEW_BASE_URL` 指定本機執行設定。預設路徑針對本次雲端機器。
- `validate_v04.py`：Pillow 13；驗證 alpha 遮罩、安全圈、不透明主圖示與截圖 hash，輸出 technical-check.json。

本次用 Pillow 13.0.0。`render_review_v04.cjs` 的 Playwright 為雲端預裝依賴；若在其他機器執行，需先安裝 Playwright 與可執行的 Chromium。Python 可使用獨立 venv，避免更動系統環境。

順序：重建 HTML → 啟動本機靜態 HTTP → 執行瀏覽器互動檢查與截圖 → 執行兩個 validator。只在原圖、規格或檢閱頁變更時重做受影響的檢查。

截圖是頁面的實際渲染結果，不等同 App 實機驗證。檢查通過不會把 candidate 自動變為 approved。
