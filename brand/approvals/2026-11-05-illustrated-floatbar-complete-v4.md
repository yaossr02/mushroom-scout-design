# 懸浮列補齊 · v4三張核准與完整系列交付

2026-11-05（Asia/Taipei）。使用者確認v4比較板：「好, 就確定這些。推上去。」核准Feed、ReturnToApp、GameReturn三張固定PNG。

- Feed：自動循環箭頭＋被咬一口的紅蘋果。
- ReturnToApp：v3 B的金框綠底蘑菇程式主體，配v3 A的黃色彎曲向左返回箭頭。
- GameReturn：同款金框綠底與黃色返回箭頭，中央換成遊戲手把。

三圖規格、SHA-256及來源在 `brand/ui/illustrated-v1/approved/batch2-floatbar/completion-v4/approval.json`；原始模型輸出、完整prompt、實際附圖路徑與metadata保留在同目錄provenance。

完整浮列16項固定來源見completion-v4/manifest.json。GoldBasin直接沿用既有D核准，其他12項沿既有逐張核准，未重畫。地圖原五項及其他七項維持；整套28個語意ID索引在 `brand/ui/illustrated-v1/approved/active-sets.json`。

核准範圍是視覺設計與固定PNG；ready_for_full_replacement指設計資產已齊，不是App已匯入或實機測試已通過。舊partial/current manifest保留歷史不覆蓋；新正式索引以active-sets.json與完整批次manifest為準。沒有改App，未選候選不隨正式包推送。
