<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { loadAdminArtistOptions } from "@/libs/adminArtistOptions.js";
import { resolveSelectedArtists } from "@/libs/artistOptions.js";
import { useRoute, useRouter } from "vue-router";
import axios from "@/axios";
import html2pdf from 'html2pdf.js'
import { exportWorkbook } from '@/libs/xlsx-export.js'
import { indexToCountry } from "@/libs/utils.js";
import EventSummaryCards from "@/views/Campaign/components/EventSummaryCard.vue";
import SalesTrendLineChart from "@/views/Campaign/components/OfflineEvent_SalesTrendLineChart.vue"
import TicketZonePerformanceChart from "@/views/Campaign/components/OfflineEvent_ZonePerformanceChart.vue"
import GenderDistributionChart from "@/views/Campaign/components/OfflineEvent_GenderCard.vue";
import AgeDistributionChart from "@/views/Campaign/components/OfflineEvent_AgeCard.vue";
import OfflineEventReport from '@/views/Campaign/components/OfflineEvent_Report.vue'
import EventShareLinkCard from '@/views/Admin/components/EventShareLinkCard.vue'
import { computeEventSummaryMetrics } from '@/libs/eventMetrics.js'

const route = useRoute();
const router = useRouter();
const eventId = route.params.id;

const loading = ref(false);
const detailLoading = ref(false);
const editMode = ref(false);

const artistOptions = ref([]);
const isArtistDropdownOpen = ref(false);

// Excel/ PDF Report
const reportRef = ref(null)
const exportingPDF = ref(false)
const exportingExcel = ref(false)

const eventData = ref({
  event_name: "",
  type: "",
  artist_ids: [],
  event_date: "",
  session: "",
  held_country: "",
  held_city: "",
  venue: "",
  organizer: "",
  ticket_release: "",
  ticket_close: "",
  created_at: "",
  updated_at: ""
});

const originalEventData = ref({});

// Read-only view uses the event's own artists; the full list (loaded in edit mode)
// covers artists newly picked in the form.
const selectedArtistsList = computed(() =>
  resolveSelectedArtists(eventData.value.artist_ids, artistOptions.value, eventData.value.artists)
);

const toggleArtistSelection = (artistId) => {
  const selectedIds = Array.isArray(eventData.value.artist_ids)
    ? [...eventData.value.artist_ids]
    : [];

  const id = String(artistId);
  const index = selectedIds.findIndex(
    selectedId => String(selectedId) === id
  );

  if (index >= 0) {
    selectedIds.splice(index, 1);
  } else {
    selectedIds.push(id);
  }

  eventData.value.artist_ids = selectedIds;
};

// Snapshot 相關狀態
const snapshots = ref([]);
const activeTabId = ref(null); // 當前選中的 snapshot id
const editSnapshotMode = ref(false); // 該 snapshot 是否處於編輯模式
const editingSnapshotData = ref(null); // 正在編輯中的 snapshot 暫存資料

const showSnapshotDialog = ref(false);
const snapshotLoading = ref(false);
const eventTypeOptions = ["Concert", "Fan Meeting", "Festival", "Showcase", "Award Show", "Other"];
const currencyOptions = [
  { label: "USD ($)", value: "USD" },
  { label: "台幣 (NT$)", value: "TWD" },
  { label: "人民幣 (¥)", value: "CNY" },
  { label: "港幣 (HK$)", value: "HKD" },
  { label: "新幣 (S$)", value: "SGD" }
];

const typeOptions = ["ticket", "benefit"];
const genderDistributionFields = [
  { key: "male", label: "Male" },
  { key: "female", label: "Female" },
  { key: "unknown", label: "Unknown" }
];
const ageDistributionFields = [
  { key: "age_10s", label: "10s" },
  { key: "age_20s", label: "20s" },
  { key: "age_30s", label: "30s" },
  { key: "age_40s", label: "40s" },
  { key: "age_50_plus", label: "50+" }
];
const emptyGenderDistribution = () => ({ male: 0, female: 0, unknown: 0 });
const emptyAgeDistribution = () => ({
  age_10s: 0,
  age_20s: 0,
  age_30s: 0,
  age_40s: 0,
  age_50_plus: 0
});

// 固定選項 + Custom date 下拉
const fixedSnapshotOptions = [
  "T+1 Hour",
  "T+24 Hour",
  "Closed"
];

const snapshotNameOptions = [
  ...fixedSnapshotOptions,
  "Custom date"
];

// 自定義 T+N 天數 (2 ~ 30)
const customDays = ref(2);

const emptySnapshot = () => ({
  snapshot_name: "T+1 Hour",
  observed_at: "",
  ticket_items: [
    {
      name: "",
      type: "ticket",
      currency: "USD",
      price: 0,
      total_quantity: 0,
      sold: 0,
      refund: 0
    }
  ],
  gender_distribution: emptyGenderDistribution(),
  age_distribution: emptyAgeDistribution()
});

const newSnapshot = ref(emptySnapshot());

const resetSnapshotForm = () => {
  newSnapshot.value = emptySnapshot();
  customDays.value = 2;
};

const snackbar = ref({
  show: false,
  message: "",
  color: "info"
});

const showMessage = (message, color = "info") => {
  snackbar.value = { show: true, message, color };
};

const formatDate = (date) => {
  if (!date) return "-";
  const d = new Date(date);
  if (Number.isNaN(d.getTime())) return "-";
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const formatDateTime = (date) => {
  if (!date) return "-";
  const d = new Date(date);
  if (Number.isNaN(d.getTime())) return "-";
  return `${formatDate(d)} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
};

// 數字千分位格式化
const formatNumber = (val) => {
  if (val === null || val === undefined || isNaN(val)) return "0";
  return Number(val).toLocaleString("en-US");
};

const formatBirthDate = (date) => {
  if (!date) return "-";
  return formatDate(date);
};

const distributionHasValues = (distribution) => {
  if (!distribution || typeof distribution !== "object") return false;
  return Object.values(distribution).some(value => Number(value) > 0);
};

const attachClosedSnapshotDemographics = (payload, snapshotData) => {
  if (payload.snapshot_type !== "closed") return;

  const hasGenderValues = distributionHasValues(snapshotData.gender_distribution);
  const hasAgeValues = distributionHasValues(snapshotData.age_distribution);
  if (!hasGenderValues && !hasAgeValues) return;

  payload.gender_distribution = {
    male: Number(snapshotData.gender_distribution?.male) || 0,
    female: Number(snapshotData.gender_distribution?.female) || 0,
    unknown: Number(snapshotData.gender_distribution?.unknown) || 0
  };
  payload.age_distribution = {
    age_10s: Number(snapshotData.age_distribution?.age_10s) || 0,
    age_20s: Number(snapshotData.age_distribution?.age_20s) || 0,
    age_30s: Number(snapshotData.age_distribution?.age_30s) || 0,
    age_40s: Number(snapshotData.age_distribution?.age_40s) || 0,
    age_50_plus: Number(snapshotData.age_distribution?.age_50_plus) || 0
  };
};

const getArtistLabel = (artist) => {
  if (!artist || typeof artist !== "object") return "";
  const englishName = artist.artist_en_name || artist.artist_id || "";
  const koreanName = artist.artist_kr_name || "";
  return koreanName ? `${englishName} (${koreanName})` : englishName;
};

const selectArtist = (artistId) => {
  eventData.value.artist_id = artistId;
  isArtistDropdownOpen.value = false;
};

// 藝人下拉選單搜尋關鍵字
const artistSearchQuery = ref("");

// 根據搜尋關鍵字動態過濾藝人選項（支援英文名、韓文名）
const filteredArtistOptions = computed(() => {
  if (!artistSearchQuery.value.trim()) {
    return artistOptions.value;
  }
  const query = artistSearchQuery.value.toLowerCase().trim();
  return artistOptions.value.filter((artist) => {
    const enName = (artist.artist_en_name || artist.english_name || "").toLowerCase();
    const krName = (artist.artist_kr_name || artist.korean_name || "").toLowerCase();
    const label = getArtistLabel(artist).toLowerCase();
    return enName.includes(query) || krName.includes(query) || label.includes(query);
  });
});

const toDateInput = (value) => {
  if (!value) return "";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "";
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const toDateTimeInput = (value) => {
  if (!value) return "";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "";
  return `${toDateInput(d)}T${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
};

const normalizeEvent = (event) => ({
  ...event,
  artist_ids: Array.isArray(event.artist_ids)
    ? event.artist_ids.map(artist =>
        String(typeof artist === "object" ? artist.id : artist)
      )
    : Array.isArray(event.artists)
      ? event.artists.map(artist => String(artist.id))
      : event.artist_id
        ? [String(event.artist_id)]
        : [],
  event_date: toDateInput(event.event_date),
  ticket_release: toDateTimeInput(event.ticket_release),
  ticket_close: toDateTimeInput(event.ticket_close)
});

const fetchArtistOptions = async () => {
  try {
    artistOptions.value = await loadAdminArtistOptions();
  } catch (err) {
    console.error("Error fetching artist list:", err);
    showMessage("Failed to load artists. Leave edit mode and try again.", "error");
  }
};

const fetchEventDetail = async () => {
  detailLoading.value = true;
  try {
    const res = await axios.get(`/admin/v1/events/${eventId}`);
    const normalized = normalizeEvent(res.data?.data || {});
    eventData.value = normalized;
    originalEventData.value = JSON.parse(JSON.stringify(normalized));
  } catch (err) {
    console.error("Failed to fetch event details:", err);
    showMessage("Failed to fetch event details.", "error");
  } finally {
    detailLoading.value = false;
  }
};

const updateEvent = async () => {
  loading.value = true;
  try {
    await axios.patch(`/admin/v1/events/${eventId}`, {
      event_name: eventData.value.event_name,
      type: eventData.value.type,
      artist_ids: eventData.value.artist_ids.map(String),
      event_date: eventData.value.event_date,
      session: eventData.value.session,
      held_country: eventData.value.held_country,
      held_city: eventData.value.held_city,
      venue: eventData.value.venue,
      organizer: eventData.value.organizer,
      ticket_release: eventData.value.ticket_release,
      ticket_close: eventData.value.ticket_close
    });
    showMessage("Event updated successfully.", "success");
    editMode.value = false;
    await fetchEventDetail();
  } catch (err) {
    console.error("Update event failed:", err);
    showMessage(err.response?.data?.error || "Failed to update event.", "error");
  } finally {
    loading.value = false;
  }
};

const cancelEdit = () => {
  eventData.value = JSON.parse(JSON.stringify(originalEventData.value));
  editMode.value = false;
  isArtistDropdownOpen.value = false;
};

// Tickets & Benefits 動態增減欄位 (新增 Modal 用)
const addTicketRow = () => {
  newSnapshot.value.ticket_items.push({
    name: "",
    type: "ticket",
    currency: "USD",
    price: 0,
    total_quantity: 0,
    sold: 0,
    refund: 0
  });
};

const removeTicketRow = (index) => {
  newSnapshot.value.ticket_items.splice(index, 1);
};

// Tickets & Benefits 動態增減欄位 (編輯 Snapshot 用)
const addEditingTicketRow = () => {
  if (!editingSnapshotData.value) return;
  editingSnapshotData.value.ticket_items.push({
    name: "",
    type: "ticket",
    currency: "USD",
    price: 0,
    total_quantity: 0,
    sold: 0,
    refund: 0
  });
};

const removeEditingTicketRow = (index) => {
  if (!editingSnapshotData.value) return;
  editingSnapshotData.value.ticket_items.splice(index, 1);
};

const fetchSnapshots = async () => {
  try {
    const res = await axios.get(`/admin/v1/events/${eventId}/snapshots`);
    snapshots.value = res.data?.data || [];
    if (snapshots.value.length > 0 && (!activeTabId.value || !snapshots.value.some(s => s.id === activeTabId.value))) {
      activeTabId.value = snapshots.value[0].id;
    }
  } catch (err) {
    console.error("Fetch snapshots failed:", err);
  }
};

const switchTab = (snapshotId) => {
  activeTabId.value = snapshotId;
  editSnapshotMode.value = false;
  editingSnapshotData.value = null;
};

const currentActiveSnapshot = computed(() => {
  return snapshots.value.find(s => s.id === activeTabId.value) || null;
});

const chartSnapshots = computed(() => {
  if (!Array.isArray(snapshots.value)) return [];

  return snapshots.value
    .filter(snapshot => snapshot && !Number.isNaN(new Date(snapshot.observed_at).getTime()))
    .map(snapshot => ({
      ...snapshot,
      ticket_items: Array.isArray(snapshot.ticket_items) ? snapshot.ticket_items : []
    }));
});

const activeChartTicketItems = computed(() => {
  const items = currentActiveSnapshot.value?.ticket_items;
  return Array.isArray(items) ? items : [];
});

const hasSalesTrendChartData = computed(() => chartSnapshots.value.length > 0);
const hasZonePerformanceChartData = computed(() => activeChartTicketItems.value.length > 0);

const startEditSnapshot = () => {
  if (!currentActiveSnapshot.value) return;
  editSnapshotMode.value = true;
  editingSnapshotData.value = JSON.parse(JSON.stringify(currentActiveSnapshot.value));
  if (editingSnapshotData.value.observed_at) {
    editingSnapshotData.value.observed_at = toDateTimeInput(editingSnapshotData.value.observed_at);
  }
  editingSnapshotData.value.gender_distribution = {
    ...emptyGenderDistribution(),
    ...(editingSnapshotData.value.gender_distribution || {})
  };
  editingSnapshotData.value.age_distribution = {
    ...emptyAgeDistribution(),
    ...(editingSnapshotData.value.age_distribution || {})
  };
};

const cancelEditSnapshot = () => {
  editSnapshotMode.value = false;
  editingSnapshotData.value = null;
};

const saveSnapshotEdit = async () => {
  if (!editingSnapshotData.value) return;
  snapshotLoading.value = true;
  try {
    const snapshotId = editingSnapshotData.value.id;
    const payload = {
      event_id: eventId,
      snapshot_name: editingSnapshotData.value.snapshot_name,
      snapshot_type: editingSnapshotData.value.snapshot_name === "Closed" ? "closed" : "custom",
      observed_at: editingSnapshotData.value.observed_at,
      ticket_items: editingSnapshotData.value.ticket_items.map(item => ({
        name: item.name,
        type: item.type,
        currency: item.currency,
        price: Number(item.price) || 0,
        total_quantity: Number(item.total_quantity) || 0,
        sold: Number(item.sold) || 0,
        refund: Number(item.refund) || 0
      }))
    };
    attachClosedSnapshotDemographics(payload, editingSnapshotData.value);

    await axios.delete(`/admin/v1/snapshots/${snapshotId}`);
    const res = await axios.post(`/admin/v1/events/${eventId}/snapshots`, payload);

    showMessage("Snapshot updated successfully.", "success");
    editSnapshotMode.value = false;
    await fetchSnapshots();
    if (res.data?.data?.id) {
      activeTabId.value = res.data.data.id;
    }
  } catch (err) {
    console.error("Update snapshot failed:", err);
    showMessage(err.response?.data?.error || "Failed to update snapshot.", "error");
  } finally {
    snapshotLoading.value = false;
  }
};

const addSnapshot = async () => {
  snapshotLoading.value = true;
  try {
    let finalSnapshotName = newSnapshot.value.snapshot_name;
    if (finalSnapshotName === "Custom date") {
      const days = Math.max(2, Math.min(30, Number(customDays.value) || 2));
      finalSnapshotName = `T+${days} Days`;
    }

    const payload = {
      event_id: eventId,
      snapshot_name: finalSnapshotName,
      snapshot_type: finalSnapshotName === "Closed" ? "closed" : "custom",
      observed_at: newSnapshot.value.observed_at,
      ticket_items: newSnapshot.value.ticket_items.map(item => ({
        name: item.name,
        type: item.type,
        currency: item.currency,
        price: Number(item.price) || 0,
        total_quantity: Number(item.total_quantity) || 0,
        sold: Number(item.sold) || 0,
        refund: Number(item.refund) || 0
      }))
    };
    attachClosedSnapshotDemographics(payload, newSnapshot.value);

    const res = await axios.post(`/admin/v1/events/${eventId}/snapshots`, payload);

    showMessage("Snapshot added successfully.", "success");
    showSnapshotDialog.value = false;
    resetSnapshotForm();

    await fetchSnapshots();
    if (res.data?.data?.id) {
      activeTabId.value = res.data.data.id;
    }
  } catch (err) {
    console.error("Add snapshot failed:", err);
    showMessage(err.response?.data?.error || "Failed to add snapshot.", "error");
  } finally {
    snapshotLoading.value = false;
  }
};

const deleteSnapshot = async (snapshotId) => {
  if (!confirm("Are you sure you want to delete this snapshot?")) return;
  try {
    await axios.delete(`/admin/v1/snapshots/${snapshotId}`);
    showMessage("Snapshot deleted successfully.", "success");
    editSnapshotMode.value = false;
    await fetchSnapshots();
    if (snapshots.value.length > 0) {
      activeTabId.value = snapshots.value[0].id;
    } else {
      activeTabId.value = null;
    }
  } catch (err) {
    console.error("Delete snapshot failed:", err);
    showMessage("Failed to delete snapshot.", "error");
  }
};

// 第三區：計算當前選中 (Tab) 的 Snapshot 指標，隨 Tab 切換連動
// shared with the public share page so both always show identical figures
const eventSummaryMetrics = computed(() =>
  computeEventSummaryMetrics(currentActiveSnapshot.value, snapshots.value)
);

// export report file name
const getReportFileName = () => {
  const event = eventData.value || {}
  const eventName = String(event.event_name || 'offline_event')
    .trim()
    .replace(/[\\/:*?"<>|]/g, '-')
    .replace(/\s+/g, '_')

  const date = event.event_date
    ? new Date(event.event_date)
    : null

  const yyyy = date && !Number.isNaN(date.getTime())
    ? date.getFullYear()
    : 'unknown'

  const mm = date && !Number.isNaN(date.getTime())
    ? String(date.getMonth() + 1).padStart(2, '0')
    : 'unknown'

  const dd = date && !Number.isNaN(date.getTime())
    ? String(date.getDate()).padStart(2, '0')
    : 'unknown'

  const session = String(event.session || 'unknown')
      .trim()
      .replace(/:/g, '_')
      .replace(/[\\/*?"<>|]/g, '-')
      .replace(/\s+/g, '-')
  return `${eventName}_${yyyy}_${mm}_${dd}_${session}_report`
}

const exportEventReport = async () => {
  try {
    const event = eventData.value
    const selectedSnapshot = currentActiveSnapshot.value

    if (!event || !event.event_name) {
      showMessage('Event information is not available.', 'error')
      return
    }

    // Sort snapshots by observation time
    const allSnapshots = [...(snapshots.value || [])].sort(
      (a, b) =>
        new Date(a.observed_at || 0) -
        new Date(b.observed_at || 0)
    )

    // Find the final Closed snapshot
    const closedSnapshot = allSnapshots.find(
      snapshot =>
        snapshot.snapshot_name === 'Closed' ||
        snapshot.snapshot_type === 'closed'
    )

    // Artist names
    const artists = selectedArtistsList.value
      .map(getArtistLabel)
      .filter(Boolean)
      .join(', ')

    // Helper: normalize numeric values
    const toNumber = value => Number(value) || 0

    // Helper: calculate net sold
    const getNetSold = item => {
      if (item.net_sold != null) {
        return toNumber(item.net_sold)
      }

      return Math.max(
        0,
        toNumber(item.sold) - toNumber(item.refund)
      )
    }

    // Helper: calculate revenue
    const getRevenue = item => {
      if (item.revenue != null) {
        return toNumber(item.revenue)
      }

      return getNetSold(item) * toNumber(item.price)
    }

    // --------------------------------------------------
    // Sheet 1: Event Overview
    // --------------------------------------------------

    const metrics = eventSummaryMetrics.value || {}

    const overviewRows = [
      {
        Section: 'Event Information',
        Field: 'Event Name',
        Value: event.event_name
      },
      {
        Section: 'Event Information',
        Field: 'Event Type',
        Value: event.type
      },
      {
        Section: 'Event Information',
        Field: 'Artists',
        Value: artists
      },
      {
        Section: 'Event Information',
        Field: 'Event Date',
        Value: event.event_date
      },
      {
        Section: 'Event Information',
        Field: 'Session',
        Value: event.session
      },
      {
        Section: 'Event Information',
        Field: 'Country',
        Value: event.held_country
      },
      {
        Section: 'Event Information',
        Field: 'City',
        Value: event.held_city
      },
      {
        Section: 'Event Information',
        Field: 'Venue',
        Value: event.venue
      },
      {
        Section: 'Event Information',
        Field: 'Organizer',
        Value: event.organizer
      },
      {
        Section: 'Event Information',
        Field: 'Ticket Release',
        Value: event.ticket_release
      },
      {
        Section: 'Event Information',
        Field: 'Ticket Close',
        Value: event.ticket_close
      },

      {
        Section: 'Event Summary',
        Field: 'Selected Snapshot',
        Value: selectedSnapshot?.snapshot_name || ''
      },
      {
        Section: 'Event Summary',
        Field: 'Observed At',
        Value: selectedSnapshot?.observed_at || ''
      },
      {
        Section: 'Event Summary',
        Field: 'Ticket Revenue',
        Value: metrics.ticketRevenue ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Benefit Revenue',
        Value: metrics.benefitRevenue ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Total Revenue',
        Value: metrics.totalRevenue ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Ticket Sell-through (%)',
        Value: metrics.ticketSellThrough ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Benefit Sell-through (%)',
        Value: metrics.benefitSellThrough ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Sales Velocity',
        Value: metrics.salesVelocity ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Ticket Remaining',
        Value: metrics.ticketRemaining ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Benefit Remaining',
        Value: metrics.benefitRemaining ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Ticket Refund Rate (%)',
        Value: metrics.ticketRefundRate ?? 0
      },
      {
        Section: 'Event Summary',
        Field: 'Benefit Refund Rate (%)',
        Value: metrics.benefitRefundRate ?? 0
      }
    ]

    // --------------------------------------------------
    // Sheet 2: Ticket & Benefit Sales
    // All snapshots
    // --------------------------------------------------

    const salesRows = []

    allSnapshots.forEach(snapshot => {
      ;(snapshot.ticket_items || []).forEach(item => {
        const sold = toNumber(item.sold)
        const refund = toNumber(item.refund)
        const netSold = getNetSold(item)
        const totalQuantity = toNumber(item.total_quantity)
        const price = toNumber(item.price)

        salesRows.push({
          Snapshot: snapshot.snapshot_name || '',
          'Observed At': snapshot.observed_at || '',
          Type: item.type || '',
          'Item Name': item.name || '',
          Currency: item.currency || '',
          'Unit Price': price,
          'Total Quantity': totalQuantity,
          Sold: sold,
          Refund: refund,
          'Net Sold': netSold,
          'Sell-through (%)': totalQuantity > 0
            ? Number(((netSold / totalQuantity) * 100).toFixed(2))
            : 0,
          Revenue: getRevenue(item)
        })
      })
    })

    // --------------------------------------------------
    // Sheet 3: Sales Revenue Trend
    // Group by snapshot and currency
    // --------------------------------------------------

    const trendRows = []

    allSnapshots.forEach(snapshot => {
      const currencyTotals = {}

      ;(snapshot.ticket_items || []).forEach(item => {
        const currency = item.currency || 'Unknown'
        const revenue = getRevenue(item)

        if (!currencyTotals[currency]) {
          currencyTotals[currency] = {
            ticketRevenue: 0,
            benefitRevenue: 0
          }
        }

        if (item.type === 'ticket') {
          currencyTotals[currency].ticketRevenue += revenue
        } else if (item.type === 'benefit') {
          currencyTotals[currency].benefitRevenue += revenue
        }
      })

      Object.entries(currencyTotals).forEach(([currency, totals]) => {
        trendRows.push({
          Snapshot: snapshot.snapshot_name || '',
          'Observed At': snapshot.observed_at || '',
          Currency: currency,
          'Ticket Revenue': totals.ticketRevenue,
          'Benefit Revenue': totals.benefitRevenue,
          'Total Revenue':
            totals.ticketRevenue + totals.benefitRevenue
        })
      })
    })

    // --------------------------------------------------
    // Sheet 4: Ticket Zone Performance
    // Selected snapshot
    // --------------------------------------------------

    const zoneRows = (selectedSnapshot?.ticket_items || [])
      .filter(item => item.type === 'ticket')
      .map(item => {
        const sold = toNumber(item.sold)
        const refund = toNumber(item.refund)
        const netSold = getNetSold(item)
        const totalQuantity = toNumber(item.total_quantity)
        const price = toNumber(item.price)

        return {
          'Ticket Zone': item.name || '',
          Currency: item.currency || '',
          'Unit Price': price,
          'Total Quantity': totalQuantity,
          Sold: sold,
          Refund: refund,
          'Net Sold': netSold,
          'Sell-through (%)': totalQuantity > 0
            ? Number(((netSold / totalQuantity) * 100).toFixed(2))
            : 0,
          Revenue: getRevenue(item)
        }
      })

    // --------------------------------------------------
    // Sheet 5: Audience Demographics
    // Closed snapshot only
    // --------------------------------------------------

    const gender = closedSnapshot?.gender_distribution || {}
    const age = closedSnapshot?.age_distribution || {}

    const demographicRows = [
      {
        Distribution: 'Gender',
        Category: 'Male',
        'Percentage (%)': toNumber(gender.male)
      },
      {
        Distribution: 'Gender',
        Category: 'Female',
        'Percentage (%)': toNumber(gender.female)
      },
      {
        Distribution: 'Gender',
        Category: 'Other',
        'Percentage (%)': toNumber(gender.other)
      },
      {
        Distribution: 'Age',
        Category: '10s',
        'Percentage (%)': toNumber(age.age_10s)
      },
      {
        Distribution: 'Age',
        Category: '20s',
        'Percentage (%)': toNumber(age.age_20s)
      },
      {
        Distribution: 'Age',
        Category: '30s',
        'Percentage (%)': toNumber(age.age_30s)
      },
      {
        Distribution: 'Age',
        Category: '40s',
        'Percentage (%)': toNumber(age.age_40s)
      },
      {
        Distribution: 'Age',
        Category: '50+',
        'Percentage (%)': toNumber(age.age_50_plus)
      }
    ]

    // --------------------------------------------------
    // Prepare workbook
    // --------------------------------------------------

    const sheets = [
      {
        name: 'Event Overview',
        rows: overviewRows
      },
      {
        name: 'Ticket & Benefit Sales',
        rows: salesRows
      },
      {
        name: 'Sales Revenue Trend',
        rows: trendRows
      },
      {
        name: 'Ticket Zone Performance',
        rows: zoneRows
      },
      {
        name: 'Audience Demographics',
        rows: demographicRows
      }
    ]

    // Export workbook
    await exportWorkbook(sheets, `${getReportFileName()}.xlsx`)

    showMessage(
      'Excel report exported successfully.',
      'success'
    )

  } catch (err) {
    console.error('Export event report failed:', err)

    showMessage(
      'Failed to export Excel report.',
      'error'
    )
  }
}

const exportEventPDF = async () => {
  if (exportingPDF.value) return

  try {
    const element = reportRef.value?.getElement()

    if (!element) {
      showMessage('PDF report is not available.', 'error')
      return
    }

    exportingPDF.value = true

    const options = {
      margin: [10, 10, 18, 10],
      filename: `${getReportFileName()}.pdf`,
      image: {
        type: 'jpeg',
        quality: 0.98
      },
      html2canvas: {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: 794
      },
      jsPDF: {
        unit: 'mm',
        format: 'a4',
        orientation: 'portrait'
      },
      pagebreak: {
        mode: ['css'],
        before: ['.report-page-start'],
        avoid: [
          '.kpi-card',
          '.info-item',
          '.demographic-card',
          '.trend-item'
        ]
      }
    }


    await html2pdf()
      .set(options)
      .from(element)
      .save()

    showMessage('PDF report exported successfully.', 'success')
  } catch (error) {
    console.error('PDF export failed:', error)
    showMessage('Failed to export PDF report.', 'error')
  } finally {
    exportingPDF.value = false
  }
}

onMounted(() => {
  fetchEventDetail();
  fetchSnapshots();
});

// The artist list is large and only needed by the edit form: load it on entering edit mode.
watch(editMode, (isEditing) => {
  if (isEditing) fetchArtistOptions();
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- 頂部導航與標題 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <button
          @click="router.push('/admin/campaigns/offline')"
          class="p-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <h2 class="text-2xl font-semibold text-gray-800">
          Event Management Details
        </h2>
      </div>
      <!-- Export Buttons -->
      <div class="flex items-center gap-2 flex-shrink-0">

        <!-- Excel -->
        <button
            @click="exportEventReport"
            :disabled="exportingExcel"
            class="inline-flex items-center gap-2 px-4 py-2.5
             border border-indigo-600 text-indigo-600
             rounded-lg hover:bg-indigo-50 transition
             text-sm font-medium disabled:opacity-50
             disabled:cursor-not-allowed"
        >
          <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
          >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 16V4m0 12l-4-4m4 4l4-4M4 20h16"
            />
          </svg>

          {{ exportingExcel ? 'Exporting...' : 'Export Excel' }}
        </button>

        <!-- PDF -->
        <button
            @click="exportEventPDF"
            :disabled="exportingPDF"
            class="inline-flex items-center gap-2 px-4 py-2.5
             bg-indigo-600 text-white
             rounded-lg hover:bg-indigo-700 transition
             text-sm font-medium shadow-sm
             disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
          >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 16V4m0 12l-4-4m4 4l4-4M4 20h16"
            />
          </svg>

          {{ exportingPDF ? 'Generating...' : 'Export PDF' }}
        </button>

      </div>
    </div>

    <!-- 載入狀態 -->
    <div v-if="detailLoading" class="text-center py-12 text-gray-500">
      Loading event details...
    </div>

    <div v-else class="space-y-6">

      <!-- Artist share link (public read-only report) -->
      <EventShareLinkCard
          :event-id="eventId"
          :has-share-link="Boolean(eventData.has_share_link)"
          :share-token-created-at="eventData.share_token_created_at || null"
          @notify="showMessage"
          @updated="(link) => { eventData = { ...eventData, ...link } }"
      />

      <!-- 第一區：Event Info -->
      <div class="bg-white rounded-xl shadow p-6 border border-gray-200 mb-6">
        <!-- 區塊標題與編輯按鈕 -->
        <div class="flex items-center justify-between pb-3 border-b border-gray-100 mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Event Information</h3>
          <div class="flex gap-2">
            <button
                v-if="!editMode"
                @click="editMode = true"
                class="px-3 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-medium hover:bg-indigo-700 transition">
              Edit Info
            </button>
            <template v-else>
              <button
                  @click="editMode = false"
                  class="px-3 py-1.5 border border-gray-300 text-gray-700 rounded-lg text-xs font-medium hover:bg-gray-50 transition">
                Cancel
              </button>
              <button
                  @click="updateEvent"
                  :disabled="loading"
                  class="px-3 py-1.5 bg-green-600 text-white rounded-lg text-xs font-medium hover:bg-green-700 transition">
                {{ loading ? 'Saving...' : 'Save' }}
              </button>
            </template>
          </div>
        </div>

        <div class="space-y-4">

          <!-- Row 1: Event Name & Type -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="md:col-span-2">
              <label class="block text-xs font-medium text-gray-500 mb-1">Event Name</label>
              <input
                  v-model="eventData.event_name"
                  :readonly="!editMode"
                  type="text"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none font-semibold'"/>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Event Type</label>
              <select
                  v-if="editMode"
                  v-model="eventData.type"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none">
                <option value="" disabled>Select Type</option>
                <option v-for="option in eventTypeOptions" :key="option" :value="option">{{ option }}</option>
              </select>
              <div v-else class="py-1">
          <span
              class="px-2.5 py-1 text-xs font-semibold rounded-full inline-flex items-center gap-1"
              :class="{
              'bg-blue-50 text-blue-700 border border-blue-100': eventData.type === 'Concert',
              'bg-purple-50 text-purple-700 border border-purple-100': eventData.type === 'Fan Meeting',
              'bg-emerald-50 text-emerald-700 border border-emerald-100': eventData.type === 'Festival',
              'bg-amber-50 text-amber-700 border border-amber-100': eventData.type === 'Showcase',
              'bg-rose-50 text-rose-700 border border-rose-100': eventData.type === 'Award Show',
              'bg-gray-100 text-gray-700 border border-gray-200': !['Concert', 'Fan Meeting', 'Festival', 'Showcase', 'Award Show'].includes(eventData.type)
            }">
            {{ eventData.type || '-' }}
          </span>
              </div>
            </div>
          </div>

          <!-- Row 2: Artists (加上模糊搜尋) -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Artists</label>
            <!-- 編輯模式：多選下拉選單 -->
            <div v-if="editMode" class="relative">
              <div
                  @click="isArtistDropdownOpen = !isArtistDropdownOpen"
                  class="w-full border border-gray-300 rounded-md px-3 py-1.5 bg-white flex items-center justify-between cursor-pointer focus:ring-2 focus:ring-indigo-500 min-h-[42px]">

                <!-- 已選擇的藝人 Tags 顯示區 -->
                <div class="flex flex-wrap items-center gap-1.5 min-w-0 py-1">
                  <template v-if="selectedArtistsList.length > 0">
                    <span
                        v-for="artist in selectedArtistsList"
                        :key="artist.id"
                        class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-100">
                        {{ getArtistLabel(artist) }}
                      <button
                          @click.stop="toggleArtistSelection(artist.id)"
                          type="button"
                          class="hover:text-indigo-900 font-bold ml-0.5">
                        ×
                      </button>
                    </span>
                  </template>
                  <span v-else class="text-sm text-gray-400">Select Artists...</span>
                </div>

                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 flex-shrink-0 ml-2" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>

              <!-- 下拉選單列表 (包含頂部模糊搜尋輸入框) -->
              <div
                  v-if="isArtistDropdownOpen"
                  class="absolute z-30 mt-1 w-full bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-y-auto">

                <!-- 模糊搜尋輸入框 -->
                <div class="p-2 sticky top-0 bg-white border-b border-gray-100 z-10">
                  <input
                      v-model="artistSearchQuery"
                      type="text"
                      placeholder="Search artist name..."
                      class="w-full px-2.5 py-1.5 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      @click.stop/>
                </div>

                <!-- 藝人選項清單 -->
                <template v-if="filteredArtistOptions.length > 0">
                  <div
                      v-for="artist in filteredArtistOptions"
                      :key="artist.id"
                      @click="toggleArtistSelection(artist.id)"
                      class="p-2.5 hover:bg-indigo-50 cursor-pointer flex items-center justify-between border-b border-gray-50 last:border-none transition">
                    <div class="flex items-center gap-3 min-w-0">
                      <div
                          class="w-8 h-8 rounded-full overflow-hidden bg-gray-200 flex-shrink-0 flex items-center justify-center border border-gray-200">
                        <img v-if="artist.image" :src="artist.image" alt="" class="w-full h-full object-cover"/>
                        <span v-else class="text-[10px] text-gray-500 font-bold">👤</span>
                      </div>
                      <!-- 藝人名稱與生日資訊 -->
                      <div class="flex flex-col min-w-0">
                  <span class="text-sm font-medium text-gray-800 truncate">
                    {{ getArtistLabel(artist) }}
                  </span>
                        <span class="text-xs text-gray-400">
                    Birth: {{ formatBirthDate(artist.birth) }}
                  </span>
                      </div>
                    </div>
                    <!-- 勾選狀態圖示 -->
                    <div class="flex-shrink-0">
                      <input
                          type="checkbox"
                          :checked="eventData.artist_ids.some(
                      id => String(id) === String(artist.id)
                    )"
                          class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 pointer-events-none"
                      />
                    </div>
                  </div>
                </template>

                <!-- 無搜尋結果提示 -->
                <div v-else class="p-3 text-xs text-center text-gray-400">
                  No artists found.
                </div>

              </div>
            </div>

            <!-- 非編輯模式：展示多個藝人 Tags -->
            <div v-else class="flex flex-wrap items-center gap-2 px-0 py-1.5">
              <template v-if="selectedArtistsList.length > 0">
                <div
                    v-for="artist in selectedArtistsList"
                    :key="artist.id"
                    class="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded-full border border-gray-200">
                  <div
                      class="w-5 h-5 rounded-full overflow-hidden bg-gray-200 flex-shrink-0 flex items-center justify-center">
                    <img v-if="artist.image" :src="artist.image" alt="" class="w-full h-full object-cover"/>
                    <span v-else class="text-[9px] text-gray-500 font-bold">👤</span>
                  </div>
                  <span class="text-xs text-gray-800 font-medium">
              {{ getArtistLabel(artist) }}
            </span>
                </div>
              </template>
              <span v-else class="text-sm text-gray-400">-</span>
            </div>
          </div>

          <!-- Row 3: Date, Session, Country, City -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Show Date</label>
              <input
                  v-model="eventData.event_date"
                  :readonly="!editMode"
                  type="date"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Session</label>
              <input
                  v-model="eventData.session"
                  :readonly="!editMode"
                  type="time"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Country</label>
              <select
                  v-if="editMode"
                  v-model="eventData.held_country"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none">
                <option v-for="c in indexToCountry" :key="c" :value="c">{{ c }}</option>
              </select>
              <div v-else class="text-sm text-gray-700 py-1">{{ eventData.held_country || '-' }}</div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">City</label>
              <input
                  v-model="eventData.held_city"
                  :readonly="!editMode"
                  type="text"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
          </div>

          <!-- Row 4: Venue, Organizer -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Venue</label>
              <input
                  v-model="eventData.venue"
                  :readonly="!editMode"
                  type="text"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Organizer</label>
              <input
                  v-model="eventData.organizer"
                  :readonly="!editMode"
                  type="text"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
          </div>

          <!-- Row 5: Ticket Release, Close Time -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Ticket Release</label>
              <input
                  v-model="eventData.ticket_release"
                  :readonly="!editMode"
                  type="datetime-local"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Ticket Close Time</label>
              <input
                  v-model="eventData.ticket_close"
                  :readonly="!editMode"
                  type="datetime-local"
                  class="w-full text-sm transition"
                  :class="editMode ? 'border border-gray-300 rounded-md px-3 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none' : 'bg-transparent border-none px-0 py-1 text-gray-700 pointer-events-none'"/>
            </div>
          </div>

        </div>
      </div>

      <!-- 第二區：Event Ticket Sales Info (Snapshot 資訊區 - Tab 型式) -->
      <div class="bg-white rounded-xl shadow p-6 border border-gray-200">
        <div class="flex justify-between items-center mb-4 pb-3 border-b border-gray-100">
          <h3 class="text-lg font-semibold text-gray-800">Event Ticket Sales Info (Snapshots)</h3>
          <button
            @click="showSnapshotDialog = true"
            class="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Add Snapshot
          </button>
        </div>

        <div v-if="snapshots.length === 0" class="text-center py-8 text-gray-400 text-sm">
          No ticket sales snapshots added yet. Click "Add Snapshot" to record sales data.
        </div>

        <div v-else>
          <!-- Tab 列 -->
          <div class="flex border-b border-gray-200 mb-4 overflow-x-auto gap-2">
            <button
              v-for="snapshot in snapshots"
              :key="snapshot.id"
              @click="switchTab(snapshot.id)"
              class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap"
              :class="activeTabId === snapshot.id ? 'border-indigo-600 text-indigo-600 bg-indigo-50/50 rounded-t-lg' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'">
              {{ snapshot.snapshot_name }}
            </button>
          </div>

          <!-- 當前啟用的 Tab 內容呈現區 -->
          <div v-if="currentActiveSnapshot" class="border border-gray-200 rounded-xl p-4 bg-gray-50 shadow-sm">

            <!-- 標題與操作按鈕區 (Edit / Save / Cancel / Delete) -->
            <div class="flex justify-between items-center mb-3 pb-2 border-b border-gray-200">
              <div class="flex items-center gap-3">
                <span class="text-xs text-gray-500">Observed At:
                  <template v-if="!editSnapshotMode">{{ formatDateTime(currentActiveSnapshot.observed_at) }}</template>
                  <input v-else-if="editingSnapshotData" v-model="editingSnapshotData.observed_at" type="datetime-local" class="border rounded px-2 py-1 text-xs bg-white ml-2" />
                </span>
              </div>

              <div class="flex items-center gap-2">
                <template v-if="!editSnapshotMode">
                  <!-- Edit Icon 按鈕 -->
                  <button
                    @click="startEditSnapshot"
                    class="flex items-center gap-1 px-3 py-1 bg-indigo-50 text-indigo-600 border border-indigo-200 rounded text-xs font-medium hover:bg-indigo-100 transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                    Edit
                  </button>
                  <button
                    @click="deleteSnapshot(currentActiveSnapshot.id)"
                    class="text-red-600 hover:text-red-800 text-xs px-2.5 py-1 bg-white border border-red-200 rounded shadow-sm transition">
                    Delete
                  </button>
                </template>
                <template v-else-if="editingSnapshotData">
                  <button
                    @click="saveSnapshotEdit"
                    :disabled="snapshotLoading"
                    class="px-3 py-1 bg-green-600 text-white rounded text-xs font-medium hover:bg-green-700 transition">
                    Save
                  </button>
                  <button
                    @click="cancelEditSnapshot"
                    class="px-3 py-1 bg-gray-200 text-gray-700 rounded text-xs font-medium hover:bg-gray-300 transition">
                    Cancel
                  </button>
                </template>
              </div>
            </div>

            <!-- 非編輯模式：明細表格 -->
            <div v-if="!editSnapshotMode" class="overflow-x-auto bg-white rounded-lg border border-gray-200">
              <table class="min-w-full text-xs text-gray-700">
                <thead class="bg-gray-100 uppercase text-[10px] text-gray-600">
                <tr>
                  <th class="px-4 py-2 text-left">Name</th>
                  <th class="px-4 py-2 text-left">Type</th>
                  <th class="px-4 py-2 text-left">Currency</th>
                  <th class="px-4 py-2 text-right">Price</th>
                  <th class="px-4 py-2 text-right">Total Qty</th>
                  <th class="px-4 py-2 text-right">Sold</th>
                  <th class="px-4 py-2 text-right">Refund</th>
                  <th class="px-4 py-2 text-right">Net Sold</th>
                  <th class="px-4 py-2 text-right">Revenue</th>
                  <th class="px-4 py-2 text-right">Sell-Through Rate</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(item, idx) in currentActiveSnapshot.ticket_items" :key="idx" class="border-t hover:bg-gray-50">
                  <td class="px-4 py-2 font-medium text-gray-900">{{ item.name }}</td>
                  <td class="px-4 py-2 capitalize">
                    <span class="px-2 py-0.5 rounded text-[10px]"
                          :class="item.type === 'ticket' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'">
                      {{ item.type }}
                    </span>
                  </td>
                  <td class="px-4 py-2">{{ item.currency }}</td>
                  <td class="px-4 py-2 text-right">{{ formatNumber(item.price) }}</td>
                  <td class="px-4 py-2 text-right">{{ formatNumber(item.total_quantity) }}</td>
                  <td class="px-4 py-2 text-right">{{ formatNumber(item.sold) }}</td>
                  <td class="px-4 py-2 text-right">{{ formatNumber(item.refund) }}</td>
                  <td class="px-4 py-2 text-right font-semibold text-indigo-600">{{ formatNumber(item.net_sold) }}</td>
                  <td class="px-4 py-2 text-right font-semibold text-green-600">{{ formatNumber(item.revenue) }}</td>
                  <td class="px-4 py-2 text-right font-bold text-gray-800">{{ item.sell_through_rate }}%</td>
                </tr>
                </tbody>
              </table>
            </div>

            <!-- 編輯模式：動態輸入表格 -->
            <div v-else-if="editingSnapshotData" class="space-y-3 bg-white p-4 rounded-lg border border-gray-200">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-semibold text-gray-700">編輯票區明細</span>
                <button @click="addEditingTicketRow" type="button" class="text-xs bg-indigo-50 text-indigo-600 px-2.5 py-1 rounded hover:bg-indigo-100 transition font-medium">+ Add Tier</button>
              </div>

              <div class="space-y-2">
                <div v-for="(item, index) in editingSnapshotData.ticket_items" :key="index" class="p-3 bg-gray-50 rounded-lg border border-gray-200 grid grid-cols-1 md:grid-cols-8 gap-2 items-end">
                  <div class="md:col-span-2">
                    <label class="block text-[10px] text-gray-500 mb-0.5">名稱</label>
                    <input v-model="item.name" type="text" class="w-full border rounded px-2 py-1 text-sm bg-white" />
                  </div>
                  <div>
                    <label class="block text-[10px] text-gray-500 mb-0.5">Type</label>
                    <select v-model="item.type" class="w-full border rounded px-2 py-1 text-sm bg-white capitalize">
                      <option v-for="t in typeOptions" :key="t" :value="t">{{ t }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-[10px] text-gray-500 mb-0.5">貨幣</label>
                    <select v-model="item.currency" class="w-full border rounded px-2 py-1 text-sm bg-white">
                      <option v-for="c in currencyOptions" :key="c.value" :value="c.value">{{ c.label }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-[10px] text-gray-500 mb-0.5">單價</label>
                    <input v-model.number="item.price" type="number" class="w-full border rounded px-2 py-1 text-sm bg-white" />
                  </div>
                  <div>
                    <label class="block text-[10px] text-gray-500 mb-0.5">總數量</label>
                    <input v-model.number="item.total_quantity" type="number" class="w-full border rounded px-2 py-1 text-sm bg-white" />
                  </div>
                  <div>
                    <label class="block text-[10px] text-gray-500 mb-0.5">售出數</label>
                    <input v-model.number="item.sold" type="number" class="w-full border rounded px-2 py-1 text-sm bg-white" />
                  </div>
                  <div class="flex items-center gap-1">
                    <div class="flex-1">
                      <label class="block text-[10px] text-gray-500 mb-0.5">退款數</label>
                      <input v-model.number="item.refund" type="number" class="w-full border rounded px-2 py-1 text-sm bg-white" />
                    </div>
                    <button @click="removeEditingTicketRow(index)" type="button" class="text-red-500 hover:text-red-700 p-1 mt-4">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="editingSnapshotData && editingSnapshotData.snapshot_name === 'Closed'" class="mt-5 p-4 bg-white rounded-lg border border-indigo-200 space-y-4">
              <h4 class="text-sm font-semibold text-gray-800">Audience Demographics</h4>
              <p class="text-xs text-gray-500">僅 Closed snapshot 可輸入，兩組比例各自需合計為 100%。</p>
              <div>
                <h5 class="text-xs font-semibold text-gray-700 mb-2">Gender Distribution (%)</h5>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div v-for="field in genderDistributionFields" :key="field.key">
                    <label class="block text-xs text-gray-500 mb-1">{{ field.label }}</label>
                    <input v-model.number="editingSnapshotData.gender_distribution[field.key]" type="number" min="0" max="100" step="0.01" class="w-full border rounded px-2 py-1.5 text-sm bg-white" />
                  </div>
                </div>
              </div>
              <div>
                <h5 class="text-xs font-semibold text-gray-700 mb-2">Age Distribution (%)</h5>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                  <div v-for="field in ageDistributionFields" :key="field.key">
                    <label class="block text-xs text-gray-500 mb-1">{{ field.label }}</label>
                    <input v-model.number="editingSnapshotData.age_distribution[field.key]" type="number" min="0" max="100" step="0.01" class="w-full border rounded px-2 py-1.5 text-sm bg-white" />
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- 第三區：Event Summary -->
      <div class="space-y-6">
        <EventSummaryCards :metrics="eventSummaryMetrics"/>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          <SalesTrendLineChart
              v-if="hasSalesTrendChartData"
              :snapshots="chartSnapshots"
              title="Sales Revenue Trend"
          />
          <div
              v-else
              class="bg-white rounded-xl shadow p-6 border border-gray-200 min-h-[420px] flex items-center justify-center text-sm text-gray-400">
            No valid snapshot data available for the sales trend chart.
          </div>

          <TicketZonePerformanceChart
              v-if="hasZonePerformanceChartData"
              :ticketItems="activeChartTicketItems"
              title="Ticket Zone Performance"
          />
          <div
              v-else
              class="bg-white rounded-xl shadow p-6 border border-gray-200 min-h-[420px] flex items-center justify-center text-sm text-gray-400">
            No ticket zone data available for the selected snapshot.
          </div>

        </div>
        <!-- Gender & Age Distribution -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GenderDistributionChart
              :snapshot="currentActiveSnapshot"
          />

          <AgeDistributionChart
              :snapshot="currentActiveSnapshot"
          />
        </div>

      </div>

      <!-- PDF Report Template -->
      <div
          class="fixed left-[-9999px] top-0 pointer-events-none"
          aria-hidden="true"
      >
        <OfflineEventReport
            ref="reportRef"
            :event="eventData"
            :selected-snapshot="currentActiveSnapshot"
            :snapshots="snapshots"
            :artists="selectedArtistsList"
            :summary-metrics="eventSummaryMetrics"
        />
      </div>
    </div>

    <!-- 新增 Snapshot 彈窗 (Modal) -->
    <div v-if="showSnapshotDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6">
        <div class="flex justify-between items-center pb-3 border-b border-gray-100 mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Add Ticket Sales Snapshot</h3>
          <button @click="showSnapshotDialog = false" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                 stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <!-- 基本設定 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">Snapshot Name</label>
              <select
                v-model="newSnapshot.snapshot_name"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none">
                <option v-for="opt in snapshotNameOptions" :key="opt" :value="opt">{{ opt }}</option>
              </select>

              <!-- 當選擇 Custom date 時顯示天數設定 -->
              <div v-if="newSnapshot.snapshot_name === 'Custom date'" class="mt-2 flex items-center gap-2">
                <span class="text-xs text-gray-600 font-medium">T +</span>
                <input
                  v-model.number="customDays"
                  type="number"
                  min="2"
                  max="30"
                  class="w-20 border border-gray-300 rounded-md px-2 py-1 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-indigo-50/30" />
                <span class="text-xs text-gray-600 font-medium">Days (2 - 30)</span>
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">Observed At (觀測時間)</label>
              <input v-model="newSnapshot.observed_at" type="datetime-local"
                     class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"/>
            </div>
          </div>

          <!-- Tickets & Benefits 列表設定 -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="text-sm font-semibold text-gray-700">Tickets & Benefits 票區設定</label>
              <button @click="addTicketRow" type="button"
                      class="text-xs bg-gray-100 px-2.5 py-1 rounded hover:bg-gray-200 transition font-medium text-indigo-600">
                + Add Tier
              </button>
            </div>

            <div class="space-y-3">
              <div v-for="(item, index) in newSnapshot.ticket_items" :key="index"
                   class="p-3 bg-gray-50 rounded-lg border border-gray-200 grid grid-cols-1 md:grid-cols-8 gap-2 items-end">
                <div class="md:col-span-2">
                  <label class="block text-[10px] text-gray-500 mb-0.5">名稱</label>
                  <input v-model="item.name" type="text" placeholder="例: VIP 區"
                         class="w-full border rounded px-2 py-1 text-sm bg-white"/>
                </div>

                <div>
                  <label class="block text-[10px] text-gray-500 mb-0.5">Type</label>
                  <select v-model="item.type" class="w-full border rounded px-2 py-1 text-sm bg-white capitalize">
                    <option v-for="t in typeOptions" :key="t" :value="t">{{ t }}</option>
                  </select>
                </div>

                <div>
                  <label class="block text-[10px] text-gray-500 mb-0.5">貨幣</label>
                  <select v-model="item.currency" class="w-full border rounded px-2 py-1 text-sm bg-white">
                    <option v-for="c in currencyOptions" :key="c.value" :value="c.value">{{ c.label }}</option>
                  </select>
                </div>

                <div>
                  <label class="block text-[10px] text-gray-500 mb-0.5">單價</label>
                  <input v-model.number="item.price" type="number"
                         class="w-full border rounded px-2 py-1 text-sm bg-white"/>
                </div>

                <div>
                  <label class="block text-[10px] text-gray-500 mb-0.5">總數量</label>
                  <input v-model.number="item.total_quantity" type="number"
                         class="w-full border rounded px-2 py-1 text-sm bg-white"/>
                </div>

                <div>
                  <label class="block text-[10px] text-gray-500 mb-0.5">售出數</label>
                  <input v-model.number="item.sold" type="number"
                         class="w-full border rounded px-2 py-1 text-sm bg-white"/>
                </div>

                <div class="flex items-center gap-1">
                  <div class="flex-1">
                    <label class="block text-[10px] text-gray-500 mb-0.5">退款數</label>
                    <input v-model.number="item.refund" type="number"
                           class="w-full border rounded px-2 py-1 text-sm bg-white"/>
                  </div>
                  <button @click="removeTicketRow(index)" type="button"
                          class="text-red-500 hover:text-red-700 p-1 mt-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="newSnapshot.snapshot_name === 'Closed'" class="mt-5 p-4 bg-white rounded-lg border border-indigo-200 space-y-4">
            <h4 class="text-sm font-semibold text-gray-800">Audience Demographics</h4>
            <p class="text-xs text-gray-500">僅 Closed snapshot 可輸入，兩組比例各自需合計為 100%。</p>
            <div>
              <h5 class="text-xs font-semibold text-gray-700 mb-2">Gender Distribution (%)</h5>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <div v-for="field in genderDistributionFields" :key="field.key">
                  <label class="block text-xs text-gray-500 mb-1">{{ field.label }}</label>
                  <input v-model.number="newSnapshot.gender_distribution[field.key]" type="number" min="0" max="100" step="0.01" class="w-full border rounded px-2 py-1.5 text-sm bg-white" />
                </div>
              </div>
            </div>
            <div>
              <h5 class="text-xs font-semibold text-gray-700 mb-2">Age Distribution (%)</h5>
              <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div v-for="field in ageDistributionFields" :key="field.key">
                  <label class="block text-xs text-gray-500 mb-1">{{ field.label }}</label>
                  <input v-model.number="newSnapshot.age_distribution[field.key]" type="number" min="0" max="100" step="0.01" class="w-full border rounded px-2 py-1.5 text-sm bg-white" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部按鈕區 -->
        <div class="flex justify-end gap-2 mt-6 pt-3 border-t border-gray-100">
          <button @click="showSnapshotDialog = false"
                  class="px-4 py-2 text-sm border rounded-lg hover:bg-gray-100 transition">Cancel
          </button>
          <button @click="addSnapshot" :disabled="snapshotLoading"
                  class="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">Save
            Snapshot
          </button>
        </div>
      </div>
    </div>

    <!-- 訊息提示 Snackbar -->
    <div v-if="snackbar.show" class="fixed top-5 right-5 z-50 px-4 py-3 rounded-lg shadow-lg text-white text-sm" :class="snackbar.color === 'success' ? 'bg-green-600' : 'bg-red-600'">
      {{ snackbar.message }}
    </div>
  </div>
</template>

<style scoped>

</style>
