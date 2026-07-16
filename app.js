const navigationButtons = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const resizeChart = id => {
  const chart = document.getElementById(id);
  if (chart) Plotly.Plots.resize(chart);
};

const pageCharts = {
  'primary': ['primary-bar-chart', 'primary-histogram'],
  'secondary-curriculum': ['bar-chart', 'histogram'],
  'secondary-outcomes': ['competition-capability-chart', 'competition-class-chart', 'certificate-chart']
};

navigationButtons.forEach(button => {
  button.addEventListener('click', () => {
    navigationButtons.forEach(item => item.classList.remove('active'));
    pages.forEach(page => page.classList.remove('active'));
    button.classList.add('active');
    document.getElementById(button.dataset.page).classList.add('active');
    const charts = pageCharts[button.dataset.page];
    if (charts) window.setTimeout(() => charts.forEach(resizeChart), 50);
  });
});

const chartConfig = {
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d']
};

const chartLayout = {
  paper_bgcolor: '#ffffff',
  plot_bgcolor: '#ffffff',
  font: { family: 'Inter, Noto Sans TC, sans-serif', color: '#12263b' },
  margin: { l: 55, r: 25, t: 62, b: 50 }
};

Plotly.newPlot('competition-capability-chart', [{
  labels: ['網站／小程序', '機械人／智能裝置', '資訊科技綜合', '算法／編程', 'AI／網絡安全', '3D 建模', 'Office 應用'],
  values: [11, 10, 7, 6, 6, 2, 1],
  type: 'pie',
  hole: 0.56,
  textinfo: 'label+value',
  textposition: 'outside',
  marker: { colors: ['#224870', '#4ba9c8', '#e8bd48', '#75c9ae', '#e76f51', '#9aa8b3', '#d9a441'] },
  hovertemplate: '%{label}<br>%{value} 項（%{percent}）<extra></extra>'
}], {
  ...chartLayout,
  title: '能力範圍組成',
  margin: { l: 45, r: 45, t: 62, b: 42 },
  showlegend: false,
  annotations: [{ text: '<b>43</b><br>項成果', x: 0.5, y: 0.5, showarrow: false, font: { size: 18, color: '#0a1d2f' } }]
}, chartConfig);

Plotly.newPlot('competition-class-chart', [{
  x: ['F3A', 'F4B', 'F6B', 'F3B', 'F5B', 'F2B', 'F4A'],
  y: [13, 12, 7, 6, 2, 2, 1],
  type: 'bar',
  text: [13, 12, 7, 6, 2, 2, 1],
  textposition: 'outside',
  marker: { color: ['#e8bd48', '#224870', '#4ba9c8', '#75c9ae', '#d9a441', '#8da4b2', '#c7d2d9'] }
}], {
  ...chartLayout,
  title: '各班獲獎貢獻',
  margin: { l: 55, r: 30, t: 62, b: 48 },
  yaxis: { title: '獲獎項數', dtick: 2, range: [0, 15] },
  showlegend: false
}, chartConfig);

Plotly.newPlot('bar-chart', [
  { x: ['F1', 'F2', 'F3', 'F4', 'F5'], y: [100, 100, 77.8, 100, 97.6], name: '合格率', type: 'bar', marker: { color: '#e8bd48' }, texttemplate: '%{y:.1f}%', textposition: 'outside' },
  { x: ['F1', 'F2', 'F3', 'F4', 'F5'], y: [26.8, 46.3, 30.2, 45.8, 28.6], name: '80 分或以上比率', type: 'bar', marker: { color: '#0a1d2f' }, texttemplate: '%{y:.1f}%', textposition: 'outside' }
], {
  ...chartLayout,
  title: '各級合格率與高分比率',
  barmode: 'group',
  yaxis: { range: [0, 112], title: '百分比', ticksuffix: '%' }
}, chartConfig);

Plotly.newPlot('histogram', [{
  x: ['60 分以下', '60–69', '70–79', '80–89', '90–100'],
  y: [15, 62, 113, 81, 29],
  type: 'bar',
  text: [15, 62, 113, 81, 29],
  textposition: 'outside',
  marker: { color: ['#e76f51', '#8ecae6', '#3aa6a0', '#e8bd48', '#0a1d2f'] }
}], {
  ...chartLayout,
  title: '300 名學生的全年成績分布',
  xaxis: { title: '全年總成績區間' },
  yaxis: { title: '人數' }
}, chartConfig);

Plotly.newPlot('primary-bar-chart', [
  { x: ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'], y: [100, 100, 98.4, 100, 100, 100], name: '合格率', type: 'bar', marker: { color: '#75c9ae' }, texttemplate: '%{y:.1f}%', textposition: 'outside' },
  { x: ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'], y: [89.8, 85.0, 43.8, 82.6, 95.2, 69.6], name: '80 分或以上比率', type: 'bar', marker: { color: '#224870' }, texttemplate: '%{y:.1f}%', textposition: 'outside' }
], {
  ...chartLayout,
  title: '小學英文部各級合格率與高分比率',
  barmode: 'group',
  yaxis: { range: [0, 112], title: '百分比', ticksuffix: '%' }
}, chartConfig);

Plotly.newPlot('primary-histogram', [{
  x: ['60 分以下', '60–69', '70–79', '80–89', '90–100'],
  y: [1, 10, 72, 159, 129],
  type: 'bar',
  text: [1, 10, 72, 159, 129],
  textposition: 'outside',
  marker: { color: ['#e76f51', '#8ecae6', '#3aa6a0', '#75c9ae', '#224870'] }
}], {
  ...chartLayout,
  title: '小學英文部 371 名學生的全年成績分布',
  xaxis: { title: '全年總成績區間' },
  yaxis: { title: '人數' }
}, chartConfig);

Plotly.newPlot('certificate-chart', [{
  x: ['未取得', '取得 1 張', '取得 2 張', '取得 3 張或以上'],
  y: [3, 4, 18, 1],
  type: 'bar',
  text: [3, 4, 18, 1],
  textposition: 'outside',
  marker: { color: ['#e76f51', '#8ecae6', '#e8bd48', '#0a1d2f'] }
}], {
  ...chartLayout,
  title: 'F5B 學生取得證書數分布',
  xaxis: { title: '取得證書數' },
  yaxis: { title: '學生人數', range: [0, 21] },
  showlegend: false
}, chartConfig);
