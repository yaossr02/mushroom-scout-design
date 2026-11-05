# 設計素材工作規則

- 最新方向 v0.5 禁止擬人化：蘑菇不得有眼睛、嘴巴、腮紅、表情、人物身體或配件。使用者最新要求優先於舊核准；active_reference:false 的版本只能追溯，不能生成或匯入。

- 使用繁體中文與使用者溝通。只在這個設計 repo 工作；除非另有要求，不變更 App repo、不建立 worktree。
- 新增或修改圖示先讀 `brand/STYLE.md`、`brand/catalog.json` 與 `.agents/skills/brand-icons/SKILL.md`。
- B 概念圖是已選定的風格方向；`candidate` 是待核准素材。不得將候選自動升格為 approved，不得宣稱生成可保證逐像素一致。
- 新稿採新檔名或新版本目錄；保留原始圖、實際提示詞、參考圖、生成日期與實際規格。不得覆蓋已核准素材。
- 有符合最新 STYLE 的 active approved 同類素材時優先使用；目前以 brand/approved/v0.5/ 為蘑菇與品牌基準。禁止回退帶臉 B 圖板；新變體不能繼承核准。
- 圖片生成與編輯使用可用的圖片工具。若工具缺失，交付生成 brief 並說明缺少能力；不要偽稱已生成或已驗證。
- 比較圖板為示意，原檔縮放頁才是尺寸檢閱依據。新生成素材不要自動修改全域品牌規範。
- 匯入 App 需另有指示，且只匯入 approved 素材；不修改分類器模板與模型。

- 維護全系列總覽：未來新增、修改或停用圖示，以及變更核准狀態時，必須同步更新 `brand/reviews/overview/all-icons-overview.png` 與 `README.md` 的總覽說明。直接排列目前有效的原始素材，涵蓋蘑菇、植物、品牌與全部功能用途的一般／選取狀態，標明名稱與實際審核狀態；不混入已停用的歷史版本，不改動素材本身或自動核准候選。交付前確認 README 圖片連結與大圖顯示正常。

- 功能圖示新方向（2026-11-01）：使用者已選定五組比較中的 B「植物線條」，並授權開始修改。採圓潤鼠尾草綠線條、奶油色與少量珊瑚紅／暖黃，葉片只作不影響辨識的點綴。新版於 `brand/ui/v0.7-botanical/`，首批六項已於 2026-11-01 經使用者明確核准，見 `brand/approvals/2026-11-01-botanical-ui-first-six-v0.7.md`；後續新增項仍為 candidate；後續沿此方向延伸，不能回退成通用 Phosphor 或把方向選定視為全套核准。

- 元素菇特效定稿（2026-11-01）：使用者明確核准 `brand/effects/v0.9-orbit-bold/catalog.json` 的五種 B「環繞流動強化版」，並指示「之前的版本不用保留」。核准紀錄為 `brand/approvals/2026-11-01-element-orbit-bold-v0.9.md`；目前只保留這版特效，不得重建或封存先前元素特效及方向探索稿。原始 v0.5 蘑菇是本版組合來源，保留不改。
- 核准的五種元素特效包含大型火舌／浪頭／分岔電弧／毒霧旋渦／晶片；圖層與合成圖 hash 綁定於 `brand/effects/v0.9-orbit-bold/approval.json`，新改稿不能繼承核准。此 B 與功能圖示 B「植物線條」分開；本次核准不擴及其他功能圖示，沒有執行時動畫或 App 整合。

- 懸浮功能列已核准方向（2026-11-04）：遊戲 overlay 專用「C 金盆圓角貼紙 v2」，核准16張，固定交付在 `brand/ui/v0.7-botanical/approved/floatbar-C-v2/manifest.json`。新增／改浮列圖示先讀 `brand/ui/v0.7-botanical/FLOATBAR-STYLE.md`，附上核准 `GoldBasin.png` 與同套用途圖作image_gen參考；墨綠實心、連續奶油貼紙邊、墨綠外keyline、單一珊瑚紅重點。App內一般圖示仍沿既有植物線條方向；不得混用。整套視覺核准不代表線寬警示或實機測試已通過；新變體仍須另行核准。Claude匯入交接見 `FLOATBAR-CLAUDE-HANDOFF.md`。

- 2026-11-05 GoldBasin 最新選用：使用者「我選D」核准蘑菇插圖畫法 D（雙葉、粗下箭頭），正式來源 `brand/ui/approved/gold-planter-illustrated-v1/approval.json`。僅 GoldBasin 取代 v6／C-v2 選用；其他圖示不繼承核准。後續以 v0.5 紅菇／火菇霧面立體插圖作畫法參考，不對這張沿用貼紙規則。核准範圍與Claude交接見正式目錄，尚未接App。

- 2026-11-05 插圖風功能首批已逐項核准：Auto A、Tasks A、Records A、Favorites B、Scan A，正式來源 `brand/ui/illustrated-v1/approved/batch1/manifest.json`；GoldBasin沿用D。後續門面插圖依 `ILLUSTRATED-STYLE.md`，每次附核准D金盆與v0.5紅菇；新功能不繼承核准，16dp小符號不在本系列。App交接 `brand/ui/illustrated-v1/CLAUDE-HANDOFF.md`，本repo不改App。
