'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DoctorRegister() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    license_number: '',
    specialization: '',
    hospital_name: 'City General Hospital',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const res = await fetch('https://medikiosk-backend-ilvk.onrender.com/api/auth/register-doctor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Registration failed');

      setMessage(data.message);
      setTimeout(() => router.push('/doctor-login'), 3000);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 p-8 rounded-xl shadow-lg border border-slate-700">
        <h2 className="text-2xl font-bold mb-2 text-teal-400">Doctor Registration</h2>
        <p className="text-slate-400 text-sm mb-6">Apply for hospital affiliation and system access.</p>

        {message && <div className="p-3 bg-green-500/20 border border-green-500 text-green-300 rounded mb-4">{message}</div>}
        {error && <div className="p-3 bg-red-500/20 border border-red-500 text-red-300 rounded mb-4">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Full Name (Dr. John Doe)"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
          />
          <input
            type="email"
            placeholder="Work Email"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />
          <input
            type="text"
            placeholder="Medical License Number"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            onChange={(e) => setFormData({ ...formData, license_number: e.target.value })}
          />
          <input
            type="text"
            placeholder="Specialization (e.g., Cardiology)"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            onChange={(e) => setFormData({ ...formData, specialization: e.target.value })}
          />
          <button type="submit" className="w-full py-3 bg-teal-500 hover:bg-teal-600 font-semibold rounded text-slate-950 transition">
            Submit Application
          </button>
        </form>
      </div>
    </div>
  );
}