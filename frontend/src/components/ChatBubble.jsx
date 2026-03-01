export default function ChatBubble({
  question_id,
  question,
  answer,
  confidence,
  onUpdate
}) {
  const getConfidenceStyle = (level) => {
    switch (level) {
      case "High":
        return "bg-green-100 text-green-700";
      case "Medium":
        return "bg-yellow-100 text-yellow-700";
      case "Low":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-600";
    }
  };

  return (
    <div className="mb-8">
     
      <div className="flex justify-end">
        <div className="bg-blue-600 text-white p-4 rounded-2xl max-w-xl shadow">
          {question}
        </div>
      </div>

      
      <div className="flex justify-start mt-3">
        <div className="bg-white border p-4 rounded-2xl max-w-xl shadow w-full">
          <textarea
            value={answer}
            onChange={(e) => onUpdate(question_id, e.target.value)}
            className="w-full border rounded p-2 mb-3 resize-none"
            rows={4}
          />

          {confidence && confidence !== "None" && (
            <span
              className={`text-xs px-3 py-1 rounded-full font-semibold ${getConfidenceStyle(
                confidence
              )}`}
            >
              {confidence}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}