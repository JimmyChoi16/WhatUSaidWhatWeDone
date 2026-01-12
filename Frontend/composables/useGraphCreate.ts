import { EdgeMouseEvent, NodeMouseEvent, useVueFlow, type Connection, type Edge, type Node } from '@vue-flow/core';
import { computed, ref } from 'vue';
import { useAuth } from './useAuth';
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050';

type EditorNodeData = {
  title: string;
  nodeType: string;
  color: string;
  border: string;
  background: string;
  width?: number;
  height?: number;
};

export const useGraphCreate = () => {
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
    event.preventDefault();
    const type = event.dataTransfer?.getData('application/vueflow');
    if (!type) return;

    const target = event.currentTarget as HTMLElement;
    const bounds = target.getBoundingClientRect();
    const position = project
      ? project({ x: event.clientX - bounds.left, y: event.clientY - bounds.top })
      : { x: event.clientX - bounds.left, y: event.clientY - bounds.top };

    nodes.value = [
      ...nodes.value,
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

const onConnect = (c: Connection) => {
  if (!c.source || !c.target) return

  //防止重复边
  const exists = edges.value.some(e => e.source === c.source && e.target === c.target)
  if (exists) return

  edges.value = [
    ...edges.value,
    {
      id: `edge-${edgeId++}`,
      source: c.source,
      target: c.target,
      type: defaultEdgeType.value,
      style: { stroke: defaultEdgeColor.value, strokeWidth: 2 },
    },
  ]
  console.log('edges after add:', edges.value)
}


  const onNodeClick = ({ node }: NodeMouseEvent) => {
    selectedNodeId.value = node.id;
    selectedEdgeId.value = null;
  };

  const onEdgeClick = ({ edge }: EdgeMouseEvent) => {
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
    const { accessToken } = useAuth()

    if (!accessToken.value) {
      saveStatus.value = 'Please sign in before saving.'
      throw new Error('Please sign in before saving.')
    }

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
      const response = await fetch(`${API_BASE}/api/graphs`, {
        method: 'POST',
        headers: 
        {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken.value}`,
        },
        body: JSON.stringify(payload),
      });
      const text = await response.text()

      if (!response.ok) {
        throw new Error(`Request failed (${response.status}): ${text}`)
      }

      saveStatus.value = 'Saved.';
    } catch (error) {
      saveStatus.value = 'Save failed. Check the API endpoint.';
      console.error(error);
    }
  };

  return {
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
  };
};
