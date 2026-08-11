import { Calendar } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="flex items-center gap-3 mb-4">
        <Calendar className="w-10 h-10 text-blue-600" aria-hidden />
        <h1 className="text-2xl font-semibold">calendarioprovas</h1>
      </div>
      <p className="text-gray-600 text-center max-w-md">
        Plataforma web — scaffold T1 (React + Vite + Tailwind). Telas MVP em{" "}
        <code className="text-sm bg-gray-100 px-1 rounded">target_screens.md</code>.
      </p>
    </div>
  );
}
