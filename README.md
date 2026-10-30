# Mushroom Scout Design

蘑菇偵察的獨立品牌與圖示素材庫。選定方向為 **B 奶油軟糖 / Cream Gumdrop**。

## 第一批基準包 v0.1（待核准）

- [五張透明 PNG](brand/candidates/v0.1/)
- [比較圖板](brand/reviews/v0.1/comparison-board.png)：風格示意，實際資產以 PNG 為準。
- [原檔檢閱頁](brand/reviews/v0.1/review.html)：下載或 clone 後用瀏覽器開啟；GitHub 不直接執行 HTML。
- [品牌規範草案](brand/STYLE.md)
- [素材目錄與規格](brand/catalog.json)
- [既有專案圖示盤點](brand/icon-inventory.md)
- [生成提示詞](brand/prompts/)

目前只核准了 B 的風格方向，**五張新角色尚未核准，不是正式 App 資產**。先檢閱角色、材質、配色與小尺寸辨識度，再逐顆核准、修整透明邊緣並製作正式輸出；不要從比較圖板裁切資產。

## 下一次新增圖示

Codex 先讀 [AGENTS.md](AGENTS.md) 與 [brand-icons 技能](.agents/skills/brand-icons/SKILL.md)；Claude Code 先讀 [CLAUDE.md](CLAUDE.md)。兩者共用相同品牌規範與素材目錄。此 repo 沒有 App 建置或常駐伺服器需求。

生成工具支援情況依執行環境而異；Claude 若沒有圖片生成工具，請產出完整生成 brief，待具備工具的任務生成，不能以其他風格的素材替代。

## 驗證

使用 Python 3 與 Pillow：`python tools/validate_assets.py`。檢查檔案雜湊、尺寸、RGBA、透明邊界與審核狀態，不能替代人工視覺核准。Pillow 可在獨立 venv 安裝，不需要變更 App repo。

本 repo 僅含設計候選與文件，未更動 `mushroom-scout`。App 匯入時需指定本 repo commit SHA 與核准素材 ID；不得替換辨識模板或 HOG 模型。
