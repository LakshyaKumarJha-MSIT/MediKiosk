'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DoctorLogin() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('https://medikiosk-backend-ilvk.onrender.com/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Login failed');

      localStorage.setItem('doctor_token', data.access_token);
      router.push('/doctor-dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 p-8 rounded-xl shadow-lg border border-slate-700">
        <h2 className="text-2xl font-bold mb-2 text-teal-400">Doctor Portal Login</h2>
        <p className="text-slate-400 text-sm mb-6">Enter your verified credentials to access patient logs.</p>

        {error && <div className="p-3 bg-red-500/20 border border-red-500 text-red-300 rounded mb-4 text-sm">{error}</div>}

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="Email Address"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            required
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded text-white"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="w-full py-3 bg-teal-500 hover:bg-teal-600 font-semibold rounded text-slate-950 transition">
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}