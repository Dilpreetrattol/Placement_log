/**
 * PlacementLog dashboard charts.
 *
 * Each render* function takes a <canvas> id plus the labels/values arrays
 * rendered into the page by dashboard.html (from main.dashboard()) and
 * draws a single-series Chart.js bar chart. Colors follow this project's
 * data-viz conventions: a single accent hue is used wherever the axis
 * labels already carry category identity (no legend needed for one
 * series), and the reserved status palette (good/warning/critical) is
 * used only for the Passed/Pending/Failed outcome chart, where color
 * literally encodes status.
 */

const CHART_INK = '#52514e';
const CHART_GRID = '#e1e0d9';
const CHART_ACCENT = '#2a78d6';

const STATUS_COLORS = {
  Passed: '#0ca30c',
  Pending: '#fab219',
  Failed: '#d03b3b',
  Unknown: '#898781',
};

Chart.defaults.font.family = "'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif";
Chart.defaults.color = CHART_INK;

function baseOptions(horizontal) {
  const valueAxis = { beginAtZero: true, grid: { color: CHART_GRID }, ticks: { precision: 0 } };
  const labelAxis = { grid: { display: false } };
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1c2130',
        padding: 10,
        cornerRadius: 6,
        displayColors: false,
      },
    },
    indexAxis: horizontal ? 'y' : 'x',
    scales: horizontal
      ? { x: valueAxis, y: labelAxis }
      : { x: labelAxis, y: valueAxis },
  };
}

function renderBarChart(canvasId, labels, values, { horizontal = false, colors = null } = {}) {
  const el = document.getElementById(canvasId);
  if (!el || !labels.length) return;

  new Chart(el, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors || CHART_ACCENT,
        borderRadius: 4,
        maxBarThickness: 36,
      }],
    },
    options: baseOptions(horizontal),
  });
}

function renderStatusOutcomeChart(canvasId, labels, values) {
  const colors = labels.map((label) => STATUS_COLORS[label] || STATUS_COLORS.Unknown);
  renderBarChart(canvasId, labels, values, { colors });
}
