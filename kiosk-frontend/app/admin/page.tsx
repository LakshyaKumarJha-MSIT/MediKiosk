'use client';

import { useEffect, useState } from 'react';

interface Doctor {
  id: number;
  full_name: string;
  email: string;
  license_number: string;
  specialization: string;
  hospital_name: string;
  is_verified: boolean;
}

export default function AdminDashboard() {
  const [pendingDoctors, setPendingDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const fetchPendingDoctors = async () => {
    try {
      const res = await fetch('https://medikiosk-backend-ilvk.onrender.com/api/admin/pending-doctors');
      if (!res.ok) throw new Error('Failed to fetch pending applications');
      const data = await res.json();
      setPendingDoctors(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPendingDoctors();
  }, []);

  const handleVerify = async (doctorId: number) => {
    setMessage('');
    setError('');

    try {
      const res = await fetch(`https://medikiosk-backend-ilvk.onrender.com/api/admin/verify-doctor/${doctorId}`, {
        method: 'POST',
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Verification failed');

      setMessage(data.message);
      // Refresh the list after verifying
      setPendingDoctors((prev) => prev.filter((doc) => doc.id !== doctorId));
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8 border-b border-slate-800 pb-4">
          <h1 className="text-3xl font-bold text-teal-400">Hospital Admin Portal</h1>
          <p className="text-slate-400 mt-1">Review and verify affiliated doctor applications.</p>
        </header>

        {message && <div className="p-4 bg-green-500/20 border border-green-500 text-green-300 rounded-lg mb-6">{message}</div>}
        {error && <div className="p-4 bg-red-500/20 border border-red-500 text-red-300 rounded-lg mb-6">{error}</div>}

        {loading ? (
          <p className="text-slate-400">Loading applications...</p>
        ) : pendingDoctors.length === 0 ? (
          <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 text-center text-slate-400">
            No pending doctor applications found.
          </div>
        ) : (
          <div className="grid gap-4">
            {pendingDoctors.map((doc) => (
              <div key={doc.id} className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex justify-between items-center">
                <div>
                  <h3 className="text-xl font-semibold text-white">{doc.full_name}</h3>
                  <p className="text-teal-400 text-sm font-medium">{doc.specialization} — {doc.hospital_name}</p>
                  <div className="mt-2 text-xs text-slate-400 space-y-1">
                    <p><span className="text-slate-500">Email:</span> {doc.email}</p>
                    <p><span className="text-slate-500">License No:</span> <code className="bg-slate-900 px-2 py-0.5 rounded text-amber-300">{doc.license_number}</code></p>
                  </div>
                </div>

                <button
                  onClick={() => handleVerify(doc.id)}
                  className="px-5 py-2.5 bg-teal-500 hover:bg-teal-600 font-semibold text-slate-950 rounded-lg transition"
                >
                  Approve & Verify
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}