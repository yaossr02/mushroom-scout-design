# Claude 交接：懸浮功能列 C 金盆圓角貼紙 v2

使用者已核准16張並要求推送。請從設計 repo `yaossr02/mushroom-scout-design` 的交接 commit 取用整套，不要混用先前 A／B／C-v1 或舊金盆v6。

## 直接取用

- 核准來源目錄：`brand/ui/v0.7-botanical/approved/floatbar-C-v2/`。
- 映射與 SHA-256：同目錄 `manifest.json`，每個 `assets[].id` 對應一張同名PNG。
- 設計方式：`brand/ui/v0.7-botanical/FLOATBAR-STYLE.md`。
- 核准紀錄：`brand/approvals/2026-11-04-floatbar-C-v2.md`。
- 視覺檢閱：`brand/ui/v0.7-botanical/approved/floatbar-C-v2/overview.png`、`review.png`、`index.html`。

PNG為1254×1254透明RGBA，最多三種平面色，約8%安全邊；不是向量或已完成的平台密度包。請依manifest驗證每張圖的hash再匯入。

## 替換範圍

主功能：HideFloat（隱藏）、GoldBasin（金盆）、Ticket（抽獎）、Dispatch（派遣）、Feed（餵果）、LightSpeed（光速）、ReturnToApp（回到App）、Close（關閉）、FloatMenu（主鈕）。

次要控制：Play、Pause、SkipBack、SkipForward、Stop、GameReturn（回到遊戲）、Check。

請檢查 App 當前的懸浮列、控制列資源和操作映射，再用以上語意ID逐項接上。`scan/FloatMenu.kt`／`functionEntries` 是已知入口；本設計工作沒有讀取最新App實作，因此不把未知檔名或行號當成已驗證資訊。

只替換遊戲畫面上的overlay圖示；不要全域取代共用AppIcon而影響App內圖示。「拉金盆」應使用這套的 `GoldBasin.png`，不再暫用Locate；定位用途繼續保留原圖示。ReturnToApp與GameReturn是不同動作，SkipBack與SkipForward方向相反。保留現有動作、點擊範圍與功能行為。

## 顯示與驗收

保留40dp暖白 `#FFFCF6` 圓與深色膠囊短標籤，圖示20dp並驗24dp。匯入正式來源PNG，按平台流程輸出合適密度，不要把檢閱截圖、遊戲背景、generated-original、候選誤稿或整張比較圖放入App。

在高飽和綠草地、花和蘑菇的真實遊戲畫面上確認辨識、對齊、透明邊緣、裁切、按下與停用狀態，保留實機截圖供使用者比較。來源圖已帶安全邊，注意不要在容器再加一層讓主體過小的padding。

目前只有瀏覽器版型與模擬背景檢查；使用者未提供附件實機畫面。原定1.75dp最細線、3dp點綴及金盆箭頭門檻仍有篩檢警示，不能宣稱全部數值已通過。珊瑚紅2.874:1為使用者已接受的品牌色例外。請保留這些限制並做實機驗證；若必須改圖才能達標，回報差異並另存新稿，不要偷偷修改核准來源。

此設計repo沒有修改、建置或部署App。設計被核准也不代表已完成程式整合。

## 此次發布範圍

遠端只包含16張核准PNG、對應提示詞、固定manifest、設計規則及只展示核准素材的檢閱頁。未選用A／B／C-v1、候選誤稿與生成中間圖仍保留在本地，未隨此次推送。manifest的source_workspace_only是來源追溯資訊，不是匯入路徑；請只讀assets[].path。
