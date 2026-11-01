# B 植物線條 · 完整功能圖示 v0.7

沿用使用者選定並核准的 B Botanical Line：圓潤鼠尾草綠輪廓、奶油色主體，少量珊瑚紅／暖黃點綴，植物細節只出現在適合的用途。

## 範圍與核准

- **56 項既有功能用途＋1 個額外地圖入口，55 張獨立透明 PNG 原圖。**
- 首批搜尋、地圖、掃描、收藏、設定、相簿六張已核准，見 [核准紀錄](../../approvals/2026-11-01-botanical-ui-first-six-v0.7.md)。原圖與核准時的 SHA-256 保持一致。
- 其餘 49 張延伸原圖涵蓋剩餘 51 項用途，仍為 candidate，等待這一批的視覺審核。
- 數量修正：首批的「地圖」是額外入口，不等於既有的 Layers「圖層」。因此不是首批 6＋剩餘 50；56 項舊用途實際有 5 項於首批完成，其餘 51 項本輪補齊。「新增／放大」共用 plus，「移除／縮小」共用 minus。

## 檢閱與原檔

- [完整圖示檢閱大圖](review/all-icons.png)
- [原圖 32／48／64 px、一般／選取、深色／棋盤底與搜尋檢閱頁](review/index.html)
- [全系列總覽](../../reviews/overview/all-icons-overview.png)
- [素材規格、hash 與 56 項用途映射](catalog.json)
- [首批提示詞](PROMPTS.json) · [延伸圖示完整提示詞](REMAINING-PROMPTS.json)
- [首批歷史檢閱大圖](review/first-six.png) · [首批歷史檢閱頁](review/first-six.html)

HTML 請從設計 repo 根目錄以本機靜態 HTTP 開啟；PNG 可直接在 GitHub 閱覽。png/ 保存獨立生成原圖，未從比較圖裁切，也沒有以程式重畫原圖。

## 一般／選取與深色介面

兩態使用同一原圖；選取增加奶油底、鼠尾草綠外框與底部圓點。深色介面使用奶油承托底，避免搜尋、掃描等深綠輪廓直接放深底時對比不足。實際容器示例在檢閱頁 CSS 中；PNG 原圖本身不包含容器。

Empty 的中心兩態都保持透明空心，選取只改外部容器，避免表示為已填入。Dispatch 仍是功能占位，Info／Rotate 是保留用途；製作圖示不代表這些功能已啟用。

## 交付邊界

這是全套視覺候選與完整用途映射，原始輸出為 RGBA PNG。未宣稱為 SVG、VectorDrawable、Android 密度包、iOS AppIcon 集合或已完成 App 整合。生成結果仍可能有線寬、色調、光學大小與低 alpha 邊緣差異，正式平台輸出需另行整理。

使用者這次要求修改功能圖示，已取代本批原本沿用 Phosphor 的限制；v0.6 舊包及其 MIT 授權完整保留供追溯，不再作目前總覽的功能圖示。蘑菇與平台品牌原圖、全域品牌規範及 App repo 沒有修改。

## 重建與檢查

在 repo 根目錄執行：

```sh
/workspace/.design-venv/bin/python tools/complete_botanical_catalog_v07.py
python3 tools/build_botanical_review_v07.py
python3 tools/build_overview.py
node tools/render_botanical_review_v07.cjs
```

需要 Pillow、Playwright、Chromium；瀏覽器和暫時本機 HTTP 服務可能需要環境允許。檢查包括 56 項舊 ID 完整映射、55 張原檔的 hash／RGBA／alpha、57 張用途卡、171 個尺寸預覽、57 項選取切換及中英文搜尋。瀏覽器檢查不等於 App 實機測試，也不會自動核准新稿。

## 工作區交接

Repository：`yaossr02/mushroom-scout-design`；交付分支：`main`；原始設計來源基底 commit：`11e9e3438483e01c753cf07ff3a7c2fa4d05b3ec`。素材 ID、狀態與 hash 以 catalog 為準。

`rejected/` 保存停止圖示的第一版誤稿與排除原因；目前 catalog、大圖與用途映射均使用修正版，不包含誤稿。
