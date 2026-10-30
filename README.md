# Mushroom Scout Design

蘑菇偵察的獨立設計素材庫。最新方向：**Cream Gumdrop Botanical 非擬人化自然蘑菇**。

## v0.5 非擬人化全系列（已定稿）

依使用者要求，蘑菇移除所有眼睛、嘴巴、腮紅、表情與人物配件，採自然素色菇柄。先前擬人版只保留作歷史，不能作新稿參考或新版 App 素材。

1. [15 種蘑菇與植物圖板](brand/reviews/v0.5/01-mushrooms.png)
2. [尺寸與狀態圖板](brand/reviews/v0.5/02-marker-system.png)
3. [App／平台品牌圖板](brand/reviews/v0.5/03-brand-platforms.png)

[完整審核說明](brand/reviews/v0.5/REVIEW.md) · [原檔互動頁](brand/reviews/v0.5/review.html) · [核准原稿](brand/approved/v0.5/) · [固定版本 manifest](brand/approved/v0.5/manifest.json) · [核准紀錄](brand/approvals/2026-10-31-botanical-v0.5.md) · [方向變更紀錄](brand/direction-change-v0.5.md)

新版 15 張蘑菇＋4 張品牌／平台圖示已核准；葉芽與綠色花苞沿用非擬人化核准原圖。本次核准同時涵蓋尺寸／狀態設計，固定版本存於 approved/v0.5/；未來新增或修改素材仍須另行審核。圖板是直接渲染原圖的瀏覽器截圖，HTML 請以本機靜態 HTTP 開啟，GitHub 可直接看 PNG。

## 共同規範

- [品牌規範](brand/STYLE.md)
- [素材目錄與實際規格](brand/catalog.json)：先看 current_direction_version 與 active_reference，不能只看歷史 approved。
- [生成模板](brand/prompts/TEMPLATE.md)與[圖示用途盤點](brand/icon-inventory.md)
- Codex 先讀 [AGENTS.md](AGENTS.md) 與 [brand-icons 技能](.agents/skills/brand-icons/SKILL.md)。
- Claude Code 先讀 [CLAUDE.md](CLAUDE.md)，共用相同 STYLE，不另建另一套規範。沒有圖片生成能力時產出 brief，不偽造完成。

## 檢查與交接

Python／Pillow 的 catalog 與平台檢查，以及 Playwright／Chromium 的互動檢閱與截圖工具位於 [tools](tools/)。圖示設計核准之後才整理正式尺寸、透明邊緣、平台密度與 AppIcon 集合；不將 PNG 偽裝成 SVG。

[後續流程](brand/ROADMAP.md)仍在設計 repo 進行；App 匯入需另行授權，指定 commit SHA 與核准素材版本，不替換分類器模板或 HOG。

## 歷史版本

v0.1–v0.4 的檔案、圖板、提示詞及核准紀錄仍在 brand/ 下保留供追溯。它們不能作新版蘑菇的生成參考。植物核准不受影響。
