/**
 * LaundryFlow - Main Application Controller
 * Sistem Informasi Manajemen Laundry Pintar
 */

const AppState = {
  currentUser: null,
  activeView: 'dashboard',
  services: [],
  customers: [],
  orders: [],
  selectedOrder: null,
  activeOrderItems: []
};

// ==========================================
// INITIALIZATION
// ==========================================
document.addEventListener('DOMContentLoaded', async () => {
  await fetchCurrentUser();
  await loadInitialData();
  setupEventListeners();
  switchView('dashboard');
});

async function fetchCurrentUser() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    if (data.success) {
      AppState.currentUser = data.user;
      renderUserHeader();
    }
  } catch (err) {
    console.error('Failed to load user:', err);
  }
}

function renderUserHeader() {
  const user = AppState.currentUser;
  if (!user) return;

  document.getElementById('header-user-name').textContent = user.name;
  
  const roleBadge = document.getElementById('header-user-role');
  roleBadge.textContent = user.role;
  roleBadge.className = `user-role-badge role-${user.role.toLowerCase()}`;

  // Update switcher pills
  document.querySelectorAll('.role-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.role === user.role);
  });

  // Role permissions UI adjustment
  const isOwner = user.role === 'OWNER';
  const isStaff = user.role === 'STAFF';
  const isCustomer = user.role === 'CUSTOMER';

  document.querySelectorAll('.owner-only').forEach(el => {
    el.style.display = isOwner ? '' : 'none';
  });

  document.querySelectorAll('.staff-owner-only').forEach(el => {
    el.style.display = (isOwner || isStaff) ? '' : 'none';
  });

  document.querySelectorAll('.customer-only').forEach(el => {
    el.style.display = isCustomer ? '' : 'none';
  });

  // If customer, switch directly to their portal or tracking
  if (isCustomer && (AppState.activeView === 'dashboard' || AppState.activeView === 'queue')) {
    switchView('customer-portal');
  }
}

async function loadInitialData() {
  await Promise.all([
    fetchServices(),
    fetchCustomers()
  ]);
}

async function fetchServices() {
  try {
    const res = await fetch('/api/services');
    const data = await res.json();
    if (data.success) {
      AppState.services = data.services;
      renderServicesList();
    }
  } catch (err) {
    console.error(err);
  }
}

async function fetchCustomers() {
  try {
    const res = await fetch('/api/customers');
    const data = await res.json();
    if (data.success) {
      AppState.customers = data.customers;
      populateCustomerSelect();
      renderCustomersList();
    }
  } catch (err) {
    console.error(err);
  }
}

// ==========================================
// VIEW SWITCHING
// ==========================================
function switchView(viewName) {
  AppState.activeView = viewName;

  document.querySelectorAll('.view-container').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

  const targetView = document.getElementById(`view-${viewName}`);
  if (targetView) targetView.classList.add('active');

  const activeNavLink = document.querySelector(`.nav-link[data-view="${viewName}"]`);
  if (activeNavLink) activeNavLink.classList.add('active');

  // Trigger data reload depending on view
  if (viewName === 'dashboard') {
    loadDashboardSummary();
  } else if (viewName === 'queue') {
    loadQueueBoard();
  } else if (viewName === 'orders') {
    loadOrdersTable();
  } else if (viewName === 'new-order') {
    initNewOrderForm();
  } else if (viewName === 'customer-portal') {
    loadCustomerPortal();
  } else if (viewName === 'settings') {
    loadSettings();
  } else if (viewName === 'audit-logs') {
    loadAuditLogs();
  }

  // Close mobile sidebar if open
  document.getElementById('app-sidebar').classList.remove('open');
}

// ==========================================
// ROLE SWITCHER (SIM DEMO)
// ==========================================
async function switchRole(targetRole) {
  try {
    const res = await fetch('/api/auth/switch-role', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: targetRole })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      await fetchCurrentUser();
      if (targetRole === 'CUSTOMER') {
        switchView('customer-portal');
      } else {
        switchView('dashboard');
      }
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal beralih peran', 'error');
  }
}

// ==========================================
// DASHBOARD & ANALYTICS
// ==========================================
async function loadDashboardSummary() {
  try {
    const [summaryRes, chartsRes] = await Promise.all([
      fetch('/api/dashboard/summary'),
      fetch('/api/analytics/charts')
    ]);

    const summary = await summaryRes.json();
    const charts = await chartsRes.json();

    if (summary.success) {
      const m = summary.metrics;
      document.getElementById('metric-today-orders').textContent = m.orders_today;
      document.getElementById('metric-active-orders').textContent = m.active_orders;
      document.getElementById('metric-ready-orders').textContent = m.ready_for_pickup;
      document.getElementById('metric-revenue-today').textContent = formatRupiah(m.revenue_today);
      document.getElementById('metric-unpaid').textContent = formatRupiah(m.unpaid_total);
      document.getElementById('metric-waiting-queue').textContent = m.waiting_queue;

      renderRecentOrdersTable(summary.recent_orders);

      if (charts.success) {
        window.LaundryCharts.initOrUpdateDailyChart('chart-daily-trend', charts.daily_trend);
        window.LaundryCharts.initOrUpdateStatusChart('chart-status-donut', m.status_breakdown);
        renderSIMInsights(charts.insights);
        renderPeakPeriods(charts.peak_hours, charts.peak_days);
      }
    }
  } catch (err) {
    console.error('Failed to load dashboard:', err);
  }
}

function renderRecentOrdersTable(orders) {
  const tbody = document.getElementById('recent-orders-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (!orders || orders.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 24px; color: #94a3b8;">Belum ada pesanan terbaru</td></tr>`;
    return;
  }

  orders.forEach(o => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="order-code-badge">${o.order_code}</span></td>
      <td><strong>${o.customer_name}</strong><br><small style="color:#64748b;">${o.customer_phone}</small></td>
      <td>${getStatusBadge(o.status)}</td>
      <td>${getPaymentBadge(o.payment_status)}</td>
      <td><strong>${formatRupiah(o.total_amount)}</strong></td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="openOrderDetailModal(${o.id})">Detail</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function renderSIMInsights(insights) {
  const container = document.getElementById('sim-insights-container');
  if (!container) return;
  container.innerHTML = '';

  insights.forEach(ins => {
    const icon = ins.type === 'WARNING' ? '⚠️' : (ins.type === 'SUCCESS' ? '📈' : '💡');
    const div = document.createElement('div');
    div.className = `insight-card ${ins.type}`;
    div.innerHTML = `
      <div class="insight-icon">${icon}</div>
      <div class="insight-content">
        <h4>${ins.title}</h4>
        <p>${ins.message}</p>
      </div>
    `;
    container.appendChild(div);
  });
}

function renderPeakPeriods(hours, days) {
  const listEl = document.getElementById('peak-hours-list');
  if (!listEl) return;
  listEl.innerHTML = '';

  hours.forEach(h => {
    const div = document.createElement('div');
    div.className = 'receipt-row';
    div.style.padding = '4px 0';
    div.innerHTML = `
      <span>${h.hour}</span>
      <span><strong>${h.orders} order</strong> <span style="font-size:0.75rem; color:${h.intensity.includes('Sangat') ? '#ef4444' : '#2563eb'};">(${h.intensity})</span></span>
    `;
    listEl.appendChild(div);
  });
}

// ==========================================
// KANBAN QUEUE PIPELINE BOARD
// ==========================================
async function loadQueueBoard() {
  try {
    const res = await fetch('/api/orders?status=ACTIVE');
    const data = await res.json();
    if (!data.success) return;

    const orders = data.orders;

    // Reset columns
    const colQueue = document.getElementById('col-cards-queue');
    const colProcess = document.getElementById('col-cards-process');
    const colReady = document.getElementById('col-cards-ready');
    const colDone = document.getElementById('col-cards-done');

    colQueue.innerHTML = '';
    colProcess.innerHTML = '';
    colReady.innerHTML = '';
    colDone.innerHTML = '';

    let cntQueue = 0, cntProcess = 0, cntReady = 0, cntDone = 0;

    orders.forEach(o => {
      const card = createKanbanCard(o);
      if (['RECEIVED', 'QUEUED'].includes(o.status)) {
        colQueue.appendChild(card);
        cntQueue++;
      } else if (['WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK', 'ON_HOLD'].includes(o.status)) {
        colProcess.appendChild(card);
        cntProcess++;
      } else if (o.status === 'READY_FOR_PICKUP') {
        colReady.appendChild(card);
        cntReady++;
      }
    });

    // Also fetch last few completed
    const doneRes = await fetch('/api/orders?status=COMPLETED');
    const doneData = await doneRes.json();
    if (doneData.success) {
      doneData.orders.slice(0, 8).forEach(o => {
        colDone.appendChild(createKanbanCard(o));
        cntDone++;
      });
    }

    document.getElementById('cnt-queue').textContent = cntQueue;
    document.getElementById('cnt-process').textContent = cntProcess;
    document.getElementById('cnt-ready').textContent = cntReady;
    document.getElementById('cnt-done').textContent = cntDone;

  } catch (err) {
    console.error('Queue load failed:', err);
  }
}

function createKanbanCard(order) {
  const card = document.createElement('div');
  card.className = `order-kanban-card ${order.extra_charge > 0 ? 'is-express' : ''}`;
  card.onclick = () => openOrderDetailModal(order.id);

  const nextStatus = getNextLogicalStatus(order.status);

  card.innerHTML = `
    <div class="order-code-row">
      <span class="order-code-badge">${order.order_code}</span>
      ${getStatusBadge(order.status)}
    </div>
    <div class="card-customer-name">${order.customer_name}</div>
    <div class="card-service-desc">
      <span>${order.primary_service_name || 'Layanan'}</span>
      <strong>${order.primary_quantity || 1} ${order.primary_unit || 'KG'}</strong>
    </div>
    <div class="card-time-row">
      <span>⏱ Est: ${order.estimated_ready_at || '-'}</span>
    </div>
    <div class="card-actions-row">
      ${nextStatus ? `
        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); quickAdvanceStatus(${order.id}, '${nextStatus}')">
          Lanjut: ${getStatusLabel(nextStatus)} →
        </button>
      ` : ''}
    </div>
  `;
  return card;
}

function getNextLogicalStatus(current) {
  const pipeline = ['RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK', 'READY_FOR_PICKUP', 'COMPLETED'];
  const idx = pipeline.indexOf(current);
  if (idx !== -1 && idx < pipeline.length - 1) {
    return pipeline[idx + 1];
  }
  return null;
}

async function quickAdvanceStatus(orderId, newStatus) {
  try {
    const res = await fetch(`/api/orders/${orderId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Status diperbarui ke ${getStatusLabel(newStatus)}`, 'success');
      loadQueueBoard();
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal mengubah status', 'error');
  }
}

// ==========================================
// ORDERS MANAGEMENT TABLE
// ==========================================
async function loadOrdersTable() {
  const filter = document.getElementById('filter-order-status').value;
  const search = document.getElementById('search-order-input').value.trim();

  try {
    const res = await fetch(`/api/orders?status=${filter}&q=${encodeURIComponent(search)}`);
    const data = await res.json();
    if (!data.success) return;

    const tbody = document.getElementById('all-orders-tbody');
    tbody.innerHTML = '';

    if (data.orders.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 36px; color:#94a3b8;">Tidak ada pesanan ditemukan</td></tr>`;
      return;
    }

    data.orders.forEach(o => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="order-code-badge">${o.order_code}</span></td>
        <td><strong>${o.customer_name}</strong><br><small style="color:#64748b;">${o.customer_phone}</small></td>
        <td>${o.primary_service_name || '-'}<br><small style="color:#64748b;">${o.primary_quantity || 1} ${o.primary_unit || 'KG'}</small></td>
        <td>${getStatusBadge(o.status)}</td>
        <td>${getPaymentBadge(o.payment_status)}</td>
        <td><strong>${formatRupiah(o.total_amount)}</strong></td>
        <td><small style="color:#64748b;">${o.estimated_ready_at || '-'}</small></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openOrderDetailModal(${o.id})">Buka</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Failed to load orders:', err);
  }
}

// ==========================================
// NEW ORDER FORM (KASIR POS)
// ==========================================
function initNewOrderForm() {
  AppState.activeOrderItems = [];
  document.getElementById('new-order-notes').value = '';
  document.getElementById('new-order-extra').value = 0;
  document.getElementById('new-order-discount').value = 0;
  document.getElementById('toggle-new-cust-fields').checked = false;
  document.getElementById('new-customer-fields').style.display = 'none';
  document.getElementById('new-order-initial-pay').value = 0;

  // Add one default service item
  if (AppState.services.length > 0) {
    addOrderItemRow(AppState.services[0].id, 3.0);
  }
  recalculateOrderTotals();
}

function addOrderItemRow(serviceId = null, qty = 1.0) {
  const container = document.getElementById('order-items-container');
  if (!container) return;

  const itemIndex = AppState.activeOrderItems.length;
  const srv = serviceId ? AppState.services.find(s => s.id === parseInt(serviceId)) : AppState.services[0];

  AppState.activeOrderItems.push({
    service_id: srv.id,
    quantity: qty,
    notes: ''
  });

  renderOrderItemsRows();
  recalculateOrderTotals();
}

function renderOrderItemsRows() {
  const container = document.getElementById('order-items-container');
  container.innerHTML = '';

  AppState.activeOrderItems.forEach((itm, idx) => {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex; gap:12px; align-items:center; margin-bottom:10px; background:#f8fafc; padding:10px; border-radius:8px; border:1px solid #e2e8f0;';

    const srvOptions = AppState.services.map(s => `
      <option value="${s.id}" ${s.id === itm.service_id ? 'selected' : ''}>
        ${s.name} (Rp ${s.price.toLocaleString('id-ID')} / ${s.pricing_unit})
      </option>
    `).join('');

    row.innerHTML = `
      <div style="flex:2;">
        <select class="form-control" onchange="updateOrderItemService(${idx}, this.value)">
          ${srvOptions}
        </select>
      </div>
      <div style="flex:1;">
        <input type="number" step="0.1" min="0.1" class="form-control" value="${itm.quantity}" placeholder="Jumlah / Berat" onchange="updateOrderItemQty(${idx}, this.value)" onkeyup="updateOrderItemQty(${idx}, this.value)">
      </div>
      <div style="flex:1;">
        <input type="text" class="form-control" placeholder="Catatan item (opsional)" value="${itm.notes || ''}" onchange="updateOrderItemNote(${idx}, this.value)">
      </div>
      <div>
        <button type="button" class="btn btn-danger btn-sm" onclick="removeOrderItemRow(${idx})">✕</button>
      </div>
    `;
    container.appendChild(row);
  });
}

function updateOrderItemService(idx, srvId) {
  AppState.activeOrderItems[idx].service_id = parseInt(srvId);
  recalculateOrderTotals();
}

function updateOrderItemQty(idx, qty) {
  AppState.activeOrderItems[idx].quantity = parseFloat(qty) || 0;
  recalculateOrderTotals();
}

function updateOrderItemNote(idx, note) {
  AppState.activeOrderItems[idx].notes = note;
}

function removeOrderItemRow(idx) {
  if (AppState.activeOrderItems.length <= 1) {
    showToast('Minimal harus ada 1 item layanan', 'warning');
    return;
  }
  AppState.activeOrderItems.splice(idx, 1);
  renderOrderItemsRows();
  recalculateOrderTotals();
}

function recalculateOrderTotals() {
  let subtotal = 0;
  let maxDuration = 0;
  let hasExpress = false;

  AppState.activeOrderItems.forEach(itm => {
    const srv = AppState.services.find(s => s.id === itm.service_id);
    if (srv) {
      subtotal += srv.price * itm.quantity;
      if (srv.estimated_duration_minutes > maxDuration) {
        maxDuration = srv.estimated_duration_minutes;
      }
      if (srv.is_express) hasExpress = true;
    }
  });

  const extra = parseFloat(document.getElementById('new-order-extra').value) || 0;
  const discount = parseFloat(document.getElementById('new-order-discount').value) || 0;
  const total = Math.max(0, subtotal + extra - discount);

  document.getElementById('summary-subtotal').textContent = formatRupiah(subtotal);
  document.getElementById('summary-total').textContent = formatRupiah(total);

  // Live estimate calculation preview
  const now = new Date();
  const estDate = new Date(now.getTime() + (maxDuration * 60000));
  const estFormatted = estDate.toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric', month: 'short' }) + ' ' +
                       estDate.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });

  document.getElementById('preview-est-ready').textContent = estFormatted;
  document.getElementById('preview-est-label').textContent = hasExpress ? '⚡ Mode Cepat (Express Priority)' : '✨ Berdasarkan antrean & jam buka outlet';
}

async function submitCreateOrder() {
  const isNewCust = document.getElementById('toggle-new-cust-fields').checked;
  const customerId = isNewCust ? null : parseInt(document.getElementById('select-customer-order').value);

  const newCust = isNewCust ? {
    name: document.getElementById('new-cust-name').value.trim(),
    phone: document.getElementById('new-cust-phone').value.trim(),
    address: document.getElementById('new-cust-address').value.trim()
  } : null;

  if (isNewCust && (!newCust.name || !newCust.phone)) {
    showToast('Nama dan nomor telepon pelanggan baru wajib diisi', 'error');
    return;
  }

  const payload = {
    customer_id: customerId,
    new_customer: newCust,
    items: AppState.activeOrderItems,
    extra_charge: parseFloat(document.getElementById('new-order-extra').value) || 0,
    discount_amount: parseFloat(document.getElementById('new-order-discount').value) || 0,
    customer_notes: document.getElementById('new-order-notes').value.trim(),
    initial_payment: {
      amount: parseFloat(document.getElementById('new-order-initial-pay').value) || 0,
      method: document.getElementById('new-order-pay-method').value
    }
  };

  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      await fetchCustomers();
      switchView('queue');
      openOrderDetailModal(data.order_id);
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Terjadi kesalahan saat membuat pesanan', 'error');
  }
}

// ==========================================
// ORDER DETAIL & MODAL ACTIONS
// ==========================================
async function openOrderDetailModal(orderId) {
  try {
    const res = await fetch(`/api/orders/${orderId}`);
    const data = await res.json();
    if (!data.success) {
      showToast(data.error, 'error');
      return;
    }

    AppState.selectedOrder = data;
    const o = data.order;

    document.getElementById('modal-order-code').textContent = o.order_code;
    document.getElementById('modal-order-cust').textContent = `${o.customer_name} (${o.customer_phone})`;
    document.getElementById('modal-order-status-badge').innerHTML = getStatusBadge(o.status);
    document.getElementById('modal-order-pay-badge').innerHTML = getPaymentBadge(o.payment_status);
    document.getElementById('modal-order-received').textContent = o.received_at;
    document.getElementById('modal-order-estimated').textContent = o.estimated_ready_at;
    document.getElementById('modal-order-total').textContent = formatRupiah(o.total_amount);
    document.getElementById('modal-order-paid').textContent = formatRupiah(o.paid_amount);

    const sisa = o.total_amount - o.paid_amount;
    document.getElementById('modal-order-remaining').textContent = formatRupiah(Math.max(0, sisa));

    // Render items list
    const itemsTbody = document.getElementById('modal-items-tbody');
    itemsTbody.innerHTML = '';
    data.items.forEach(itm => {
      itemsTbody.innerHTML += `
        <tr>
          <td><strong>${itm.service_name_snapshot}</strong></td>
          <td>${itm.quantity} ${itm.pricing_unit_snapshot}</td>
          <td>${formatRupiah(itm.unit_price)}</td>
          <td><strong>${formatRupiah(itm.line_total)}</strong></td>
        </tr>
      `;
    });

    // Render timeline history
    const timelineEl = document.getElementById('modal-timeline-history');
    timelineEl.innerHTML = '';
    data.history.forEach(h => {
      timelineEl.innerHTML += `
        <div style="padding: 6px 0; border-left: 2px solid #2563eb; padding-left: 12px; margin-bottom: 8px;">
          <div style="font-weight:700; font-size:0.84rem;">${getStatusBadge(h.to_status)} <span style="font-size:0.75rem; color:#64748b; margin-left:6px;">${h.changed_at}</span></div>
          <div style="font-size:0.8rem; color:#475569;">${h.note || '-'} (${h.changed_by_name || 'Petugas'})</div>
        </div>
      `;
    });

    // Pre-fill payment input with remaining amount
    document.getElementById('modal-pay-amount').value = Math.max(0, sisa);

    // Show modal
    document.getElementById('order-detail-modal').classList.add('active');

  } catch (err) {
    showToast('Gagal memuat detail pesanan', 'error');
  }
}

function closeOrderDetailModal() {
  document.getElementById('order-detail-modal').classList.remove('active');
}

async function submitModalStatusChange() {
  if (!AppState.selectedOrder) return;
  const newStatus = document.getElementById('modal-change-status-select').value;
  const note = document.getElementById('modal-change-status-note').value.trim();

  try {
    const res = await fetch(`/api/orders/${AppState.selectedOrder.order.id}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus, note: note })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      await openOrderDetailModal(AppState.selectedOrder.order.id);
      loadQueueBoard();
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal mengubah status', 'error');
  }
}

async function submitModalPayment() {
  if (!AppState.selectedOrder) return;
  const amount = parseFloat(document.getElementById('modal-pay-amount').value) || 0;
  const method = document.getElementById('modal-pay-method').value;

  if (amount <= 0) {
    showToast('Nominal pembayaran harus lebih dari 0', 'warning');
    return;
  }

  try {
    const res = await fetch(`/api/orders/${AppState.selectedOrder.order.id}/payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: amount, method: method })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      await openOrderDetailModal(AppState.selectedOrder.order.id);
      loadDashboardSummary();
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal mencatat pembayaran', 'error');
  }
}

// ==========================================
// THERMAL RECEIPT & PRINTING
// ==========================================
function printOrderReceipt() {
  if (!AppState.selectedOrder) return;
  const data = AppState.selectedOrder;
  const o = data.order;
  const outlet = data.outlet || {};

  const printArea = document.getElementById('print-area');
  printArea.innerHTML = `
    <div class="receipt-paper">
      <div class="receipt-header">
        <div class="receipt-logo">${outlet.name || 'LaundryFlow Clean'}</div>
        <div style="font-size:0.75rem;">${outlet.address || 'Jl. Dipati Ukur No. 45, Bandung'}</div>
        <div style="font-size:0.75rem;">Telp: ${outlet.phone || '0812-3456-7890'}</div>
      </div>
      <div class="receipt-divider"></div>
      <div class="receipt-row">
        <span>No. Order:</span>
        <strong>${o.order_code}</strong>
      </div>
      <div class="receipt-row">
        <span>Pelanggan:</span>
        <span>${o.customer_name}</span>
      </div>
      <div class="receipt-row">
        <span>Waktu Masuk:</span>
        <span>${o.received_at}</span>
      </div>
      <div class="receipt-row">
        <span>Est. Selesai:</span>
        <strong>${o.estimated_ready_at}</strong>
      </div>
      <div class="receipt-divider"></div>
      ${data.items.map(itm => `
        <div class="receipt-row">
          <span>${itm.service_name_snapshot} (${itm.quantity} ${itm.pricing_unit_snapshot})</span>
          <span>${formatRupiah(itm.line_total)}</span>
        </div>
      `).join('')}
      <div class="receipt-divider"></div>
      <div class="receipt-row">
        <span>Subtotal:</span>
        <span>${formatRupiah(o.subtotal)}</span>
      </div>
      ${o.extra_charge > 0 ? `
        <div class="receipt-row">
          <span>Biaya Tambahan:</span>
          <span>${formatRupiah(o.extra_charge)}</span>
        </div>
      ` : ''}
      <div class="receipt-row" style="font-size:1rem; font-weight:bold;">
        <span>TOTAL:</span>
        <span>${formatRupiah(o.total_amount)}</span>
      </div>
      <div class="receipt-row">
        <span>Dibayar:</span>
        <span>${formatRupiah(o.paid_amount)}</span>
      </div>
      <div class="receipt-row">
        <span>Status Bayar:</span>
        <strong>${o.payment_status}</strong>
      </div>
      <div class="receipt-divider"></div>
      <div style="text-align:center; font-size:0.75rem; margin-top:10px;">
        *** TERIMA KASIH ***<br>
        Lacak status cucian di:<br>
        <strong>laundryflow.id/track/${o.order_code}</strong>
      </div>
    </div>
  `;

  window.print();
}

// ==========================================
// PUBLIC TRACKING
// ==========================================
async function performPublicTrack() {
  const code = document.getElementById('public-track-code').value.trim();
  if (!code) {
    showToast('Masukkan kode order atau nomor handphone', 'warning');
    return;
  }

  try {
    const res = await fetch(`/api/track/${encodeURIComponent(code)}`);
    const data = await res.json();
    if (!data.success) {
      showToast(data.error, 'error');
      document.getElementById('track-result-box').style.display = 'none';
      return;
    }

    const o = data.order;
    document.getElementById('track-result-box').style.display = 'block';
    document.getElementById('track-res-code').textContent = o.order_code;
    document.getElementById('track-res-cust').textContent = o.customer_name;
    document.getElementById('track-res-status-badge').innerHTML = getStatusBadge(o.status);
    document.getElementById('track-res-est').textContent = o.estimated_ready_at;
    document.getElementById('track-res-label').textContent = o.confidence_label || 'Estimasi Cerdas';

    // Stepper visual
    const steps = ['RECEIVED', 'WASHING', 'DRYING', 'IRONING', 'READY_FOR_PICKUP', 'COMPLETED'];
    const currentIdx = steps.indexOf(o.status);

    document.querySelectorAll('.step-node').forEach((node, idx) => {
      node.classList.remove('completed', 'current');
      if (currentIdx !== -1) {
        if (idx < currentIdx) node.classList.add('completed');
        if (idx === currentIdx) node.classList.add('current');
      }
    });

    document.getElementById('stepper-progress-fill').style.width = `${data.progress_pct}%`;

    // Items
    const itemsContainer = document.getElementById('track-res-items');
    itemsContainer.innerHTML = data.items.map(i => `
      <div class="receipt-row" style="padding: 6px 0; border-bottom:1px solid #f1f5f9;">
        <span>${i.service_name_snapshot} (${i.quantity} ${i.pricing_unit_snapshot})</span>
        <strong>${formatRupiah(i.line_total)}</strong>
      </div>
    `).join('');

    document.getElementById('track-res-total').textContent = formatRupiah(o.total_amount);
    document.getElementById('track-res-pay-status').innerHTML = getPaymentBadge(o.payment_status);

  } catch (err) {
    showToast('Gagal melacak pesanan', 'error');
  }
}

// ==========================================
// CUSTOMER PORTAL
// ==========================================
async function loadCustomerPortal() {
  try {
    const res = await fetch('/api/orders?status=ALL');
    const data = await res.json();
    if (!data.success) return;

    const tbody = document.getElementById('cust-portal-orders-tbody');
    tbody.innerHTML = '';

    if (data.orders.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 36px; color:#94a3b8;">Belum ada riwayat cucian</td></tr>`;
      return;
    }

    data.orders.forEach(o => {
      tbody.innerHTML += `
        <tr>
          <td><span class="order-code-badge">${o.order_code}</span></td>
          <td>${o.primary_service_name || '-'} (${o.primary_quantity || 1} ${o.primary_unit || 'KG'})</td>
          <td>${getStatusBadge(o.status)}</td>
          <td>${getPaymentBadge(o.payment_status)}</td>
          <td>${o.estimated_ready_at || '-'}</td>
          <td><button class="btn btn-secondary btn-sm" onclick="openOrderDetailModal(${o.id})">Lihat Rincian</button></td>
        </tr>
      `;
    });
  } catch (err) {
    console.error(err);
  }
}

// ==========================================
// MASTER DATA & SETTINGS
// ==========================================
function populateCustomerSelect() {
  const select = document.getElementById('select-customer-order');
  if (!select) return;
  select.innerHTML = AppState.customers.map(c => `
    <option value="${c.id}">${c.name} - ${c.phone_normalized}</option>
  `).join('');
}

function renderServicesList() {
  const tbody = document.getElementById('services-table-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';
  AppState.services.forEach(s => {
    tbody.innerHTML += `
      <tr>
        <td><strong>${s.name}</strong><br><small style="color:#64748b;">${s.description || '-'}</small></td>
        <td><span class="col-count-pill">${s.pricing_unit}</span></td>
        <td><strong>${formatRupiah(s.price)}</strong></td>
        <td>${Math.round(s.estimated_duration_minutes / 60)} Jam (${s.estimated_duration_minutes} mnt)</td>
        <td>${s.is_express ? '⚡ Express' : 'Standar'}</td>
        <td><span class="badge-status ${s.is_active ? 'COMPLETED' : 'CANCELLED'}">${s.is_active ? 'Aktif' : 'Nonaktif'}</span></td>
      </tr>
    `;
  });
}

function renderCustomersList() {
  const tbody = document.getElementById('customers-table-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';
  AppState.customers.forEach(c => {
    tbody.innerHTML += `
      <tr>
        <td><strong>${c.name}</strong></td>
        <td>${c.phone_normalized}</td>
        <td>${c.address || '-'}</td>
        <td><span class="col-count-pill">${c.order_count || 0} Order</span></td>
        <td><strong>${formatRupiah(c.total_spent || 0)}</strong></td>
        <td><small style="color:#64748b;">${c.last_order_date || '-'}</small></td>
      </tr>
    `;
  });
}

async function loadSettings() {
  try {
    const res = await fetch('/api/settings');
    const data = await res.json();
    if (data.success) {
      const o = data.outlet;
      document.getElementById('setting-outlet-name').value = o.name || '';
      document.getElementById('setting-outlet-address').value = o.address || '';
      document.getElementById('setting-outlet-phone').value = o.phone || '';
      document.getElementById('setting-outlet-opens').value = o.opens_at || '08:00';
      document.getElementById('setting-outlet-closes').value = o.closes_at || '21:00';
      document.getElementById('setting-outlet-capacity').value = o.max_daily_capacity_kg || 250;
    }
  } catch (err) {
    console.error(err);
  }
}

async function saveSettings() {
  const payload = {
    name: document.getElementById('setting-outlet-name').value.trim(),
    address: document.getElementById('setting-outlet-address').value.trim(),
    phone: document.getElementById('setting-outlet-phone').value.trim(),
    opens_at: document.getElementById('setting-outlet-opens').value.trim(),
    closes_at: document.getElementById('setting-outlet-closes').value.trim(),
    max_daily_capacity_kg: parseFloat(document.getElementById('setting-outlet-capacity').value) || 250
  };

  try {
    const res = await fetch('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal menyimpan pengaturan', 'error');
  }
}

async function resetDemoData() {
  if (!confirm('Apakah Anda yakin ingin mereset seluruh database dan mengembalikan data demo awal?')) return;
  try {
    const res = await fetch('/api/settings/reset-demo', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      await loadInitialData();
      switchView('dashboard');
    } else {
      showToast(data.error, 'error');
    }
  } catch (err) {
    showToast('Gagal mereset demo', 'error');
  }
}

async function loadAuditLogs() {
  try {
    const res = await fetch('/api/audit-logs');
    const data = await res.json();
    if (!data.success) return;

    const tbody = document.getElementById('audit-logs-tbody');
    tbody.innerHTML = '';
    data.logs.forEach(l => {
      tbody.innerHTML += `
        <tr>
          <td><small style="color:#64748b;">${l.created_at}</small></td>
          <td><strong>${l.actor_name}</strong></td>
          <td><span class="col-count-pill">${l.action}</span></td>
          <td>${l.entity_type} #${l.entity_id || '-'}</td>
          <td><small>${l.details || '-'}</small></td>
        </tr>
      `;
    });
  } catch (err) {
    console.error(err);
  }
}

// ==========================================
// EVENT LISTENERS & HELPERS
// ==========================================
function setupEventListeners() {
  // Sidebar navigation
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const view = link.dataset.view;
      if (view) switchView(view);
    });
  });

  // Mobile sidebar toggle
  const toggleBtn = document.getElementById('toggle-sidebar-btn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.getElementById('app-sidebar').classList.toggle('open');
    });
  }

  // Toggle new customer form in order creation
  const custToggle = document.getElementById('toggle-new-cust-fields');
  if (custToggle) {
    custToggle.addEventListener('change', (e) => {
      document.getElementById('existing-customer-fields').style.display = e.target.checked ? 'none' : 'block';
      document.getElementById('new-customer-fields').style.display = e.target.checked ? 'block' : 'none';
    });
  }
}

function getStatusBadge(status) {
  const map = {
    'RECEIVED': 'Diterima',
    'QUEUED': 'Antrean',
    'WASHING': 'Pencucian',
    'DRYING': 'Pengeringan',
    'IRONING': 'Setrika',
    'QUALITY_CHECK': 'Cek Kualitas',
    'READY_FOR_PICKUP': 'Siap Ambil',
    'COMPLETED': 'Selesai',
    'ON_HOLD': 'Ditahan',
    'CANCELLED': 'Batal'
  };
  return `<span class="badge-status ${status}">${map[status] || status}</span>`;
}

function getStatusLabel(status) {
  const map = {
    'RECEIVED': 'Diterima',
    'QUEUED': 'Antrean',
    'WASHING': 'Pencucian',
    'DRYING': 'Pengeringan',
    'IRONING': 'Setrika',
    'QUALITY_CHECK': 'Cek Kualitas',
    'READY_FOR_PICKUP': 'Siap Ambil',
    'COMPLETED': 'Selesai'
  };
  return map[status] || status;
}

function getPaymentBadge(status) {
  const map = {
    'PAID': 'Lunas',
    'PARTIALLY_PAID': 'Sebagian',
    'UNPAID': 'Belum Bayar'
  };
  return `<span class="badge-pay ${status}">${map[status] || status}</span>`;
}

function formatRupiah(val) {
  return 'Rp ' + Math.round(val || 0).toLocaleString('id-ID');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✅' : (type === 'error' ? '❌' : (type === 'warning' ? '⚠️' : 'ℹ️'));
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
