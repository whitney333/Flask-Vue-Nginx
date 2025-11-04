<script setup>
import { ref, onMounted, watch } from "vue";
import { AgGridVue } from "ag-grid-vue3";
import axios from "axios";
import InstagramIcon from "@/assets/icons/instagram.svg";
import TikTokIcon from "@/assets/icons/tiktok.svg";
import XiaohongshuIcon from "@/assets/icons/xiaohongshu.svg";
import BilibiliIcon from "@/assets/icons/bilibili.svg";
import YoutubeIcon from "@/assets/icons/youtube.svg"
import { useUserStore } from "@/stores/user.js";


const props = defineProps({
  campaignId: {
    type: String,
    required: true,
  },
});

const userStore = useUserStore()
const rowData = ref([])

const kolAccountRenderer = (params) => {
  // add link to account
  const account = params.value || "";
  const platform = params.data.platform || "Instagram"; // fallback Instagram
  const username = account.startsWith("@") ? account.slice(1) : account;

  let url = "#";
  switch (platform.toLowerCase()) {
    case "instagram":
      url = `https://www.instagram.com/${username}`;
      break;
    case "tiktok":
      url = `https://www.tiktok.com/@${username}`;
      break;
    case "xiaohongshu":
      url = "#";
      break;
    case "bilibili":
      url = "#";
      break;
    case "youtube":
      url = `https://www.youtube.com/${username}`
      break;
    case "offline":
      url = "#";
      break;
    default:
      url = "#";
  }

  return `<a href="${url}" target="_blank" style="color:#1a73e8;text-decoration:underline;">${account}</a>`;
};

const platformRenderer = (params) => {
   const platform = params.value?.toLowerCase();
  let iconPath = "";
  let name = "";

  switch (platform) {
    case "instagram":
      iconPath = InstagramIcon;
      name = "Instagram";
      break;
    case "tiktok":
      iconPath = TikTokIcon;
      name = "TikTok";
      break;
    case "youtube":
      iconPath = YoutubeIcon;
      name = "YouTube";
      break;
    case "xiaohongshu":
      iconPath = XiaohongshuIcon;
      name = "Xiaohongshu";
      break;
    case "bilibili":
      iconPath = BilibiliIcon;
      name = "Bilibili";
      break;
    case "offline":
      iconPath = Shapes;
      name = "Offline";
      break;
    default:
      iconPath = Globe;
      name = platform || "Unknown";
  }

  return `
    <div class="platform-icon" title="${name}">
      <img src="${iconPath}" alt="${name}" class="platform-img" />
    </div>
  `;
};

const hashtagRenderer = (params) => {
  const hashtags = params.value || [];
  if (!Array.isArray(hashtags) || hashtags.length === 0) return "";

  const container = document.createElement("div");
  container.classList.add("hashtag-container");

  // limit init number
  let expanded = false;
  const MAX_VISIBLE = 5;

  // chips container
  const chipWrapper = document.createElement("div");
  chipWrapper.classList.add("hashtag-wrapper");
  container.appendChild(chipWrapper);

  const renderChips = () => {
    chipWrapper.innerHTML = "";
    const displayTags = expanded ? hashtags : hashtags.slice(0, MAX_VISIBLE);
    displayTags.forEach((tag) => {
      const chip = document.createElement("span");
      chip.classList.add("hashtag-chip");
      chip.textContent = tag;
      chipWrapper.appendChild(chip);
    });
  };

  renderChips();

  // if hashtags number are greater than MAX_VISIBLE > Show more
  if (hashtags.length > MAX_VISIBLE) {
    const toggleButton = document.createElement("button");
    toggleButton.textContent = "Show more";
    toggleButton.classList.add("hashtag-toggle");

    toggleButton.addEventListener("click", (e) => {
      e.stopPropagation();
      expanded = !expanded;
      toggleButton.textContent = expanded ? "Show less" : "Show more";
      renderChips();

      // recalculate height
      const rowNode = params.node;
      if (params.api && rowNode) {
        setTimeout(() => params.api.resetRowHeights(), 50);
      }
    });

    container.appendChild(toggleButton);
  }

  return container;
};

// Column Definitions: Defines the columns to be displayed.
const colDefs = ref([
    {field: "artist", headerName: "Artist"},
    {field: "content", headerName: "Content"},
    {
      field: "kol_account",
      headerName: "KOL Account",
      cellRenderer: kolAccountRenderer,
      pinned: "left"
    },
    {
      field: "platform",
      headerName: "Platform",
      pinned: "left"
    },
    {field: "status", headerName: "Status"},
    {field: "target_country", headerName: "Target Country"},
    {field: "type", headerName: "Type"},
    {field: "cost", headerName: "Cost"},
    {field: "post_created_at", headerName: "Post Created"},
    {field: "reach", headerName: "Reach"},
    {field: "reaction", headerName: "Reaction"},
    {field: "engagement", headerName: "Engagement"},
    {field: "hashtag_reach", headerName: "Hashtag Reach"},
    {field: "cost_per_reach", headerName: "Cost Per Reach"},
    {field: "cost_per_view", headerName: "Cost Per View"},
    {field: "one_hour_view", headerName: "1 HR View"},
    {field: "twentyfour_hour_view", headerName: "24 HR View"},
    {field: "latest_view", headerName: "Latest View"},
    {field: "used_hashtag", headerName: "Used Hashtags",
      cellRenderer: hashtagRenderer,
      autoHeight: true,
      cellStyle: {
        whiteSpace: "normal",
      },
      minWidth: 400,
      flex: 1,
    },
]);

const defaultColDef = ref({
  sortable: true,
  filter: true,
  resizable: true,
  flex: 0,
  minWidth: 50,
});

const sideBar = {
  // enterprise version only
  // open column tool
  toolPanels: [
    {
      id: 'columns',
      labelDefault: 'Columns',
      toolPanel: 'agColumnsToolPanel',
    },
  ],
  defaultToolPanel: "columns",
};

const fetchData = async (campaignId) => {
  if (!campaignId) return;
  try {
    const res = await axios.get(
        `/api/campaign/v1/detail/${campaignId}`,
        {headers: {
            "Authorization": `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
          }}
    )

    const data = res.data.data.post || []
    // console.log("cp: ", data)
    rowData.value = data.map(item => ({
      artist: item.artist,
      content: item.content,
      kol_account: item.kol_account,
      platform: item.platform,
      status: item.status,
      target_country: item.target_country,
      type: item.type,
      cost: item.cost,
      post_created_at: item.post_created_at,
      reach: item.reach,
      reaction: item.reaction,
      engagement: item.engagement,
      hashtag_reach: item.hashtag_reach,
      cost_per_reach: item.cost_per_reach,
      cost_per_view: item.cost_per_view,
      one_hour_view: item.one_hour_view,
      twentyfour_hour_view: item.twentyfour_hour_view,
      latest_view: item.latest_view,
      used_hashtag: item.used_hashtag,
    }))
  } catch (err) {
    console.error("Failed to fetch campaign data:", err);
    rowData.value = [];
  }
}

onMounted(() =>
    fetchData(props.campaignId)
);

watch(() => props.campaignId, (newId) => {
  if (newId) fetchData(newId);
});

</script>

<template>
   <div class="ag-theme-quartz" style="width: 100%; height: 500px; overflow: auto;">
     <AgGridVue
         style="width: 100%; height: 100%;"
         :rowData="rowData"
         :columnDefs="colDefs"
         :defaultColDef="defaultColDef"
         :domLayout="'normal'"
         :suppressHorizontalScroll="false"
         :suppressColumnVirtualisation="false"
     ></AgGridVue>
  </div>
</template>

<style scoped>
.hashtag-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  white-space: normal;
}

.hashtag-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.hashtag-chip {
  background-color: #f0e6ff;
  color: #5b21b6;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 12px;
  line-height: 1.4;
}

.hashtag-toggle {
  background: none;
  border: none;
  color: #4b00ff;
  font-size: 12px;
  cursor: pointer;
  padding: 0;
  margin-top: 2px;
  text-decoration: underline;
}

.hashtag-toggle:hover {
  color: #2a00a5;
}

</style>