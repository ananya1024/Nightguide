import { useState } from "react";
import ConstellationOverlay from "./components/ConstellationOverlay";
import LoadingSpinner from "./components/LoadingSpinner";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;
    
    // Validate file type
    if (!selectedFile.type.startsWith('image/')) {
      setError("Please select a valid image file");
      return;
    }
    
    setFile(selectedFile);
    setResult(null);
    setError(null);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error ${res.status}`);
      }
      
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
          🌌 NightGuide
        </h1>
        <p className="text-gray-400 mt-2">AI-powered constellation identifier</p>
      </div>

      <div className="max-w-4xl mx-auto px-6">
        {/* Upload Section */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 mb-6 border border-gray-800">
          <div className="flex flex-col items-center space-y-4">
            {/* File Input */}
            <div className="w-full max-w-md">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="w-full text-sm text-gray-300
                          file:mr-4 file:py-3 file:px-6
                          file:rounded-lg file:border-0
                          file:text-sm file:font-semibold
                          file:bg-gradient-to-r file:from-indigo-600 file:to-cyan-600 
                          file:text-white file:hover:from-indigo-700 file:hover:to-cyan-700
                          file:transition-all file:duration-200
                          cursor-pointer"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={handleAnalyze}
                disabled={!file || loading}
                className="bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-700 hover:to-cyan-700 
                          disabled:opacity-50 disabled:cursor-not-allowed
                          px-6 py-3 rounded-lg font-semibold transition-all duration-200
                          transform hover:scale-105"
              >
                {loading ? "Analyzing..." : "🔍 Analyze Constellation"}
              </button>
              
              {file && (
                <button
                  onClick={handleReset}
                  disabled={loading}
                  className="bg-gray-700 hover:bg-gray-600 disabled:opacity-50
                            px-6 py-3 rounded-lg font-semibold transition-all duration-200"
                >
                  Reset
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-300">❌ {error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 mb-6 border border-gray-800">
            <LoadingSpinner />
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6 border border-gray-800">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Constellation Overlay */}
              <div>
                <h3 className="text-xl font-semibold mb-4 text-indigo-300">
                  Constellation Detection
                </h3>
                <ConstellationOverlay
                  imageSrc={preview}
                  lines={result.lines || []}
                  points={result.points || []}
                  constellation={result.constellation}
                  description={result.description}
                />
              </div>

              {/* Results Info */}
              <div className="space-y-4">
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <h4 className="text-lg font-semibold text-cyan-300 mb-2">
                    Detected Constellation
                  </h4>
                  <p className="text-2xl font-bold text-white">
                    {result.constellation}
                  </p>
                  {result.description && (
                    <p className="text-gray-300 mt-1">{result.description}</p>
                  )}
                </div>

                <div className="bg-gray-800/50 rounded-lg p-4">
                  <h4 className="text-lg font-semibold text-cyan-300 mb-2">
                    Analysis Details
                  </h4>
                  <div className="space-y-2 text-sm">
                    <p><span className="text-gray-400">Stars Detected:</span> {result.detected_stars || 0}</p>
                    <p><span className="text-gray-400">Confidence:</span> 
                      <span className={`ml-2 px-2 py-1 rounded text-xs ${
                        result.confidence === 'high' ? 'bg-green-600' : 'bg-yellow-600'
                      }`}>
                        {result.confidence || 'medium'}
                      </span>
                    </p>
                    <p><span className="text-gray-400">Constellation Lines:</span> {result.lines?.length || 0}</p>
                    <p><span className="text-gray-400">Named Stars:</span> {result.points?.length || 0}</p>
                  </div>
                </div>

                {result.points && result.points.length > 0 && (
                  <div className="bg-gray-800/50 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-cyan-300 mb-2">
                      Named Stars
                    </h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      {result.points.map((point, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-gray-300">{point.name}</span>
                          <span className="text-gray-500">
                            ({Math.round(point.x * 100)}%, {Math.round(point.y * 100)}%)
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        {!file && !loading && !result && (
          <div className="text-center py-12 text-gray-400">
            <div className="text-6xl mb-4">🌠</div>
            <h3 className="text-xl font-semibold mb-2">Upload a Night Sky Photo</h3>
            <p className="max-w-md mx-auto">
              Take a photo of the night sky and upload it to identify constellations. 
              Our AI will analyze the stars and show you the constellation patterns.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
