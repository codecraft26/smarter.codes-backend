import React from "react";

interface CardProps {
  content?: string;
  score?: number;
  loading?: boolean;
  children?: React.ReactNode;
  shimmerLines?: number[];
}

export default function Card({ content, score, loading, children, shimmerLines = [1, 0.83, 0.66] }: CardProps) {
  if (loading) {
    return (
      <div className="bg-white rounded shadow p-4 border animate-pulse">
        <div className="flex justify-between items-center mb-1">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
          <div className="h-4 bg-green-100 rounded w-16" />
        </div>
        {shimmerLines.map((w, i) => (
          <div key={i} className="h-3 bg-gray-100 rounded mb-1" style={{ width: `${w * 100}%` }} />
        ))}
      </div>
    );
  }
  return (
    <div className="bg-white rounded shadow p-4 border">
      <div className="flex justify-between items-center mb-1">
        <span className="font-medium text-gray-900">{content}</span>
        {score !== undefined && (
          <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-semibold">
            {score}% match
          </span>
        )}
      </div>
      {children}
    </div>
  );
} 