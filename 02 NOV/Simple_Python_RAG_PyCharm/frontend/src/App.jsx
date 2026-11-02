import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, PieChart, Pie, Cell, Legend
} from "recharts";
import {
  Activity, Brain, Clock, CheckCircle, RefreshCw, MessageSquare, Zap
} from "lucide-react";

const API = "http://127.0.0.1:8000";
const COLORS = ["#16a34a", "#dc2626", "#94a3b8"];

function StatCard({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-top"><span>{title}</span>{icon}</div>
      <h2>{value}</h2>
    </div>
  );
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchData() {
    try {
      setLoading(true);
      setError("");
      const [summaryResponse, recordsResponse] = await Promise.all([
        fetch(`${API}/summary`),
        fetch(`${API}/records`)
      ]);
      if (!summaryResponse.ok || !recordsResponse.ok) {
        throw new Error("Unable to fetch dashboard data. Check that the backend is running.");
      }
      setSummary(await summaryResponse.json());
      setRecords(await recordsResponse.json());
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchData(); }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return (
    <div className="loading">
      <p>{error}</p>
      <button onClick={fetchData}>Try again</button>
      <small>Start the FastAPI backend at http://127.0.0.1:8000</small>
    </div>
  );

  const models = summary?.models || [];
  const feedbackData = [
    { name: "Correct", value: models.reduce((s, m) => s + m.correct, 0) },
    { name: "Incorrect", value: models.reduce((s, m) => s + m.incorrect, 0) },
    { name: "Not rated", value: models.reduce((s, m) => s + m.not_rated, 0) }
  ];
  const hasFeedback = feedbackData.some(item => item.value > 0);

  return (
    <main className="dashboard">
      <header className="header">
        <div>
          <div className="brand"><Brain size={27} /><span>RAG Analytics</span></div>
          <p>Multi-Model Performance Dashboard</p>
        </div>
        <button className="refresh" onClick={fetchData}><RefreshCw size={17} />Refresh Data</button>
      </header>

      <section className="stats">
        <StatCard title="Total Questions" value={summary?.total_questions ?? 0} icon={<MessageSquare />} />
        <StatCard title="Models Tested" value={summary?.total_models ?? 0} icon={<Brain />} />
        <StatCard title="Overall Accuracy" value={`${summary?.accuracy ?? 0}%`} icon={<CheckCircle />} />
        <StatCard title="Avg Response Time" value={`${summary?.average_response_time ?? 0}s`} icon={<Clock />} />
      </section>

      <section className="panel">
        <div className="section-heading">
          <div><h2>Model Performance Comparison</h2><p>Accuracy percentage across different models</p></div>
          <Activity size={22} />
        </div>
        {models.length ? (
          <>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={models} margin={{ top: 10, right: 15, left: 0, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="model" tick={false} />
                <YAxis domain={[0, 100]} unit="%" />
                <Tooltip formatter={(value) => [`${value}%`, "Accuracy"]} />
                <Bar dataKey="accuracy" name="Accuracy" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
            <div className="model-labels">
              {models.map(m => <div key={m.model}><strong>{m.accuracy}%</strong><span>{m.model}</span></div>)}
            </div>
          </>
        ) : <p className="empty">No model data available yet. Run your RAG application and record feedback.</p>}
      </section>

      <section className="charts">
        <div className="panel">
          <div className="section-heading">
            <div><h2>Response Time</h2><p>Average time taken by each model</p></div>
            <Zap size={21} />
          </div>
          {models.length ? (
            <>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={models} margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="model" tick={false} />
                  <YAxis unit="s" />
                  <Tooltip formatter={(value) => [`${value}s`, "Average response time"]} />
                  <Bar dataKey="average_response_time" name="Seconds" fill="#0ea5e9" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <div className="model-labels">
                {models.map(m => <div key={m.model}><strong>{m.average_response_time}s</strong><span>{m.model}</span></div>)}
              </div>
            </>
          ) : <p className="empty">No response data yet.</p>}
        </div>

        <div className="panel">
          <div className="section-heading">
            <div><h2>Feedback Distribution</h2><p>User evaluation of generated answers</p></div>
            <CheckCircle size={21} />
          </div>
          {hasFeedback ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={feedbackData} dataKey="value" nameKey="name" outerRadius={85} label>
                  {feedbackData.map((entry, index) => <Cell key={entry.name} fill={COLORS[index]} />)}
                </Pie>
                <Tooltip /><Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="empty">No feedback available yet.</p>}
        </div>
      </section>

      <section className="panel">
        <div className="section-heading"><div><h2>Detailed Model Comparison</h2><p>Performance statistics for each LLM</p></div></div>
        <div className="table-wrapper">
          <table>
            <thead><tr><th>Model</th><th>Questions</th><th>Correct</th><th>Incorrect</th><th>Accuracy</th><th>Avg Time</th></tr></thead>
            <tbody>
              {models.map(m => (
                <tr key={m.model}>
                  <td className="model-cell">{m.model}</td><td>{m.total_questions}</td>
                  <td className="green">{m.correct}</td><td className="red">{m.incorrect}</td>
                  <td>{m.accuracy}%</td><td>{m.average_response_time}s</td>
                </tr>
              ))}
              {!models.length && <tr><td colSpan="6" className="empty-cell">No model results available.</td></tr>}
            </tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <div className="section-heading"><div><h2>Question History</h2><p>Previously generated RAG answers</p></div></div>
        <div className="history-list">
          {[...records].reverse().map((record, index) => (
            <article className="history-item" key={`${record.timestamp}-${index}`}>
              <div className="history-top">
                <strong>{record.question}</strong>
                <span className={`status ${record.feedback === "Correct" ? "correct" : record.feedback === "Incorrect" ? "incorrect" : "pending"}`}>{record.feedback || "Not rated"}</span>
              </div>
              <p>{record.answer}</p>
              <div className="history-meta">
                <span>{record.model}</span><span>{record.total_seconds}s</span>
                <span>Chunks: {record.retrieved_chunk_ids}</span>
              </div>
            </article>
          ))}
          {!records.length && <p className="empty">No questions recorded yet.</p>}
        </div>
      </section>

      <footer>RAG Analytics Dashboard · React + FastAPI</footer>
    </main>
  );
}
