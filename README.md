# 中學資訊科技科組年度匯報 Dashboard

## 建議使用：獨立前端版

為確保 p5.js 可使用全畫面滑鼠事件，主要版本已改為 `index.html + styles.css + sketch.js`，不再受 Streamlit iframe 限制。p5.js 安裝於本地，不依賴 CDN。

```bash
cd "/Users/macbook/Desktop/CDSJ5/資訊科技科組長/it_department_dashboard"
npm install
python3 -m http.server 8000
```

瀏覽器開啟 `http://localhost:8000`。

原 Streamlit `app.py` 保留作資料版本備份。

這是 Streamlit Dashboard 的現有資料版本，包含：

1. 課程發展
2. 競賽拔尖
3. F5 成果展（個人網站、成績、證書及競賽）
4. 小中銜接
5. 數據評鑑

Dashboard 已整合課程、F5 作品與證書、競賽、小中銜接及數據評鑑。成績與證書 KPI 來自 `2526/全年數據收集/中學英文部成績.xlsx`，競賽 KPI 來自 `程式語言班/2526_競賽成績_20260706.csv`。合格線為 60 分；競賽統計排除初二丁及初三戊。F5 成果展另連結全班 26 個個人網站，並展示 F5B 證書成績圖。

介面採用生成藝術風格：深海軍藍、電光青、螢光綠及橙色節點，配合流場、纖維、網格和數據軌跡表達「基礎 → 實作 → 選才 → 發展」。Hero 以 p5.js 動態生成無限符號；滑鼠會牽引附近粒子並產生光圈軌跡。其餘 Dashboard 使用一致的卡片、指標、表格及側欄視覺系統，並精簡重複文字。

p5.js 由 Streamlit 伺服器端取得並內嵌至 Hero，避免元件 iframe 無法直接載入外部 CDN 腳本。如網絡取得失敗，Hero 右下角會顯示明確提示。

無限符號的粒子公式、單一等比例縮放及金色粒子設定取自本機 `/Users/macbook/Desktop/P5js/infinity_logo`，不加入 SVG、圖片或其他顏色。全畫面滑鼠效果只使用金色線條軌跡；透明 canvas 不接收點擊，因此不影響 Dashboard 操作。

## 專案結構

```text
it_department_dashboard/
├── app.py
├── assets/
│   └── p5_hero.html
├── requirements.txt
├── README.md
└── data/
    └── .gitkeep
```

## 啟動方法

```bash
cd it_department_dashboard
python -m pip install -r requirements.txt
streamlit run app.py
```

預設瀏覽器網址為 `http://localhost:8501`。

## 日後可接駁資料（目前不設上載介面）

- `程式語言_成績.csv`
- `聖五 26-27 學年 IT 教學規劃.xlsx`
