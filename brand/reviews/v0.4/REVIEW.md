# v0.4：1–3 聯合審核包

狀態：整批 candidate，尚未核准。既有 12 個素材的核准保持不變。

這批的比較圖板是 `review.html` 的瀏覽器截圖，直接呈現 PNG 原檔與 CSS 組合，不是重新生成的插畫。原始圖、生成提示詞、系統 tokens 與平台規格均保留。

## 1｜補齊蘑菇系列

[五種蘑菇圖板](01-mushrooms.png)

- water-mushroom：水滴帽與水滴裝飾。
- electric-mushroom：圓鈍閃電帽與單一閃電標記。
- poison-mushroom：三瓣連接泡泡帽；不使用恐怖符號。
- event-mushroom：奶油黃斜紋派對帽，頂端接合星星。
- unknown-mushroom：灰褐帽與大問號，保留同系列表情。

五張皆為 v0.4，位於 `brand/candidates/v0.4/`。這批補齊後共有 15 個蘑菇基本樣式；其中 10 個已有核准，這 5 個待本次審核。

## 2｜尺寸與狀態系統

[尺寸／狀態圖板](02-marker-system.png)

- 四級倍率：小 0.85、一般 1、大 1.15、巨大 1.3，沿用既有 App 層級。
- 大／巨以奶油金圓形徽章標記。
- 六種狀態：一般、選取、進行中、暫停、完成、過期。
- 狀態同時使用線型、文字與顏色；過期只將角色降至 55% 透明度，狀態文字不變淡。
- 腳底 anchor 固定；圖示、外圈、大小徽章、狀態標籤為獨立圖層。
- 檢閱頁可切換所有 15 種蘑菇，並檢視大小與狀態疊加。

規格：`brand/systems/v0.4/marker-system.json` 與 `marker-system.css`。這是共享視覺系統，不是為每個狀態重新畫一個角色，也不是已整合的 Android／iOS 程式碼。

## 3｜App／通知品牌圖示

[平台品牌圖板](03-brand-platforms.png)

| 候選 | 交付 |
| --- | --- |
| ios-app-icon | 不透明、無內建圓角的方形原圖，作 iOS 與品牌主圖示候選 |
| android-adaptive-foreground | 透明前景，角色＋象牙白掃描框 |
| Android adaptive 背景 | 純鼠尾草深綠 `#55735B`，獨立色彩 XML |
| android-themed-monochrome | 黑色 alpha 遮罩，系統可著色；淺深主題預覽 |
| notification-mushroom | 簡化蘑菇剪影與兩個透明斑點孔；16／24／32 CSS px 預覽 |

平台規格見 `brand/systems/v0.4/platform-plan.json`。Android 前景 source scale=0.8，主題單色 source scale=0.65；採 108dp 設計格、72dp 可見視窗、66dp 安全圈。瀏覽器提供圓形、圓角方形與 squircle 近似遮罩。

單色與通知來源刻意為黑色，使用 alpha 由系統著色；不是黑底圖片。原先有雜點的白色嘗試只保留在 rejected-attempts 供追溯，不能拿來使用。

## 已完成的檢查

- 素材 hash、尺寸、RGB／RGBA 與透明政策。
- iOS 候選原圖確為不透明 RGB，實際 1254×1254；未偽稱已輸出 1024px。
- 前景／單色在指定縮放下，alpha ≥128 像素均位於 66dp 安全圈。
- 單色與通知主體為近黑 alpha 遮罩；透明孔與輪廓經實際瀏覽器著色截圖檢視。
- 所有 15 種蘑菇在尺寸／狀態頁皆可切換，深淺底色與安全圈切換通過。
- 三張瀏覽器截圖已人工檢閱；瀏覽器無頁面錯誤或 HTTP 資源錯誤。

詳見 `browser-check.json` 與 `technical-check.json`。

## 第 4 階段才進行的工作

正式畫布與光學大小、低 alpha 邊緣整理、1024px master、Android 各密度／XML／mask 資源、iOS AppIcon 集合，以及實機整合。原始 PNG 不覆寫。此包已完成 1–3 的候選設計，不表示可直接發布 App。

檢閱 HTML 建議透過本機靜態 HTTP 開啟，CSS mask 受瀏覽器檔案來源限制；GitHub 可直接看上方三張 PNG。可分別核准 1、2、3 或指出各區需要修改的項目。
