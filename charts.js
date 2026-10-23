/**
 * LaundryFlow - Charts & Visualization Engine
 * Renders executive analytics charts for Sistem Informasi Manajemen (SIM)
 * Supports Chart.js if loaded via CDN, with self-contained fallback Canvas rendering
 */

window.LaundryCharts = {
  dailyTrendChart: null,
  statusChart: null,

  initOrUpdateDailyChart: function(canvasId, trendData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const labels = trendData.map(d => d.label);
    const orders = trendData.map(d => d.orders);
    const revenues = trendData.map(d => d.revenue / 1000); // in thousands Rp

    if (window.Chart) {
      if (this.dailyTrendChart) {
        this.dailyTrendChart.destroy();
      }
      this.dailyTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Pendapatan (Ribu Rp)',
              data: revenues,
              borderColor: '#2563eb',
              backgroundColor: 'rgba(37, 99, 235, 0.1)',
              tension: 0.35,
              fill: true,
              yAxisID: 'y1'
            },
            {
              label: 'Pesanan Masuk',
              data: orders,
              borderColor: '#059669',
              backgroundColor: '#10b981',
              tension: 0.2,
              type: 'bar',
              yAxisID: 'y'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: function(context) {
                  if (context.dataset.yAxisID === 'y1') {
                    return `Pendapatan: Rp ${(context.raw * 1000).toLocaleString('id-ID')}`;
                  }
                  return `Pesanan: ${context.raw} order`;
                }
              }
            }
          },
          scales: {
            y: {
              type: 'linear',
              display: true,
              position: 'right',
              title: { display: true, text: 'Jumlah Order' },
              grid: { drawOnChartArea: false }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'left',
              title: { display: true, text: 'Pendapatan (Ribu Rp)' }
            }
          }
        }
      });
    } else {
      // Fallback native canvas chart if CDN blocked
      this.drawNativeBarChart(ctx, canvas, labels, orders, revenues);
    }
  },

  initOrUpdateStatusChart: function(canvasId, statusCounts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const statusLabels = {
      'RECEIVED': 'Diterima',
      'QUEUED': 'Antrean',
      'WASHING': 'Cuci',
      'DRYING': 'Pengering',
      'IRONING': 'Setrika',
      'QUALITY_CHECK': 'QC',
      'READY_FOR_PICKUP': 'Siap Ambil',
      'COMPLETED': 'Selesai',
      'ON_HOLD': 'Ditahan'
    };

    const keys = Object.keys(statusCounts).filter(k => statusCounts[k] > 0);
    const labels = keys.map(k => statusLabels[k] || k);
    const values = keys.map(k => statusCounts[k]);
    const colors = ['#3b82f6', '#6366f1', '#0ea5e9', '#f59e0b', '#8b5cf6', '#ec4899', '#10b981', '#14b8a6', '#f97316'];

    if (window.Chart) {
      if (this.statusChart) {
        this.statusChart.destroy();
      }
      this.statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: colors.slice(0, values.length),
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' }
          },
          cutout: '65%'
        }
      });
    } else {
      this.drawNativeDoughnut(ctx, canvas, labels, values, colors);
    }
  },

  drawNativeBarChart: function(ctx, canvas, labels, orders, revenues) {
    const w = canvas.width = canvas.parentElement.clientWidth || 500;
    const h = canvas.height = 260;
    ctx.clearRect(0, 0, w, h);

    const padding = 40;
    const chartW = w - padding * 2;
    const chartH = h - padding * 2;
    const maxVal = Math.max(...orders, 5);

    // Draw axes
    ctx.strokeStyle = '#e2e8f0';
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, h - padding);
    ctx.lineTo(w - padding, h - padding);
    ctx.stroke();

    const barW = (chartW / labels.length) * 0.45;
    labels.forEach((lbl, i) => {
      const x = padding + (i * (chartW / labels.length)) + 15;
      const barH = (orders[i] / maxVal) * chartH;
      const y = (h - padding) - barH;

      ctx.fillStyle = '#2563eb';
      ctx.fillRect(x, y, barW, barH);

      // Label
      ctx.fillStyle = '#64748b';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(lbl, x + barW / 2, h - padding + 15);
      ctx.fillText(orders[i] + ' ord', x + barW / 2, y - 5);
    });
  },

  drawNativeDoughnut: function(ctx, canvas, labels, values, colors) {
    const w = canvas.width = canvas.parentElement.clientWidth || 280;
    const h = canvas.height = 260;
    ctx.clearRect(0, 0, w, h);

    const total = values.reduce((a, b) => a + b, 0) || 1;
    let startAngle = 0;
    const cx = w / 2;
    const cy = h / 2 - 20;
    const r = Math.min(cx, cy) - 20;

    values.forEach((v, i) => {
      const sliceAngle = (v / total) * 2 * Math.PI;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, startAngle, startAngle + sliceAngle);
      ctx.closePath();
      ctx.fillStyle = colors[i % colors.length];
      ctx.fill();
      startAngle += sliceAngle;
    });

    // Inner hole
    ctx.beginPath();
    ctx.arc(cx, cy, r * 0.6, 0, 2 * Math.PI);
    ctx.fillStyle = '#ffffff';
    ctx.fill();

    // Center text
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${total} Order`, cx, cy + 6);
  }
};
