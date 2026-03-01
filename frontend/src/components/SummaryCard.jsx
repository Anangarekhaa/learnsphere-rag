export default function SummaryCard({ summary }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow mb-6">
      <h3 className="text-lg font-semibold mb-4">Coverage Summary</h3>
      <div className="grid grid-cols-4 gap-4 text-center">
        <div>
          <p className="text-xl font-bold">{summary.total_questions}</p>
          <p className="text-gray-500 text-sm">Total</p>
        </div>
        <div>
          <p className="text-xl font-bold text-green-600">
            {summary.answered_with_citations}
          </p>
          <p className="text-gray-500 text-sm">Answered</p>
        </div>
        <div>
          <p className="text-xl font-bold text-red-600">
            {summary.not_found}
          </p>
          <p className="text-gray-500 text-sm">Not Found</p>
        </div>
        <div>
          <p className="text-xl font-bold">{summary.coverage_percent}%</p>
          <p className="text-gray-500 text-sm">Coverage</p>
        </div>
      </div>
    </div>
  );
}