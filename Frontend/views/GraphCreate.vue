<template>
  <div class="graph-create">
    <div class="graph-create__header">
      <div class="graph-create__title">
        <span class="graph-create__badge">Graph Studio</span>
        <input
          v-model="graphName"
          class="graph-create__name"
          type="text"
          placeholder="Untitled graph"
        />
      </div>
      <div class="graph-create__actions">
        <button class="graph-create__button" type="button" @click="centerView">Center view</button>
        <button class="graph-create__button graph-create__button--primary" type="button" @click="saveGraph">
          Save layout
        </button>
      </div>
    </div>

    <div class="graph-create__body">
      <aside class="graph-create__panel">
        <h3 class="graph-create__panel-title">Nodes</h3>
        <div class="graph-create__palette">
          <div
            v-for="item in palette"
            :key="item.type"
            class="graph-create__palette-item"
            draggable="true"
            @dragstart="onDragStart($event, item.type)"
          >
            <span class="graph-create__dot" :style="{ background: item.color }"></span>
            <div>
              <div class="graph-create__palette-name">{{ item.label }}</div>
              <div class="graph-create__palette-sub">{{ item.hint }}</div>
            </div>
          </div>
        </div>

        <div class="graph-create__panel-section">
          <h3 class="graph-create__panel-title">Canvas</h3>
          <label class="graph-create__field">
            <span>Edge style</span>
            <select v-model="defaultEdgeType">
              <option value="smoothstep">Smooth</option>
              <option value="step">Step</option>
              <option value="straight">Straight</option>
            </select>
          </label>
          <label class="graph-create__field">
            <span>Edge color</span>
            <input v-model="defaultEdgeColor" type="color" />
          </label>
        </div>
      </aside>

      <div class="graph-create__canvas" @drop="onDrop" @dragover="onDragOver">
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :fit-view="true"
          :default-edge-options="{
            type: defaultEdgeType,
            style: { stroke: defaultEdgeColor, strokeWidth: 2 },
          }"
          
          @connect="onConnect"
          @node-click="onNodeClick"
          @edge-click="onEdgeClick"
          @pane-click="clearSelection"
        >
          <template #node-editor="{ data }">
            <div
              class="graph-create__node"
              :style="{
                background: data.background,
                borderColor: data.border,
                color: data.color,
                width: data.width ? data.width + 'px' : '160px',
                height: data.height ? data.height + 'px' : 'auto',
              }"
            >
              <div class="graph-create__node-type">{{ data.nodeType }}</div>
              <div class="graph-create__node-title">{{ data.title }}</div>
            </div>
          </template>
        </VueFlow>
      </div>

      <aside class="graph-create__panel">
        <h3 class="graph-create__panel-title">Inspector</h3>
        <div v-if="selectedNode" class="graph-create__panel-section">
          <div class="graph-create__panel-subtitle">Node</div>
          <label class="graph-create__field">
            <span>Title</span>
            <input
              type="text"
              :value="selectedNode.data.title"
              @input="updateNodeField('title', ($event.target as HTMLInputElement).value)"
            />
          </label>
          <label class="graph-create__field">
            <span>Type</span>
            <select
              :value="selectedNode.data.nodeType"
              @change="updateNodeField('nodeType', ($event.target as HTMLSelectElement).value)"
            >
              <option value="person">person</option>
              <option value="org">org</option>
              <option value="place">place</option>
              <option value="event">event</option>
              <option value="custom">custom</option>
            </select>
          </label>
          <label class="graph-create__field">
            <span>Width</span>
            <input
              type="number"
              min="80"
              :value="selectedNode.data.width"
              @input="updateNodeNumber('width', ($event.target as HTMLInputElement).value)"
            />
          </label>
          <label class="graph-create__field">
            <span>Height</span>
            <input
              type="number"
              min="60"
              :value="selectedNode.data.height"
              @input="updateNodeNumber('height', ($event.target as HTMLInputElement).value)"
            />
          </label>
          <div class="graph-create__color-row">
            <label class="graph-create__field graph-create__field--inline">
              <span>Text</span>
              <input
                type="color"
                :value="selectedNode.data.color"
                @input="updateNodeField('color', ($event.target as HTMLInputElement).value)"
              />
            </label>
            <label class="graph-create__field graph-create__field--inline">
              <span>Border</span>
              <input
                type="color"
                :value="selectedNode.data.border"
                @input="updateNodeField('border', ($event.target as HTMLInputElement).value)"
              />
            </label>
            <label class="graph-create__field graph-create__field--inline">
              <span>Fill</span>
              <input
                type="color"
                :value="selectedNode.data.background"
                @input="updateNodeField('background', ($event.target as HTMLInputElement).value)"
              />
            </label>
          </div>
        </div>

        <div v-else-if="selectedEdge" class="graph-create__panel-section">
          <div class="graph-create__panel-subtitle">Edge</div>
          <label class="graph-create__field">
            <span>Label</span>
            <input
              type="text"
              :value="selectedEdge.label || ''"
              @input="updateEdgeLabel(($event.target as HTMLInputElement).value)"
            />
          </label>
          <label class="graph-create__field">
            <span>Color</span>
            <input
              type="color"
              :value="edgeStrokeColor"
              @input="updateEdgeColor(($event.target as HTMLInputElement).value)"
            />
          </label>
        </div>

        <div v-else class="graph-create__panel-section graph-create__panel-empty">
          Select a node or edge to edit its style.
        </div>

        <div class="graph-create__status" v-if="saveStatus">{{ saveStatus }}</div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { EdgeMouseEvent, NodeMouseEvent, useVueFlow, VueFlow, type Connection, type Edge, type Node } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';
import { computed, ref } from 'vue';

type EditorNodeData = {
  title: string;
  nodeType: string;
  color: string;
  border: string;
  background: string;
  width?: number;
  height?: number;
};

const { project, fitView } = useVueFlow();

const graphName = ref('Relationship map');
const defaultEdgeType = ref<'smoothstep' | 'step' | 'straight'>('smoothstep');
const defaultEdgeColor = ref('#2563eb');
const saveStatus = ref('');

const palette = [
  { type: 'person', label: 'Person', hint: 'Founders, friends, teammates', color: '#38bdf8' },
  { type: 'org', label: 'Organization', hint: 'Companies, teams, groups', color: '#22c55e' },
  { type: 'place', label: 'Place', hint: 'Cities, campuses, hubs', color: '#f97316' },
  { type: 'event', label: 'Event', hint: 'Launches, trips, milestones', color: '#a855f7' },
  { type: 'custom', label: 'Custom', hint: 'Anything else', color: '#f43f5e' },
];

const nodes = ref<Node<EditorNodeData>[]>([
  {
    id: 'seed-1',
    type: 'editor',
    position: { x: 80, y: 120 },
    data: {
      title: 'Michael',
      nodeType: 'person',
      color: '#0f172a',
      border: '#0f172a',
      background: '#fef3c7',
    },
  },
  {
    id: 'seed-2',
    type: 'editor',
    position: { x: 380, y: 320 },
    data: {
      title: 'HSBC',
      nodeType: 'org',
      color: '#0f172a',
      border: '#1d4ed8',
      background: '#dbeafe',
    },
  },
]);

const edges = ref<Edge[]>([]);
let nodeId = 3;
let edgeId = 1;

const selectedNodeId = ref<string | null>(null);
const selectedEdgeId = ref<string | null>(null);

const selectedNode = computed(() => nodes.value.find((node) => node.id === selectedNodeId.value));
const selectedEdge = computed(() => edges.value.find((edge) => edge.id === selectedEdgeId.value));
const edgeStrokeColor = computed(() => {
  if (!selectedEdge.value) return defaultEdgeColor.value;
  const style = selectedEdge.value.style;
  if (style && typeof style === 'object' && 'stroke' in style) {
    return String((style as Record<string, string | number>).stroke);
  }
  return defaultEdgeColor.value;
});

const onDragStart = (event: DragEvent, type: string) => {
  event.dataTransfer?.setData('application/vueflow', type);
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move';
  }
};

const onDragOver = (event: DragEvent) => {
  event.preventDefault();
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move';
  }
};

const onDrop = (event: DragEvent) => {
  event.preventDefault(); // Prevent default behavior 允许drop
  const type = event.dataTransfer?.getData('application/vueflow');
  if (!type) return;
  //找到 drop 发生在哪个 DOM 上，并获取它的位置与尺寸
  const target = event.currentTarget as HTMLElement;
  const bounds = target.getBoundingClientRect();
  //计算新节点应该放在画布的什么坐标
  const position = project
    ? project({ x: event.clientX - bounds.left, y: event.clientY - bounds.top })
    : { x: event.clientX - bounds.left, y: event.clientY - bounds.top };
 //往 nodes 里加一个新节点（Vue Flow 就会渲染它）
  nodes.value = [
    ...nodes.value, //把原来数组里的所有节点，原封不动地拷贝一份，然后在后面加新节点
    {
      id: `node-${nodeId++}`,
      type: 'editor',
      position,
      data: {
        title: `${type} node`,
        nodeType: type,
        color: '#0f172a',
        border: '#111827',
        background: '#ffffff',
      },
    },
  ];
};

const onConnect = (connection: Connection) => {
  edges.value = [
    ...edges.value,
    {
      id: `edge-${edgeId++}`,
      source: connection.source ?? '',
      target: connection.target ?? '',
      type: defaultEdgeType.value,
      style: { stroke: defaultEdgeColor.value, strokeWidth: 2 },
    },
  ];
};

const onNodeClick = ({ node, event }: NodeMouseEvent) => {
  selectedNodeId.value = node.id
  selectedEdgeId.value = null
}

const onEdgeClick = ({edge, event}: EdgeMouseEvent) => {
  selectedEdgeId.value = edge.id;
  selectedNodeId.value = null;
};

const clearSelection = () => {
  selectedNodeId.value = null;
  selectedEdgeId.value = null;
};

const updateNodeField = (field: keyof EditorNodeData, value: string) => {
  if (!selectedNode.value) return;
  nodes.value = nodes.value.map((node) =>
    node.id === selectedNode.value?.id
      ? { ...node, data: { ...node.data, [field]: value } }
      : node
  );
};

const updateNodeNumber = (field: 'width' | 'height', rawValue: string) => {
  if (!selectedNode.value) return;
  const value = rawValue ? Number(rawValue) : undefined;
  nodes.value = nodes.value.map((node) =>
    node.id === selectedNode.value?.id
      ? { ...node, data: { ...node.data, [field]: value } }
      : node
  );
};

const updateEdgeLabel = (value: string) => {
  if (!selectedEdge.value) return;
  edges.value = edges.value.map((edge) =>
    edge.id === selectedEdge.value?.id ? { ...edge, label: value } : edge
  );
};

const updateEdgeColor = (value: string) => {
  if (!selectedEdge.value) return;
  edges.value = edges.value.map((edge) =>
    edge.id === selectedEdge.value?.id
      ? { ...edge, style: { ...(edge.style ?? {}), stroke: value } }
      : edge
  );
};

const centerView = () => {
  fitView({ padding: 0.2 });
};

const saveGraph = async () => {
  saveStatus.value = 'Saving...';
  const payload = {
    graph: {
      name: graphName.value,
      visibility: 'private',
    },
    nodes: nodes.value.map((node) => ({
      id: node.id,
      title: node.data.title,
      node_type: node.data.nodeType,
      position: node.position,
      style: {
        color: node.data.color,
        border: node.data.border,
        background: node.data.background,
        width: node.data.width,
        height: node.data.height,
      },
    })),
    edges: edges.value.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      type: edge.type,
      style: edge.style,
    })),
  };

  try {
    const response = await fetch('/api/graphs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Request failed (${response.status})`);
    }

    saveStatus.value = 'Saved.';
  } catch (error) {
    saveStatus.value = 'Save failed. Check the API endpoint.';
    console.error(error);
  }
};
</script>

<style scoped>
.graph-create {
  min-height: 100vh;
  padding: 64px 32px 32px;
  box-sizing: border-box;
  background: radial-gradient(circle at top, rgba(59, 130, 246, 0.18), transparent 55%),
    radial-gradient(circle at 20% 80%, rgba(248, 113, 113, 0.2), transparent 50%),
    #f8fafc;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', sans-serif;
  color: #0f172a;
}

.graph-create__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
}

.graph-create__title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.graph-create__badge {
  padding: 6px 12px;
  border-radius: 999px;
  background: #0f172a;
  color: #f8fafc;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.graph-create__name {
  border: none;
  border-bottom: 2px solid #0f172a;
  background: transparent;
  font-size: 22px;
  font-weight: 600;
  padding: 4px 8px;
  min-width: 220px;
}

.graph-create__actions {
  display: flex;
  gap: 12px;
}

.graph-create__button {
  border: 1px solid #0f172a;
  background: #ffffff;
  padding: 10px 16px;
  border-radius: 999px;
  font-weight: 600;
  cursor: pointer;
}

.graph-create__button--primary {
  background: #0f172a;
  color: #f8fafc;
}

.graph-create__body {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr) 280px;
  gap: 20px;
  align-items: stretch;
}

.graph-create__panel {
  background: rgba(255, 255, 255, 0.92);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
}

.graph-create__panel-title {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 12px;
  color: #475569;
}

.graph-create__palette {
  display: grid;
  gap: 12px;
}

.graph-create__palette-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  cursor: grab;
}

.graph-create__palette-item:active {
  cursor: grabbing;
}

.graph-create__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 6px;
}

.graph-create__palette-name {
  font-weight: 600;
}

.graph-create__palette-sub {
  font-size: 12px;
  color: #64748b;
}

.graph-create__panel-section {
  margin-top: 20px;
  display: grid;
  gap: 12px;
}

.graph-create__panel-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
}

.graph-create__field {
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: #475569;
}

.graph-create__field input,
.graph-create__field select {
  border: 1px solid #cbd5f5;
  padding: 8px 10px;
  border-radius: 10px;
  background: #ffffff;
}

.graph-create__field--inline {
  flex: 1;
}

.graph-create__color-row {
  display: flex;
  gap: 10px;
}

.graph-create__canvas {
  border-radius: 18px;
  overflow: hidden;
  background: repeating-linear-gradient(
      90deg,
      rgba(148, 163, 184, 0.2) 0,
      rgba(148, 163, 184, 0.2) 1px,
      transparent 1px,
      transparent 20px
    ),
    repeating-linear-gradient(
      0deg,
      rgba(148, 163, 184, 0.2) 0,
      rgba(148, 163, 184, 0.2) 1px,
      transparent 1px,
      transparent 20px
    );
  min-height: 70vh;
}

.graph-create__node {
  border: 2px solid;
  border-radius: 14px;
  padding: 10px 14px;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 6px;
}

.graph-create__node-type {
  text-transform: uppercase;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: inherit;
}

.graph-create__node-title {
  font-weight: 700;
  font-size: 14px;
  color: inherit;
}

.graph-create__panel-empty {
  color: #64748b;
  font-size: 13px;
}

.graph-create__status {
  margin-top: 16px;
  font-size: 12px;
  color: #0f172a;
}

@media (max-width: 1024px) {
  .graph-create__body {
    grid-template-columns: 1fr;
  }

  .graph-create__panel {
    order: 1;
  }

  .graph-create__canvas {
    order: 0;
    min-height: 60vh;
  }
}
</style>
