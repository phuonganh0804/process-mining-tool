import { useState } from "react";
import axios from "axios";
import "./App.css";



const FLASK_URL = "http://localhost:5000";

function App() {
  const [file, setFile] = useState(null);
  const [algorithm, setAlgorithm] = useState("");
  const [dependency, setDependency] = useState("0.9");
  const [and, setAnd] = useState("0.1");
  const [observation, setObservation] = useState("3");
  const [relative, setRelative] = useState("0.05");
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return setError("Please select a file");
    if (!algorithm) return setError("Please select an algorithm");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("algorithm", algorithm);
    formData.append("dependency", dependency);
    formData.append("and", and);
    formData.append("observation", observation);
    formData.append("relative", relative);

    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`/api/upload`, formData);
      const imagePath = response.data.result;
      setResultImage(`/api/result?path=${encodeURIComponent(imagePath)}`);
      
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="parent">
      <h1>Process Mining Tool</h1>
      <div className="input">
        <form onSubmit={handleUpload}>
          <label>
            Select your XES file:
            <input type="file" accept=".xes" onChange={(e) => setFile(e.target.files[0])} />
          </label>
          <label>
            Algorithm:
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
              <option value="">--Please choose an option--</option>
              <option value="Alpha Algorithm">Alpha Algorithm</option>
              <option value="Heuristic Miner">Heuristic Miner</option>
            </select>
          </label>
          {algorithm === "Heuristic Miner" && (
            <>
              <label>
                Dependency threshold:
                <input type="text" value={dependency} onChange={(e) => setDependency(e.target.value)} />
              </label>
              <label>
                AND-threshold:
                <input type="text" value={and} onChange={(e) => setAnd(e.target.value)} />
              </label>
              <label>
                Positive observations threshold:
                <input type="text" value={observation} onChange={(e) => setObservation(e.target.value)} />
              </label>
              <label>
                Relative to best threshold:
                <input type="text" value={relative} onChange={(e) => setRelative(e.target.value)} />
              </label>
            </>
          )}
          <button type="submit" disabled={loading}>
            {loading ? "Mining..." : "Start Mining"}
          </button>
        </form>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
      <div className="output">
        {resultImage && <img src={resultImage} alt="Mining result" />}
      </div>
    </div>
  );
}

export default App;