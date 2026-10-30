# Mushroom Scout Design

蘑菇偵察的獨立品牌與圖示素材庫。選定方向為 **B 奶油軟糖 / Cream Gumdrop**。

## 基準包狀態

- [已核准的四個角色 v0.1](brand/approved/v0.1/)：紅蘑菇、火蘑菇、水晶蘑菇、葉芽。
- [綠色花苞 v0.2（待確認）](brand/candidates/v0.2/flower-bud.png)：依使用者要求改為綠色。
- [目前原檔檢閱頁](brand/reviews/v0.2/review.html)：下載或 clone 後開啟，可切換底色與 32／48／64 px。
- [核准紀錄與雜湊](brand/approvals/2026-10-31-foundation.md)
- [品牌規範](brand/STYLE.md)、[素材目錄](brand/catalog.json)、[圖示盤點](brand/icon-inventory.md)、[生成提示詞](brand/prompts/)
- [歷史比較圖板 v0.1](brand/reviews/v0.1/comparison-board.png)：含已拒絕的粉色花苞，僅供追溯，不作目前花苞參考。

四個角色的視覺設計已定稿，原稿副本存於 approved 並固定 hash。正式輸出仍需整理透明邊緣與尺寸；不要從圖板裁切素材。後續生成優先附上已核准角色參考，花苞必須為綠色。

## 下一次新增圖示

Codex 先讀 [AGENTS.md](AGENTS.md) 與 [brand-icons 技能](.agents/skills/brand-icons/SKILL.md)；Claude Code 先讀 [CLAUDE.md](CLAUDE.md)。兩者共用相同品牌規範與素材目錄。此 repo 沒有 App 建置或常駐伺服器需求。

生成工具支援情況依執行環境而異；Claude 若沒有圖片生成工具，請產出完整生成 brief，待具備工具的任務生成，不能以其他風格的素材替代。

## 驗證

使用 Python 3 與 Pillow：`python tools/validate_assets.py`。檢查檔案雜湊、尺寸、RGBA、透明邊界與審核狀態，不能替代人工視覺核准。Pillow 可在獨立 venv 安裝，不需要變更 App repo。

本 repo 包含已核准設計、候選與文件，未更動 `mushroom-scout`。App 匯入時需指定本 repo commit SHA 與核准素材 ID；不得替換辨識模板或 HOG 模型。
