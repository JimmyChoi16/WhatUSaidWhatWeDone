<template>
  <div style="height: 100vh; width: 100%; padding-top: 48px; box-sizing: border-box;">
    <div style="height: calc(100vh - 48px); width: 100%;">
      <GraphFlow :nodes="resolvedNodes" :edges="resolvedEdges" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import GraphFlow, { type GraphEdge, type GraphNode } from '../components/GraphFlow.vue';

const props = withDefaults(
  defineProps<{ nodes?: GraphNode[]; edges?: GraphEdge[] }>(),
  {
    nodes: () => [],
    edges: () => [],
  }
);

const demoNodes: GraphNode[] = [
  {
    id: '1',
    x: 0,
    y: 0,
    name: 'Alice',
    avatarUrl: 'https://i.pravatar.cc/60?img=1',
  },
  {
    id: '2',
    x: 220,
    y: 120,
    name: 'Bob',
    avatarUrl: 'https://i.pravatar.cc/60?img=2',
  },
  {
    id: '3',
    x: 0,
    y: 220,
    name: 'Clara',
    avatarUrl: 'https://i.pravatar.cc/60?img=3',
  },
];

const demoEdges: GraphEdge[] = [
  {
    id: 'e1-2',
    source: '1',
    target: '2',
    type: 'smoothstep',
    color: '#2563eb',
  },
  {
    id: 'e1-3',
    source: '1',
    target: '3',
    type: 'smoothstep',
    color: '#f97316',
  },
];

const resolvedNodes = computed(() => (props.nodes.length > 0 ? props.nodes : demoNodes));
const resolvedEdges = computed(() => (props.edges.length > 0 ? props.edges : demoEdges));
</script>
