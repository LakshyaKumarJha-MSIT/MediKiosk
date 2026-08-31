'use client';

import Link from 'next/link';

export default function HospitalLanding() {
  return (
    <div className="min-h-screen bg-slate-900 text-white font-sans">
      {/* Navigation Header */}
      <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center font-bold text-slate-950 text-xl">
              +
            </div>
            <span className="text-xl font-bold tracking-tight text-white">MediKiosk Health</span>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              href="/doctor-login"
              className="text-slate-300 hover:text-white px-4 py-2 text-sm font-medium transition"
            >
              Doctor Sign In
            </Link>
            <Link
              href="/doctor-register"
              className="bg-teal-500 hover:bg-teal-600 text-slate-950 px-4 py-2 rounded-lg text-sm font-semibold transition"
            >
              Apply as Doctor
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-20 text-center">
        <span className="bg-teal-500/10 border border-teal-500/30 text-teal-400 text-xs px-3 py-1 rounded-full uppercase tracking-wider font-semibold">
          Unified Multi-Tenant Medical Network
        </span>
        <h1 className="text-4xl md:text-6xl font-extrabold mt-6 max-w-4xl mx-auto leading-tight">
          Next-Generation Patient Care & Clinical Intelligence
        </h1>
        <p className="text-slate-400 text-lg mt-6 max-w-2xl mx-auto">
          Connecting intelligent triage kiosks directly with verified hospital specialists for seamless patient intakes and secure medical history tracking.
        </p>

        <div className="mt-10 flex justify-center gap-4">
          <Link
            href="/doctor-register"
            className="bg-teal-500 hover:bg-teal-600 text-slate-950 px-6 py-3 rounded-lg font-semibold text-lg transition shadow-lg shadow-teal-500/20"
          >
            Join Medical Staff
          </Link>
          <Link
            href="/admin"
            className="border border-slate-700 hover:bg-slate-800 text-slate-300 px-6 py-3 rounded-lg font-semibold text-lg transition"
          >
            Admin Verification Panel
          </Link>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700/60">
            <div className="w-12 h-12 bg-teal-500/10 text-teal-400 rounded-xl flex items-center justify-center mb-6 font-bold text-xl">
              01
            </div>
            <h3 className="text-xl font-bold mb-2">Automated Kiosk Triage</h3>
            <p className="text-slate-400 text-sm">
              Instant symptom assessment, vital checks, and FHIR-compliant record generation right at entry.
            </p>
          </div>

          <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700/60">
            <div className="w-12 h-12 bg-teal-500/10 text-teal-400 rounded-xl flex items-center justify-center mb-6 font-bold text-xl">
              02
            </div>
            <h3 className="text-xl font-bold mb-2">Verified Practitioner Access</h3>
            <p className="text-slate-400 text-sm">
              Strict identity and medical license validation process managed by hospital administration.
            </p>
          </div>

          <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700/60">
            <div className="w-12 h-12 bg-teal-500/10 text-teal-400 rounded-xl flex items-center justify-center mb-6 font-bold text-xl">
              03
            </div>
            <h3 className="text-xl font-bold mb-2">Secure JWT Workflow</h3>
            <p className="text-slate-400 text-sm">
              End-to-end encrypted authentication pipelines ensuring patient data privacy across all departments.
            </p>
          </div>
        </div>
      </section>

      {/* Emergency Banner */}
      <footer className="border-t border-slate-800 mt-16 bg-slate-950/40">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center text-slate-500 text-sm">
          <p>© 2026 MediKiosk Health Systems. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/doctor-login" className="hover:text-slate-300">Doctor Access</Link>
            <Link href="/admin" className="hover:text-slate-300">Admin</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}