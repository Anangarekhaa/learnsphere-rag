import { useState } from "react";
import api from "../api";
import ChatBubble from "../components/ChatBubble";
import SummaryCard from "../components/SummaryCard";
import Navbar from "../components/NavBar";

export default function Dashboard() {
const [results, setResults] = useState([]);
const [summary, setSummary] = useState(null);
const [runId, setRunId] = useState(null);
const [loading, setLoading] = useState(false);

const [referenceFiles, setReferenceFiles] = useState([]);
const [questionnaireFile, setQuestionnaireFile] = useState(null);

  const handleUpload = async () => {
    if (!questionnaireFile) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", questionnaireFile);

    try {
      const uploadRes = await api.post("/upload-questionnaire", formData);
  
      const id = uploadRes.data.run_id;

      setRunId(id);
      setResults(uploadRes.data.results); 
      setSummary(uploadRes.data.summary);

    } catch (err) {
      console.error(err);
      alert("Error generating answers.");
    }

    setLoading(false);
  };


  const handleUpdateAnswer = (id, newAnswer) => {
  setResults((prev) =>
    prev.map((r) =>
      r.question_id === id ? { ...r, answer: newAnswer } : r
    )
  );
};

const handleExport = async () => {
  try {
   
    await api.post(`/update-answers/${runId}`, results);

    
    const res = await api.get(`/export/${runId}`, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "questionnaire_response.docx");
    document.body.appendChild(link);
    link.click();
    link.remove();

  } catch (err) {
    console.error("Export failed:", err);
    alert("Export failed.");
  }
};

const handleReferenceUpload = async () => {
  console.log("Upload clicked");

  if (!referenceFiles || referenceFiles.length === 0) {
    console.log("No files selected");
    alert("Please select at least one file");
    return;
  }

  const formData = new FormData();

  for (let i = 0; i < referenceFiles.length; i++) {
    formData.append("files", referenceFiles[i]);
  }

  console.log("Sending request...");

  try {
    const res = await api.post("/upload-reference", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    console.log("Response:", res.data);
    alert("Reference documents uploaded successfully.");

  } catch (err) {
    console.error("Upload error:", err.response?.data || err);
    alert("Upload failed.");
  }
};


  return (
  <div className="min-h-screen bg-gray-100 flex flex-col">
    <Navbar />

    <div className="flex-1 flex justify-center p-6">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-lg flex flex-col">

       
        {summary && (
          <div className="p-6 border-b">
            <SummaryCard summary={summary} />
          </div>
        )}

        
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading && (
            <div className="text-center text-gray-500">
              Generating responses...
            </div>
          )}

          {results.map((r) => (
            <ChatBubble
              key={r.question_id}
              question_id={r.question_id}
              question={r.question}
              answer={r.answer}
              confidence={r.confidence}
              onUpdate={handleUpdateAnswer}
            />
          ))}
        </div>

        
        <div className="border-t p-6 bg-gray-50 space-y-4">

          
          <div className="flex gap-3 items-center">
            <input
              type="file"
              multiple
              onChange={(e) => setReferenceFiles(e.target.files)}
              className="flex-1 border p-2 rounded-lg bg-white"
            />

            <button
              type="button"
              onClick={handleReferenceUpload}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg"
            >
              Upload Reference
            </button>
          </div>

          
          <div className="flex gap-3 items-center">
            <input
              type="file"
              onChange={(e) => setQuestionnaireFile(e.target.files[0])}
              className="flex-1 border p-2 rounded-lg bg-white"
            />

            <button
              type="button"
              onClick={handleUpload}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
            >
              Generate Answers
            </button>

            {runId && (
              <button
                type="button"
                onClick={handleExport}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg"
              >
                Export
              </button>
            )}
          </div>

        </div>
      </div>
    </div>
  </div>
);
}