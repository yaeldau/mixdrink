import { useSessionStore } from '../stores/sessionStore';
import { RotateCcw, Sparkles, Clock } from 'lucide-react';
import { useMemo } from 'react';

export function SessionControls() {
  const {
    currentSession,
    consumedDrinks,
    getRecommendations,
    resetSession,
    isLoading,
    isLoadingRecommendations,
  } = useSessionStore();

  // Calculate session duration
  const sessionDuration = useMemo(() => {
    if (!currentSession?.started_at) return '0m';

    const start = new Date(currentSession.started_at);
    const end = currentSession.ended_at ? new Date(currentSession.ended_at) : new Date();
    const durationMinutes = Math.floor((end.getTime() - start.getTime()) / (1000 * 60));

    if (durationMinutes < 60) {
      return `${durationMinutes}m`;
    }

    const hours = Math.floor(durationMinutes / 60);
    const minutes = durationMinutes % 60;
    return `${hours}h ${minutes}m`;
  }, [currentSession]);

  const handleGetRecommendations = async () => {
    if (consumedDrinks.length === 0) {
      return;
    }
    await getRecommendations();
  };

  const handleResetSession = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to reset your session? This will clear all consumed drinks and start fresh.'
    );
    if (confirmed) {
      await resetSession();
    }
  };

  const drinkCount = consumedDrinks.length;
  const hasSession = currentSession !== null;

  return (
    <div className="flex items-center gap-3">
      {/* Session Info */}
      {hasSession && (
        <div className="flex items-center gap-4 px-4 py-2 bg-gray-100 rounded-lg">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">{sessionDuration}</span>
          </div>
          <div className="h-4 w-px bg-gray-300" />
          <div className="text-sm text-gray-700">
            <span className="font-semibold">{drinkCount}</span>{' '}
            {drinkCount === 1 ? 'drink' : 'drinks'}
          </div>
        </div>
      )}

      {/* Get Recommendations Button */}
      <button
        onClick={handleGetRecommendations}
        disabled={drinkCount === 0 || isLoadingRecommendations}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg transition-colors text-sm font-medium"
      >
        <Sparkles className="w-4 h-4" />
        {isLoadingRecommendations ? 'Getting Recommendations...' : 'Get AI Recommendations'}
      </button>

      {/* Reset Session Button */}
      <button
        onClick={handleResetSession}
        disabled={!hasSession || isLoading}
        className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed border border-gray-300 text-gray-700 rounded-lg transition-colors text-sm font-medium"
      >
        <RotateCcw className="w-4 h-4" />
        Reset Session
      </button>
    </div>
  );
}
