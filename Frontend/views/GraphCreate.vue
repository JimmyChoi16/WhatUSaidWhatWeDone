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
              <Handle type="target" :position="Position.Left" />
              <div class="graph-create__node-type">{{ data.nodeType }}</div>
              <div class="graph-create__node-title">{{ data.title }}</div>
              <Handle type="source" :position="Position.Right" />
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
import { Handle, Position, VueFlow } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';
import { useGraphCreate } from '../composables/useGraphCreate';

const {
  graphName,
  defaultEdgeType,
  defaultEdgeColor,
  saveStatus,
  palette,
  nodes,
  edges,
  selectedNode,
  selectedEdge,
  edgeStrokeColor,
  onDragStart,
  onDragOver,
  onDrop,
  onConnect,
  onNodeClick,
  onEdgeClick,
  clearSelection,
  updateNodeField,
  updateNodeNumber,
  updateEdgeLabel,
  updateEdgeColor,
  centerView,
  saveGraph,
} = useGraphCreate();
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
