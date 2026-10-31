# App 功能圖示交付包 v0.6

範圍：**52 個既有 Android 用途＋4 個 iOS 補齊用途＝56 個語意用途，92 個獨立向量圖形**。採用專案既定 Phosphor Icons 2.1.1（MIT），未重新繪製圖形，也不是 AI 生成圖示。這是先前未交付的完整功能資產包，可搭配已核准的 v0.5 非擬人化蘑菇與品牌素材。

目前配色／狀態展示與四項補齊映射為 candidate，尚未取得這批的使用者核准；不要把 v0.5 蘑菇核准誤套到新 UI 映射。

## 檢閱

- [地圖與主要功能：21 個用途](review/01-map-main.png)
- [操作與導覽：21 個用途](review/02-actions-navigation.png)
- [自動、懸浮、狀態與 iOS 補齊：14 個用途](review/03-tools-status.png)
- [深色範例](review/04-dark-example.png)
- [可搜尋與切換深淺色的原始向量頁](review/index.html)

每格包含一般／選取狀態，以及 16／18／20 CSS px 預覽。圖示尺寸不等於點擊區；既有介面仍需至少 48dp 觸控範圍。

## 檔案

| 路徑 | 內容 |
| --- | --- |
| svg/ | 92 個原始 Phosphor SVG，256×256 viewBox、currentColor |
| android/drawable/ | 92 個 24dp VectorDrawable XML；85 個既有資源保留原始幾何，7 個為 iOS 語意補齊 |
| png/24/、png/48/ | 184 張透明黑色 PNG；由瀏覽器直接渲染向量，不是生成模型或圖板裁切 |
| sprite.svg | 可用 symbol/use 引用的 SVG sprite |
| catalog.json | 56 個用途的一般／選取映射、來源引用、檔案 hash、配色與使用狀態 |
| sources/AppIcon.kt | 原 App 對照快照，來源 commit 記錄於 catalog；不代表已修改 App |
| LICENSE-phosphor.txt | 上游 MIT 授權，匯入／再散布時必須保留 |
| package-manifest.json | 本交付包各檔案的 SHA-256 與核對規格 |

## 狀態與語意

- 可選取的物件使用 Bold／Fill；加減、箭頭、關閉等動作沿用同一圖形，以色彩與容器呈現選取。
- 新增／放大共用 plus；移除／縮小共用 minus。56 是用途數，不是 56 個彼此不同的圖形。
- Info 與 Rotate 目前在 enum 中保留，沒有查到 literal 呼叫點。
- Dispatch 在自動頁以「重新設計中」占位，不能把這顆圖示交付當成功能已完成。
- iOS 補齊：Photo=image、Success=check-circle、Error=warning-circle、Empty=circle。Empty 兩態保持空心，避免選取後誤示為已填入。
- catalog 的 ios_mapping 只提供語意對照，不包含 Apple SF Symbols 字型或圖形。

## 給 Claude／Codex 匯入

1. 依 catalog 的語意 ID 取得 normal／selected 資源，保留目前 AppIcon 集中映射。
2. Android 優先用 VectorDrawable；網頁用 SVG／sprite；PNG 供需要點陣圖的流程。iOS 可用向量或點陣圖建立對應資產，正式平台資產仍由整合任務處理。
3. 外部 img 載入 SVG 時 currentColor 不一定繼承父層，需用 inline SVG、sprite/use 或 CSS mask 控制著色。PNG 預設黑色，App 可用 tint／template rendering。
4. 不要因為這包有 7 個補齊 XML，就直接在 App enum 新增所有條目；先按實際功能選擇。
5. 保留 MIT 授權與版本來源。使用者核准後再由獨立 App 任務整合，本次沒有修改 App repo。

## 與品牌圖示的差別

這包是搜尋、設定、路線、按鈕與狀態等功能 glyph。蘑菇、植物、App launcher、adaptive／通知品牌圖示仍以 brand/approved/v0.5/ 與既有植物核准版本為準，不用本包替換辨識模型。

## 重建與檢查

`tools/build_ui_pack_v06.py` 讀取 App checkout 與固定版 @phosphor-icons/core 套件，逐項比較既有 pathData，再匯出向量與映射。`tools/render_ui_pack_v06.cjs` 以 Playwright／Chromium 產生圖板及透明 PNG。`tools/validate_ui_pack_v06.py` 檢查完整映射、SVG／XML 幾何、PNG 尺寸與透明度、hash 及授權。

完成後可使用同目錄的 ZIP 交付包。技術檢查與瀏覽器預覽不是 App 實機驗證。
