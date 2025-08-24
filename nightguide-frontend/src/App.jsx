import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); // { constellation, lines?, points?, annotatedImage? }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;
    setFile(selectedFile);
    setResult(null);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      // expected shape:
      // { constellation: "Orion", lines: [[x1,y1,x2,y2], ...], points: [{x,y,name}], annotatedImage?: "data:image/png;base64,..." }
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Analyze failed. Is your backend running on 8000? Check the console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-950 text-white gap-6 p-6">
      <h1 className="text-3xl font-bold">🌌 NightGuide</h1>

      {/* File Input */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="text-sm text-gray-300
                   file:mr-4 file:py-2 file:px-4
                   file:rounded-lg file:border-0
                   file:text-sm file:font-semibold
                   file:bg-indigo-600 file:text-white
                   hover:file:bg-indigo-700"
      />

      {/* Preview */}
      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="max-w-xs rounded-lg shadow-lg"
        />
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={!file || loading}
        className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 px-4 py-2 rounded-lg"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {/* Result */}
      {result && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 w-full max-w-md">
          <p className="text-lg">
            Detected constellation:{" "}
            <span className="font-semibold text-indigo-400">
              {result.constellation || "—"}
            </span>
          </p>
        </div>
      )}
    </div>
  );
}
