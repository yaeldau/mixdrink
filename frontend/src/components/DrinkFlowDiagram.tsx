import { useEffect, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Position,
} from '@xyflow/react';
import type { Node, Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useSessionStore } from '../stores/sessionStore';

// Custom node component for consumed drinks
function DrinkNode({ data }: { data: any }) {
  const getCategoryColor = (category: string | undefined): string => {
    const colors: Record<string, string> = {
      spirit: 'bg-amber-500',
      cocktail: 'bg-purple-500',
      wine: 'bg-rose-500',
      beer: 'bg-yellow-500',
      liqueur: 'bg-pink-500',
    };
    return colors[category?.toLowerCase() || ''] || 'bg-gray-500';
  };

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg shadow-lg min-w-[200px]">
      {/* Header with order number */}
      <div className={`${getCategoryColor(data.category)} text-white px-3 py-2 rounded-t-md`}>
        <div className="flex items-center justify-between">
          <span className="font-bold text-sm">Drink #{data.order}</span>
          <span className="text-xs opacity-90">{data.abv}% ABV</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-3">
        <h3 className="font-semibold text-sm mb-1">{data.name}</h3>
        <p className="text-xs text-gray-600 capitalize mb-2">{data.subcategory}</p>
        {data.time && (
          <p className="text-xs text-gray-500">{data.time}</p>
        )}
        {data.notes && (
          <p className="text-xs text-gray-700 mt-2 italic">"{data.notes}"</p>
        )}
      </div>
    </div>
  );
}

const nodeTypes = {
  drinkNode: DrinkNode,
};

export function DrinkFlowDiagram() {
  const { consumedDrinks, currentSession } = useSessionStore();
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  // Convert consumed drinks to ReactFlow nodes and edges
  useEffect(() => {
    if (!consumedDrinks || consumedDrinks.length === 0) {
      setNodes([]);
      setEdges([]);
      return;
    }

    // Create nodes from consumed drinks
    const newNodes: Node[] = consumedDrinks.map((consumedDrink, index) => {
      const drink = consumedDrink.drink;
      if (!drink) return null;

      // Calculate position (horizontal layout, left to right)
      const xPosition = index * 300;
      const yPosition = 100;

      // Format time
      const consumedTime = new Date(consumedDrink.consumed_at);
      const timeString = consumedTime.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      });

      return {
        id: `drink-${consumedDrink.id}`,
        type: 'drinkNode',
        position: { x: xPosition, y: yPosition },
        data: {
          order: consumedDrink.drink_order,
          name: drink.name,
          category: drink.category,
          subcategory: drink.subcategory,
          abv: drink.alcohol_content,
          time: timeString,
          notes: consumedDrink.notes,
        },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
      };
    }).filter(Boolean) as Node[];

    // Create edges connecting the drinks in order
    const newEdges: Edge[] = [];
    for (let i = 0; i < newNodes.length - 1; i++) {
      newEdges.push({
        id: `edge-${i}`,
        source: newNodes[i].id,
        target: newNodes[i + 1].id,
        animated: true,
        style: { stroke: '#94a3b8', strokeWidth: 2 },
      });
    }

    setNodes(newNodes);
    setEdges(newEdges);
  }, [consumedDrinks, setNodes, setEdges]);

  // Calculate session stats
  const sessionStats = useMemo(() => {
    if (!consumedDrinks || consumedDrinks.length === 0) {
      return null;
    }

    const totalDrinks = consumedDrinks.length;
    const totalAlcohol = consumedDrinks.reduce((sum, cd) => {
      return sum + (cd.drink?.alcohol_content || 0);
    }, 0);
    const avgAlcohol = totalAlcohol / totalDrinks;

    // Calculate session duration
    let duration = 0;
    if (currentSession && currentSession.started_at) {
      const start = new Date(currentSession.started_at);
      const end = currentSession.ended_at ? new Date(currentSession.ended_at) : new Date();
      duration = Math.floor((end.getTime() - start.getTime()) / (1000 * 60)); // minutes
    }

    return {
      totalDrinks,
      avgAlcohol: avgAlcohol.toFixed(1),
      duration,
    };
  }, [consumedDrinks, currentSession]);

  // Empty state
  if (!consumedDrinks || consumedDrinks.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-gray-50">
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No Drinks Yet
          </h3>
          <p className="text-gray-500 text-sm mb-4">
            Add a drink from the library to start your session
          </p>
          <div className="inline-block p-4 bg-white rounded-lg border-2 border-dashed border-gray-300">
            <svg
              className="w-16 h-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full relative">
      {/* Session Stats Header */}
      {sessionStats && (
        <div className="absolute top-4 left-4 z-10 bg-white/95 backdrop-blur-sm border border-gray-200 rounded-lg shadow-md p-3">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Session Stats</h3>
          <div className="space-y-1 text-xs text-gray-600">
            <div className="flex items-center gap-2">
              <span className="font-medium">Drinks:</span>
              <span>{sessionStats.totalDrinks}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-medium">Avg ABV:</span>
              <span>{sessionStats.avgAlcohol}%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-medium">Duration:</span>
              <span>{sessionStats.duration} min</span>
            </div>
          </div>
        </div>
      )}

      {/* ReactFlow Canvas */}
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{
          padding: 0.2,
          minZoom: 0.5,
          maxZoom: 1.5,
        }}
        minZoom={0.1}
        maxZoom={2}
        defaultEdgeOptions={{
          animated: true,
        }}
      >
        <Background color="#e2e8f0" gap={16} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            const category = (node.data?.category as string | undefined)?.toLowerCase();
            const colors: Record<string, string> = {
              spirit: '#f59e0b',
              cocktail: '#a855f7',
              wine: '#f43f5e',
              beer: '#eab308',
              liqueur: '#ec4899',
            };
            return colors[category || ''] || '#9ca3af';
          }}
          maskColor="rgba(0, 0, 0, 0.1)"
        />
      </ReactFlow>
    </div>
  );
}
