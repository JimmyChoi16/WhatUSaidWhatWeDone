<template>
  <div style="height: 100%; width: 100%;">
    <VueFlow :nodes="flowNodes" :edges="flowEdges" :fit-view="true" style="height: 100%; width: 100%;">
      <template #node-custom="{ data }">
        <div
          style="
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 10px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
          "
        >
          <div
            style="
              width: 28px;
              height: 28px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              overflow: hidden;
              background: #e2e8f0;
              color: #0f172a;
              font-size: 12px;
              font-weight: 600;
            "
          >
            <img
              v-if="data.avatarUrl"
              :src="data.avatarUrl"
              alt="avatar"
              style="width: 100%; height: 100%; object-fit: cover;"
            />
            <span v-else>{{ data.initial }}</span>
          </div>
          <span style="font-size: 13px; color: #111827;">{{ data.name }}</span>
        </div>
      </template>
    </VueFlow>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { VueFlow, type Edge, type Node } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';

export type GraphNode = {
  id: string;
  x: number;
  y: number;
  name: string;
  avatarUrl?: string;
};

export type GraphEdge = {
  id: string;
  source: string;
  target: string;
  type?: string;
  color: string;
};

const props = defineProps<{ nodes: GraphNode[]; edges: GraphEdge[] }>();

const flowNodes = computed<Node[]>(() =>
  props.nodes.map((node) => ({
    id: node.id,
    type: 'custom',
    position: { x: node.x, y: node.y },
    data: {
      name: node.name,
      avatarUrl: node.avatarUrl,
      initial: node.name.trim().charAt(0).toUpperCase() || '?',
    },
  }))
);

const flowEdges = computed<Edge[]>(() =>
  props.edges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    type: edge.type,
    style: {
      stroke: edge.color,
    },
  }))
);
</script>
