# 元素菇環繞特效 · v0.9 強化版（已核准）

使用者已明確核准本版，並要求不保留先前版本。目前只保留火、水、電、毒、水晶這五種強化特效；先前元素特效及方向探索圖已移除。

- 火：大火舌、寬火流與較大的火星。
- 水：左右浪頭、白色浪花與大水滴。
- 電：分岔粗電弧、亮芯與放射電火花。
- 毒：薄荷綠／紫色旋渦、雲團與泡泡。
- 水晶：大型稜晶碎片與強化軌跡。

[完整大圖](review/element-orbits.png) · [特效開關、尺寸及深淺底檢閱](review/index.html) · [素材規格](catalog.json) · [透明素材 ZIP](mushroom-scout-element-effects-v0.9.zip) · [核准紀錄](../../approvals/2026-11-01-element-orbit-bold-v0.9.md)

`layers/` 為五張原始透明特效 PNG；`composites/` 為五張 1254×1254 透明合成圖。v0.5 原始蘑菇是本版的組合來源，保留不變。特效的上下互補區域分置蘑菇後方與前方，合成參數保存在 catalog，檢閱頁可切換特效開關。

本次核准涵蓋這五種特效與合成配置；不包含其他功能圖示、執行時動畫、平台密度包或 App 整合。`approval.json` 綁定核准的圖層與合成圖 hash；重建或打包時會驗證，避免變更後誤用核准狀態。

`PROMPTS.json` 保存實際生成提示詞；其中已移除來源的路徑僅為生成紀錄，不是可用資產或重建依賴。舊版影像未封存到素材包。原始 PNG 的淡 alpha 光暈可能延伸到畫布邊緣，實際 alpha／bbox 以 catalog 為準。

重建：於完整設計 repo 根目錄執行：

```sh
/workspace/.design-venv/bin/python tools/build_element_effects_v09.py
node tools/render_element_effects_v09.cjs
/workspace/.design-venv/bin/python tools/package_element_effects_v09.py
python3 tools/build_overview.py
node tools/render_overview.cjs
```

需 Pillow 13、Playwright、Chromium；本機 HTTP 與瀏覽器可能需要環境允許。HTML 從 repo 根目錄提供靜態 HTTP。

Repository：yaossr02/mushroom-scout-design；交付分支 main；原始設計來源基底 commit 11e9e3438483e01c753cf07ff3a7c2fa4d05b3ec。素材核准與 hash 以本目錄 catalog 和 approval 為準，未匯入 App。
