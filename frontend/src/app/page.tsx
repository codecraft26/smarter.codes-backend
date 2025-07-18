'use client'

import React, { useState } from "react";
import Card from "./components/Card";
import Input from "./components/Input";

function formatHtml(html: string) {
  try {
    return html.replace(/></g, '>' + '\n' + '<');
  } catch {
    return html;
  }
}

function getFirstWords(html: string, count: number) {
  // Remove HTML tags for preview
  const text = html.replace(/<[^>]+>/g, ' ');
  return text.split(/\s+/).slice(0, count).join(' ') + '...';
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showHtml, setShowHtml] = useState<{ [key: number]: boolean }>({});

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResults([]);
    setShowHtml({});
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, query }),
      });
      if (!response.ok) throw new Error("Failed to fetch results");
      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleHtml = (idx: number) => {
    setShowHtml(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex gap-4 mb-6">
          <Input
            type="text"
            placeholder="Enter URL"
            value={url}
            onChange={e => setUrl(e.target.value)}
          />
          <Input
            type="text"
            placeholder="Enter Query"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
        <h2 className="text-xl font-semibold mb-4 text-black">Search Results</h2>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <div className="space-y-6">
          {/* Shimmer effect for loading */}
          {loading && results.length === 0 && (
            <>
              {[1, 2, 3].map((i) => (
                <Card key={i} loading />
              ))}
            </>
          )}
          {/* Actual results */}
          {results.map((result, idx) => (
            <Card
              key={idx}
              content={getFirstWords(result.html, 10)}
              score={result.score}
            >
              <button
                className="text-blue-600 text-xs mb-2"
                onClick={() => handleToggleHtml(idx)}
              >
                {showHtml[idx] ? 'Hide content' : 'View content'}
              </button>
              {showHtml[idx] && (
                <pre className="bg-gray-100 rounded p-2 text-xs overflow-x-auto text-black" style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                  {formatHtml(result.html)}
                </pre>
              )}
            </Card>
          ))}
          {results.length === 0 && !loading && !error && (
            <div className="text-gray-500 text-center">No results found.</div>
          )}
        </div>
      </div>
    </main>
  );
}
