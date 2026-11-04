# B 植物線條 · 完整功能圖示 v0.7

沿用使用者選定並核准的 B Botanical Line：圓潤鼠尾草綠輪廓、奶油色主體，少量珊瑚紅／暖黃點綴，植物細節只出現在適合的用途。

## 範圍與核准

- **57 項功能用途（56 項既有＋拉金盆）＋1 個額外地圖入口，56 張獨立透明 PNG 原圖。**
- 首批搜尋、地圖、掃描、收藏、設定、相簿六張已核准，見 [核准紀錄](../../approvals/2026-11-01-botanical-ui-first-six-v0.7.md)。原圖與核准時的 SHA-256 保持一致。
- 拉金盆 v6 已於 2026-11-04 明確核准，見 [核准紀錄](../../approvals/2026-11-04-gold-planter-swipe-down-v6.md)。其餘 49 張延伸原圖仍為 candidate。
- 數量修正：首批的「地圖」是額外入口，不等於既有的 Layers「圖層」。因此不是首批 6＋剩餘 50；56 項舊用途實際有 5 項於首批完成，其餘 51 項本輪補齊。「新增／放大」共用 plus，「移除／縮小」共用 minus。

## 檢閱與原檔

- [完整圖示檢閱大圖](review/all-icons.png)
- [原圖 32／48／64 px、一般／選取、深色／棋盤底與搜尋檢閱頁](review/index.html)
- [全系列總覽](../../reviews/overview/all-icons-overview.png)
- [素材規格、hash 與 57 項用途映射](catalog.json)
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
python3 tools/build_botanical_review_v07.py
python3 tools/build_overview.py
node tools/render_botanical_review_v07.cjs
```

需要 Pillow、Playwright、Chromium；瀏覽器和暫時本機 HTTP 服務可能需要環境允許。檢查包括 56 項舊 ID 完整映射、56 張原檔的 hash／RGBA／alpha、58 張用途卡、174 個尺寸預覽、58 項選取切換及中英文搜尋。瀏覽器檢查不等於 App 實機測試，也不會自動核准新稿。

## 工作區交接

Repository：`yaossr02/mushroom-scout-design`；交付分支：`main`；原始設計來源基底 commit：`11e9e3438483e01c753cf07ff3a7c2fa4d05b3ec`。素材 ID、狀態與 hash 以 catalog 為準。

`rejected/` 保存停止圖示的第一版誤稿與排除原因；目前 catalog、大圖與用途映射均使用修正版，不包含誤稿。

## 拉金盆專用候選 · 2026-11-04

新增 `GoldBasin`／`gold-basin`：[透明金盆原圖](png/gold-basin.png)，暖金盆身、奶油盆內、圓潤鼠尾草綠輪廓與單葉點綴。狀態為 candidate，未繼承首批核准。完整提示詞與附圖參考見 [GOLD-BASIN-PROMPT.json](GOLD-BASIN-PROMPT.json)，實際尺寸、透明度與 SHA-256 見 catalog。

對應使用者指出的 `scan/FloatMenu.kt` `functionEntries`「拉金盆」，目前 App 暫用 `AppIcon.Locate`；此為專用素材提案，既有 Locate 圖示與用途保留，未修改 App。

更新後共 57 項功能用途＋1 個地圖入口、56 張獨立透明原圖，其中 6 張已核准、50 張待審核。檢閱頁含 58 張用途卡與 174 個尺寸預覽。前述 56 用途／55 原圖／49 候選數量為新增前的批次紀錄；重建時不要執行會重置目錄的 complete_botanical_catalog_v07.py。使用 build_botanical_review_v07.py、build_overview.py 與 render_botanical_review_v07.cjs 更新檢閱即可。

## 拉金盆 · 三款拉拔動作提案（2026-11-04）

舊靜態金盆因拉拔感不足已停用，原檔保留追溯。新版 A「上拔箭頭」、B「拉環提盆」、C「斜拉拖出」均為 candidate，等待選擇與審核；功能用途仍為 GoldBasin，未選定替換素材，也未修改 App。

[三款比較圖](candidates/gold-basin-pull-v2/comparison.png) · [32／48／64 px 與深淺底檢閱](candidates/gold-basin-pull-v2/index.html) · [完整提示詞](candidates/gold-basin-pull-v2/PROMPTS.json)

目前保留 57 項功能用途與額外地圖入口；拉金盆同一用途展示三款，合計 60 張檢閱卡。有效原圖共 58 張（6 已核准、52 待審核），另保留 1 張已停用舊稿。以上數量取代前述第一版金盆數量；全系列總覽已同步更新。

### 拉金盆與完整設計的一體感比較

[三欄完整並排比較圖](candidates/gold-basin-pull-v2/cohesion.png) · [原圖檢閱頁](candidates/gold-basin-pull-v2/cohesion.html)。三欄各放相同 55 張現有功能原圖，只替換 A／B／C 金盆，另附 21 張品牌素材與 5 種元素特效共同基準。原圖不調色、不重畫；候選未核准。

## 拉金盆 · A 方向精簡三款（最新，2026-11-04）

使用者選定舊 A 的向上拉拔方向，要求更簡潔、更融入既有系列；方向選定不代表舊圖或新圖已核准。新增 A1「短箭提盆」、A2「留白上提」、A3「盆緣微箭」，均為 candidate。拿掉葉片、底部橢圓與動態線，改用奶油留白、少量暖黃與短箭頭。

[新三款比較圖](candidates/gold-basin-minimal-v3/comparison.png) · [32／48／64 px、深淺底與既有圖示並排](candidates/gold-basin-minimal-v3/index.html) · [完整提示詞及來源](candidates/gold-basin-minimal-v3/PROMPTS.json)。全系列總覽目前顯示這三款；舊靜態金盆與 v2 三款保留追溯，不再列入有效總覽。有效原圖仍為 58 張（6 已核准、52 待審核），GoldBasin 用途仍待選定最終素材，未修改 App。

## 拉金盆 · 盆形重做三款（最新，2026-11-04）

v3 精簡三款盆形已遭使用者明確否決，標為 rejected 並退出目前總覽；不再作生成參考。保留向上拉拔方向，以圓形金屬盆的橢圓盆口、捲邊與曲面盆壁重新製作：1「薄緣外張盆」、2「圓腹金盆」、3「淺口寬金盆」。三款皆 candidate，尚未核准。

[最新盆形比較圖](candidates/gold-basin-form-v4/comparison.png) · [小尺寸／深淺底與既有圖示並排](candidates/gold-basin-form-v4/index.html) · [完整提示詞及來源](candidates/gold-basin-form-v4/PROMPTS.json)。全系列總覽已改列這三款，原始 RGBA PNG 與實際規格／hash 均保留。頁面可視大小已對齊，未改動原圖。未修改 App。

## 拉金盆 · 遊戲花盆與向下拉手勢（最新，2026-11-04）

依使用者提供的遊戲圖，改為圓腹金色花盆、土壤與單葉幼苗；取消所有箭頭，以獨立手勢勾住盆緣向下拉。使用者明確要求手勢，並非讓花盆長出肢體。新稿 `gold-planter-pull-down-v5` 為 candidate，未核准；舊向上箭頭稿已退出有效總覽、僅供追溯。

[透明原圖](candidates/gold-planter-pull-down-v5/icon.png) · [尺寸與深淺底檢閱](candidates/gold-planter-pull-down-v5/index.html) · [完整提示詞](candidates/gold-planter-pull-down-v5/PROMPT.json)。全系列總覽已更新，現在共 56 張有效功能原圖（6 已核准、50 候選），對應 57 項功能用途與額外地圖入口、58 張用途卡；未修改 App。

## 拉金盆 · 保留盆形、改為向下滑動箭頭（最新，2026-11-04）

使用者已接受 v5 的盆形，但否決手部；依指示移除手，改為盆右側的珊瑚紅向下滑動箭頭。新版 `gold-planter-swipe-down-v6` 完整圖示仍為 candidate，不能把盆形認可視為整張核准。舊手勢稿保留追溯，不列入目前總覽。

[透明原圖](candidates/gold-planter-swipe-down-v6/icon.png) · [小尺寸與整套並排檢閱](candidates/gold-planter-swipe-down-v6/index.html) · [提示詞](candidates/gold-planter-swipe-down-v6/PROMPT.json)。總覽已同步更新，未修改 App。

## 拉金盆正式交接 · v6 已核准（2026-11-04）

使用者已核准完整 `gold-planter-swipe-down-v6` 原圖並要求推送。此前章節為設計迭代紀錄；最新核准狀態以本節、catalog 與核准紀錄為準。

[核准透明原圖](candidates/gold-planter-swipe-down-v6/icon.png) · [核准與 hash](candidates/gold-planter-swipe-down-v6/approval.json)。目前有效原圖共 56 張：7 張已核准、49 張待審核；用途卡 58 張。總覽已同步更新核准標記。

Claude 交接：在 `scan/FloatMenu.kt` 的 `functionEntries` 將「拉金盆」從暫用 `AppIcon.Locate` 改用獨立 `GoldBasin` 素材；既有定位用途繼續使用 Locate。本次未修改 App。此為透明 PNG，平台尺寸整理另由 App 實作處理，不是向量檔。
