<template>
  <div class="graph-hub">
    <div class="graph-hub__header">
      <div>
        <div class="graph-hub__eyebrow">Relationship Studio</div>
        <h1 class="graph-hub__title">My Relationship Graphs</h1>
        <p class="graph-hub__subtitle">Browse the networks you have saved and open one to explore.</p>
      </div>
      <RouterLink class="graph-hub__cta" to="/graph/create">Create new</RouterLink>
    </div>

    <div class="graph-hub__body">
      <aside class="graph-hub__sidebar">
        <div class="graph-hub__sidebar-title">Your graphs</div>
        <div v-if="!accessToken" class="graph-hub__state">Sign in to load your saved graphs.</div>
        <div v-else-if="listLoading" class="graph-hub__state">Loading graphs...</div>
        <div v-else-if="listError" class="graph-hub__state graph-hub__state--error">
          {{ listError }}
        </div>
        <div v-else-if="graphs.length === 0" class="graph-hub__state">
          No graphs yet. Try creating your first map.
        </div>
        <ul v-else class="graph-hub__list">
          <li v-for="graph in graphs" :key="graph.id">
            <button
              class="graph-hub__list-item"
              :class="{ 'graph-hub__list-item--active': graph.id === selectedGraphId }"
              type="button"
              @click="selectGraph(graph.id)"
            >
              <div class="graph-hub__list-name">{{ graph.name }}</div>
              <div class="graph-hub__list-meta">
                Updated {{ formatDate(graph.updated_at) }}
              </div>
            </button>
          </li>
        </ul>
      </aside>

      <section class="graph-hub__canvas">
        <div v-if="!accessToken" class="graph-hub__placeholder">
          Sign in to see the relationship networks you have saved.
        </div>
        <div v-else-if="detailLoading" class="graph-hub__placeholder">Loading graph...</div>
        <div v-else-if="detailError" class="graph-hub__placeholder graph-hub__placeholder--error">
          {{ detailError }}
        </div>
        <div v-else-if="resolvedNodes.length > 0" class="graph-hub__flow">
          <GraphFlow :nodes="resolvedNodes" :edges="resolvedEdges" />
        </div>
        <div v-else class="graph-hub__placeholder">
          Select a relationship graph from the list to visualize it.
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { RouterLink } from 'vue-router';
import GraphFlow, { type GraphEdge, type GraphNode } from '../components/GraphFlow.vue';
import { useAuth } from '../composables/useAuth';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050';
const DEFAULT_EDGE_COLOR = '#2563eb';

type GraphSummary = {
  id: string;
  name: string;
  visibility: string;
  created_at: string;
  updated_at: string;
};

type GraphDetailNode = {
  id: string;
  title: string;
  avatar_url?: string | null;
  position?: { x: number; y: number };
};

type GraphDetailEdge = {
  id: string;
  source: string;
  target: string;
  type?: string | null;
  style?: { stroke?: string } | null;
};

const { accessToken, initAuth } = useAuth();
const graphs = ref<GraphSummary[]>([]);
const selectedGraphId = ref<string | null>(null);
const graphNodes = ref<GraphDetailNode[]>([]);
const graphEdges = ref<GraphDetailEdge[]>([]);
const listLoading = ref(false);
const detailLoading = ref(false);
const listError = ref('');
const detailError = ref('');

const resolvedNodes = computed<GraphNode[]>(() =>
  graphNodes.value.map((node) => ({
    id: node.id,
    x: node.position?.x ?? 0,
    y: node.position?.y ?? 0,
    name: node.title,
    avatarUrl: node.avatar_url || undefined,
  }))
);

const resolvedEdges = computed<GraphEdge[]>(() =>
  graphEdges.value.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    type: edge.type || 'smoothstep',
    color: edge.style?.stroke || DEFAULT_EDGE_COLOR,
  }))
);

const formatDate = (value: string) =>
  new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

const fetchGraphs = async () => {
  if (!accessToken.value) return;
  listLoading.value = true;
  listError.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/graphs/mine`, {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    });
    if (!res.ok) {
      throw new Error(`Request failed (${res.status})`);
    }
    graphs.value = await res.json();
    if (graphs.value.length > 0 && !selectedGraphId.value) {
      await selectGraph(graphs.value[0].id);
    }
  } catch (error) {
    listError.value = error instanceof Error ? error.message : 'Failed to load graphs.';
  } finally {
    listLoading.value = false;
  }
};

const fetchGraphDetail = async (graphId: string) => {
  if (!accessToken.value) return;
  detailLoading.value = true;
  detailError.value = '';
  try {
    const res = await fetch(`${API_BASE}/api/graphs/${graphId}`, {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    });
    if (!res.ok) {
      throw new Error(`Request failed (${res.status})`);
    }
    const data = await res.json();
    graphNodes.value = data.nodes ?? [];
    graphEdges.value = data.edges ?? [];
  } catch (error) {
    detailError.value = error instanceof Error ? error.message : 'Failed to load graph.';
    graphNodes.value = [];
    graphEdges.value = [];
  } finally {
    detailLoading.value = false;
  }
};

const selectGraph = async (graphId: string) => {
  if (selectedGraphId.value === graphId) return;
  selectedGraphId.value = graphId;
  await fetchGraphDetail(graphId);
};

onMounted(async () => {
  await initAuth();
  if (accessToken.value) {
    await fetchGraphs();
  }
});

watch(accessToken, async (value) => {
  if (!value) {
    graphs.value = [];
    selectedGraphId.value = null;
    graphNodes.value = [];
    graphEdges.value = [];
    return;
  }
  await fetchGraphs();
});
</script>

<style scoped>
.graph-hub {
  min-height: 100vh;
  padding: 72px 32px 40px;
  background: radial-gradient(circle at top right, rgba(14, 165, 233, 0.2), transparent 55%),
    radial-gradient(circle at 10% 80%, rgba(244, 114, 182, 0.2), transparent 50%),
    #f8fafc;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', sans-serif;
  color: #0f172a;
}

.graph-hub__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto 24px;
}

.graph-hub__eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 11px;
  color: #475569;
  margin-bottom: 8px;
}

.graph-hub__title {
  font-size: 28px;
  margin: 0 0 6px;
}

.graph-hub__subtitle {
  margin: 0;
  color: #475569;
  max-width: 420px;
}

.graph-hub__cta {
  background: #0f172a;
  color: #f8fafc;
  padding: 10px 18px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2);
}

.graph-hub__body {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: stretch;
}

.graph-hub__sidebar {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.1);
  backdrop-filter: blur(12px);
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.graph-hub__sidebar-title {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #64748b;
}

.graph-hub__state {
  font-size: 13px;
  color: #475569;
  padding: 12px;
  border-radius: 12px;
  background: rgba(248, 250, 252, 0.8);
  border: 1px dashed #e2e8f0;
}

.graph-hub__state--error {
  border-color: rgba(248, 113, 113, 0.6);
  color: #b91c1c;
  background: rgba(254, 226, 226, 0.5);
}

.graph-hub__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
}

.graph-hub__list-item {
  border: 1px solid transparent;
  padding: 12px;
  border-radius: 14px;
  text-align: left;
  background: #ffffff;
  cursor: pointer;
  transition: border-color 0.2s ease, transform 0.2s ease;
  display: grid;
  gap: 6px;
}

.graph-hub__list-item:hover {
  border-color: rgba(15, 23, 42, 0.12);
  transform: translateY(-1px);
}

.graph-hub__list-item--active {
  border-color: rgba(37, 99, 235, 0.5);
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.15);
}

.graph-hub__list-name {
  font-weight: 600;
  font-size: 14px;
}

.graph-hub__list-meta {
  font-size: 12px;
  color: #64748b;
}

.graph-hub__canvas {
  background: #ffffff;
  border-radius: 22px;
  box-shadow: 0 18px 35px rgba(15, 23, 42, 0.12);
  min-height: 60vh;
  overflow: hidden;
  position: relative;
  display: flex;
}

.graph-hub__flow {
  flex: 1;
  min-height: 60vh;
}

.graph-hub__placeholder {
  margin: auto;
  text-align: center;
  font-size: 14px;
  color: #64748b;
  max-width: 320px;
  padding: 24px;
}

.graph-hub__placeholder--error {
  color: #b91c1c;
}

@media (max-width: 900px) {
  .graph-hub__header {
    flex-direction: column;
    align-items: flex-start;
  }

  .graph-hub__body {
    grid-template-columns: 1fr;
  }

  .graph-hub__sidebar {
    min-height: auto;
  }

  .graph-hub__canvas {
    min-height: 55vh;
  }
}
</style>
