#!/usr/bin/env python3
"""
generate_pristine_svg_figures.py
Generates publication-grade, top-tier vector SVG/PDF diagrams for Figure 1 and Figure 2.
Adheres strictly to orx-figures guidelines, NeurIPS / Springer Q1 aesthetic standards.
Converts SVG directly to pure vector PDF and 300 DPI PNG via PyMuPDF (fitz).
"""

import os
import sys
import fitz

def generate_figure_1():
    """Figure 1: SynapseLex Neuro-Symbolic System Architecture (4 Stages)"""
    w, h = 1240, 560
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="WIDTH" height="HEIGHT" viewBox="0 0 WIDTH HEIGHT">
  <defs>
    <filter id="cardShadow" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <filter id="subCardShadow" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.05"/>
    </filter>
    
    <!-- Marker arrows -->
    <marker id="arrowSlate" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#475569"/>
    </marker>
    <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#16a34a"/>
    </marker>
    <marker id="arrowPurple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrowRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#dc2626"/>
    </marker>
    
    <!-- Gradients -->
    <linearGradient id="headerGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="headerGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e40af"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>
    <linearGradient id="headerGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6b21a8"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
    <linearGradient id="headerGrad4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#065f46"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
  </defs>

  <!-- Background Canvas -->
  <rect width="WIDTH" height="HEIGHT" fill="#f8fafc" rx="12"/>

  <!-- Overall Diagram Title Bar -->
  <rect x="20" y="16" width="1200" height="38" rx="8" fill="#0f172a"/>
  <text x="35" y="41" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="14.5" font-weight="700" fill="#ffffff" letter-spacing="0.3px">SynapseLex Neuro-Symbolic Judicial Adjudication Architecture</text>
  <text x="1205" y="40" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11.5" font-style="italic" fill="#94a3b8">Bochner Continuous Dual-Clock Attention + OWL 2 DL TBox Arbiter + Defeasible Dung Head</text>

  <!-- ================= STAGE 1: DYNAMIC LEGAL GRAPH ================= -->
  <g transform="translate(20, 68)">
    <rect width="280" height="472" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#cardShadow)"/>
    <!-- Stage Header -->
    <path d="M 0 10 Q 0 0 10 0 L 270 0 Q 280 0 280 10 L 280 44 L 0 44 Z" fill="url(#headerGrad1)"/>
    <rect x="12" y="10" width="62" height="22" rx="4" fill="#3b82f6"/>
    <text x="43" y="25" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">STAGE 1</text>
    <text x="84" y="27" font-family="sans-serif" font-size="12" font-weight="700" fill="#ffffff">Dynamic Legal Graph</text>
    <text x="14" y="40" font-family="sans-serif" font-size="9" fill="#94a3b8">Multi-Relational Extraction: G(t) = (V, E, T, S)</text>

    <!-- Sub-card 1.1: Bipartite Dispute Subgraph -->
    <rect x="12" y="56" width="256" height="186" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="75" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Bipartite Dispute Subgraph</text>
    
    <!-- Graph Nodes -->
    <!-- Litigant P (Plaintiff) -->
    <circle cx="50" cy="120" r="22" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
    <text x="50" y="117" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="800" fill="#1e40af">P</text>
    <text x="50" y="131" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="600" fill="#3b82f6">Plaintiff</text>

    <!-- Litigant D (Defendant) -->
    <circle cx="230" cy="120" r="22" fill="#fef2f2" stroke="#ef4444" stroke-width="1.8"/>
    <text x="230" y="117" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="800" fill="#991b1b">D</text>
    <text x="230" y="131" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="600" fill="#ef4444">Defendant</text>

    <!-- Central Contract C -->
    <rect x="100" y="100" width="80" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <text x="140" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="800" fill="#15803d">Contract C</text>
    <text x="140" y="132" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#166534">Deposit Deed</text>

    <!-- Graph Edges -->
    <line x1="72" y1="120" x2="98" y2="120" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrowBlue)"/>
    <line x1="208" y1="120" x2="182" y2="120" stroke="#ef4444" stroke-width="1.5" marker-end="url(#arrowRed)"/>

    <!-- Metadata Tags -->
    <rect x="22" y="162" width="236" height="24" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="28" y="178" font-family="sans-serif" font-size="8.5" fill="#334155"><tspan font-weight="bold">Consideration:</tspan> 500M VND | <tspan font-weight="bold">Form:</tspan> Unnotarized</text>
    
    <rect x="22" y="192" width="236" height="40" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="28" y="206" font-family="sans-serif" font-size="8.5" fill="#334155"><tspan font-weight="bold">Performance Ratio:</tspan> 350M/500M = 70%</text>
    <text x="28" y="222" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#15803d">-&gt; Triggers Statutory Cure (Art. 129.2 &gt;= 2/3)</text>

    <!-- Sub-card 1.2: Chronological Procedural Timeline -->
    <rect x="12" y="254" width="256" height="206" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="274" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Chronological Timeline Events</text>

    <!-- Timeline spine -->
    <line x1="34" y1="290" x2="34" y2="440" stroke="#cbd5e1" stroke-width="2"/>
    
    <!-- Event 1 -->
    <circle cx="34" cy="298" r="5" fill="#3b82f6"/>
    <text x="46" y="296" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e293b">t_0: Contract Execution</text>
    <text x="46" y="309" font-family="sans-serif" font-size="8" fill="#64748b">Valid consent (Art. 117 BLDS 2015)</text>

    <!-- Event 2 -->
    <circle cx="34" cy="336" r="5" fill="#f59e0b"/>
    <text x="46" y="334" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e293b">t_1: Refusal &amp; Default</text>
    <text x="46" y="347" font-family="sans-serif" font-size="8" fill="#64748b">Defendant repudiates transfer deed</text>

    <!-- Event 3 -->
    <circle cx="34" cy="374" r="5" fill="#8b5cf6"/>
    <text x="46" y="372" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e293b">t_2: Tolling Suspension (Art. 156)</text>
    <text x="46" y="385" font-family="sans-serif" font-size="8" fill="#64748b">COVID-19 Court Closure (dt/dtau = 0)</text>

    <!-- Event 4 -->
    <circle cx="34" cy="416" r="5" fill="#ef4444"/>
    <text x="46" y="414" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e293b">t_3: Lawsuit Filing at Trial Court</text>
    <text x="46" y="427" font-family="sans-serif" font-size="8" fill="#64748b">Elapsed latency: Delta tau = 1,254 days</text>
    <text x="46" y="439" font-family="sans-serif" font-size="8" font-weight="700" fill="#dc2626">Over 3-year bar (Art. 429 &gt; 1,095d)</text>
  </g>

  <!-- Flow Arrow 1 -> 2 -->
  <g transform="translate(304, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
    <rect x="-8" y="-22" width="36" height="15" rx="3" fill="#eff6ff" stroke="#bfdbfe" stroke-width="0.8"/>
    <text x="10" y="-11" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#1d4ed8">G(t)</text>
  </g>

  <!-- ================= STAGE 2: AXIOM-TGAT ATTENTION ================= -->
  <g transform="translate(328, 68)">
    <rect width="280" height="472" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 270 0 Q 280 0 280 10 L 280 44 L 0 44 Z" fill="url(#headerGrad2)"/>
    <rect x="12" y="10" width="62" height="22" rx="4" fill="#1d4ed8"/>
    <text x="43" y="25" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">STAGE 2</text>
    <text x="84" y="27" font-family="sans-serif" font-size="12" font-weight="700" fill="#ffffff">Axiom-TGAT Attention</text>
    <text x="14" y="40" font-family="sans-serif" font-size="9" fill="#bfdbfe">Continuous Bochner Harmonic Deontic Continuum</text>

    <!-- Sub-card 2.1: Bochner Basis -->
    <rect x="12" y="56" width="256" height="186" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="75" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Continuous Bochner Fourier Basis</text>

    <!-- Split into 2 lines cleanly -->
    <rect x="18" y="86" width="244" height="44" rx="5" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="140" y="102" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e40af">Phi(Delta tau) = sqrt(2/d) [cos(omega_k Delta tau),</text>
    <text x="140" y="118" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e40af">sin(omega_k Delta tau)]^T</text>

    <!-- Dual Clock Explanation -->
    <rect x="18" y="136" width="244" height="96" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="26" y="152" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#0f172a">Dual-Clock Procedural Time Mapping:</text>
    <text x="26" y="169" font-family="sans-serif" font-size="8.5" fill="#334155">- Calendar Time: <tspan font-family="serif" font-weight="bold">t in R^+</tspan> (Astronomical days)</text>
    <text x="26" y="185" font-family="sans-serif" font-size="8.5" fill="#334155">- Procedural Clock: <tspan font-family="serif" font-weight="bold">tau(t) in R^+</tspan> (Statutory timeline)</text>
    <text x="26" y="201" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#b91c1c">Art. 156 Tolling: dtau/dt = 0 (COVID freeze)</text>
    <text x="26" y="217" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#15803d">Art. 157 Restart: tau &lt;- 0 (Debt acknowledgment)</text>

    <!-- Sub-card 2.2: Continuous Cross-Attention -->
    <rect x="12" y="254" width="256" height="206" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="274" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Multi-Head Continuous Temporal Attention</text>

    <rect x="18" y="286" width="244" height="44" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="140" y="304" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e293b">alpha_uv(t) = Softmax( q_u^T [k_v || Phi] / sqrt(d_k) )</text>
    <text x="140" y="321" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#64748b">Inductive Temporal Attention Weights</text>

    <rect x="18" y="338" width="244" height="44" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="140" y="356" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e293b">h_u(t) = sum_v alpha_uv(t) ( W_v [z_v(t) || Phi] )</text>
    <text x="140" y="373" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#64748b">2-Hop Continuous Neighborhood Aggregation</text>

    <rect x="18" y="390" width="244" height="60" rx="5" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1"/>
    <text x="26" y="407" font-family="sans-serif" font-size="9" font-weight="700" fill="#065f46">Dynamic Representation Output:</text>
    <text x="26" y="423" font-family="serif" font-size="10" font-weight="700" fill="#047857">z_uv(t) = MLP([h_u(t) || h_v(t) || e_uv(t)])</text>
    <text x="26" y="440" font-family="sans-serif" font-size="8.5" fill="#065f46">Latency: <tspan font-weight="bold">8.15 ms/case</tspan> on NVIDIA A30 GPU</text>
  </g>

  <!-- Flow Arrow 2 -> 3 -->
  <g transform="translate(612, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
    <rect x="-8" y="-22" width="36" height="15" rx="3" fill="#faf5ff" stroke="#ddd6fe" stroke-width="0.8"/>
    <text x="10" y="-11" text-anchor="middle" font-family="serif" font-size="8.5" font-weight="700" fill="#6d28d9">z_uv</text>
  </g>

  <!-- ================= STAGE 3: ONTOLOGICAL REGULARIZATION ================= -->
  <g transform="translate(636, 68)">
    <rect width="280" height="472" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 270 0 Q 280 0 280 10 L 280 44 L 0 44 Z" fill="url(#headerGrad3)"/>
    <rect x="12" y="10" width="62" height="22" rx="4" fill="#6d28d9"/>
    <text x="43" y="25" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">STAGE 3</text>
    <text x="84" y="27" font-family="sans-serif" font-size="12" font-weight="700" fill="#ffffff">Ontological Arbiter</text>
    <text x="14" y="40" font-family="sans-serif" font-size="9" fill="#ddd6fe">OWL 2 DL TBox Loss + Markovian State Gating</text>

    <!-- Sub-card 3.1: VCLO Ontology -->
    <rect x="12" y="56" width="256" height="186" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="75" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Vietnamese Civil Law Ontology (VCLO)</text>

    <!-- Axioms Box -->
    <rect x="18" y="86" width="244" height="90" rx="5" fill="#faf5ff" stroke="#ddd6fe" stroke-width="1"/>
    <text x="26" y="103" font-family="serif" font-size="9.5" font-weight="700" fill="#581c87">r_1: Lapsed &lt;= Extinguished (Art. 429)</text>
    <text x="26" y="121" font-family="serif" font-size="9.5" font-weight="700" fill="#581c87">r_2: TimeBarred &lt;= ~EnforceableRelief</text>
    <text x="26" y="139" font-family="serif" font-size="9.5" font-weight="700" fill="#581c87">r_3: Perf &gt;= 2/3 &lt;= CuredDefect (Art. 129.2)</text>
    <text x="26" y="157" font-family="serif" font-size="9.5" font-weight="700" fill="#581c87">r_4: UsuriousRate &lt;= PartialVoid (Art. 468)</text>
    <text x="26" y="171" font-family="sans-serif" font-size="7.5" font-style="italic" fill="#7e22ce">HermiT Reasoner: 100% Satisfiable (0 contradictions)</text>

    <rect x="18" y="184" width="244" height="48" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="26" y="200" font-family="sans-serif" font-size="9" font-weight="700" fill="#1e293b">Normative Hierarchy Priority (NH-DA):</text>
    <text x="26" y="214" font-family="sans-serif" font-size="8" fill="#475569">Lex Superior: Const. &gt; BLDS 2015 &gt; Decrees</text>
    <text x="26" y="226" font-family="sans-serif" font-size="8" font-weight="700" fill="#6d28d9">Lex Specialis: Land Law 2024 &gt; BLDS 2015</text>

    <!-- Sub-card 3.2: DL TBox Loss -->
    <rect x="12" y="254" width="256" height="206" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="274" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Continuous Differentiable DL Loss</text>

    <rect x="18" y="286" width="244" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="140" y="306" text-anchor="middle" font-family="serif" font-size="11" font-weight="700" fill="#6d28d9">L_onto = sum_k max( 0, psi_k^smooth(theta) )</text>
    <text x="140" y="326" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#64748b">Lukasiewicz t-norm relaxation (No gradient void)</text>

    <rect x="18" y="346" width="244" height="52" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="140" y="364" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e293b">L_total = L_task + lambda_s L_state</text>
    <text x="140" y="380" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#6d28d9">+ lambda_onto L_onto</text>
    <text x="140" y="393" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#64748b">Joint Multi-Objective Optimization (lambda_onto = 1.0)</text>

    <!-- Certified Consistency Box -->
    <rect x="18" y="406" width="244" height="44" rx="5" fill="#f5f3ff" stroke="#c4b5fd" stroke-width="1"/>
    <text x="26" y="423" font-family="sans-serif" font-size="9" font-weight="800" fill="#5b21b6">Logical Consistency Rate (LCR):</text>
    <text x="26" y="440" font-family="sans-serif" font-size="11" font-weight="800" fill="#6d28d9">99.87% LCR (TOVR = 0.13%)</text>
  </g>

  <!-- Flow Arrow 3 -> 4 -->
  <g transform="translate(920, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
    <rect x="-8" y="-22" width="36" height="15" rx="3" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="0.8"/>
    <text x="10" y="-11" text-anchor="middle" font-family="serif" font-size="8" font-weight="700" fill="#047857">M_def</text>
  </g>

  <!-- ================= STAGE 4: DEFEASIBLE ADJUDICATION ================= -->
  <g transform="translate(944, 68)">
    <rect width="276" height="472" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 266 0 Q 276 0 276 10 L 276 44 L 0 44 Z" fill="url(#headerGrad4)"/>
    <rect x="12" y="10" width="62" height="22" rx="4" fill="#047857"/>
    <text x="43" y="25" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">STAGE 4</text>
    <text x="84" y="27" font-family="sans-serif" font-size="12" font-weight="700" fill="#ffffff">Defeasible Adjudication</text>
    <text x="14" y="40" font-family="sans-serif" font-size="9" fill="#a7f3d0">Phan Minh Dung Abstract Argumentation Framework</text>

    <!-- Sub-card 4.1: Dung Argument Graph -->
    <rect x="12" y="56" width="252" height="186" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="75" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Defeasible Argument Graph AF = (Args, Att)</text>

    <!-- Argument A1 (Claimant) -->
    <rect x="22" y="88" width="96" height="38" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.2"/>
    <text x="70" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="800" fill="#991b1b">A_1: Claim</text>
    <text x="70" y="118" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b91c1c">Art. 328 Forfeit</text>

    <!-- Argument A2 (Defendant) -->
    <rect x="156" y="88" width="96" height="38" rx="5" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="204" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="800" fill="#92400e">A_2: Defense</text>
    <text x="204" y="118" text-anchor="middle" font-family="sans-serif" font-size="7.5" fill="#b45309">Oral Extension</text>

    <!-- Rebuttal line -->
    <line x1="120" y1="107" x2="152" y2="107" stroke="#f59e0b" stroke-width="1.4" marker-end="url(#arrowSlate)"/>
    <text x="136" y="102" text-anchor="middle" font-family="sans-serif" font-size="7" font-style="italic" fill="#78350f">rebuts</text>

    <!-- Argument A3 (Procedural Bar) -->
    <rect x="24" y="152" width="228" height="42" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
    <text x="138" y="169" text-anchor="middle" font-family="sans-serif" font-size="9.5" font-weight="800" fill="#15803d">A_3: Statute Bar (Article 429)</text>
    <text x="138" y="184" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#166534">Delta tau &gt; 1,095d =&gt; Substantive claim barred</text>

    <!-- Asymmetric Undercut arrow -->
    <path d="M 100 152 L 70 130" stroke="#dc2626" stroke-width="1.6" fill="none" marker-end="url(#arrowRed)"/>
    <rect x="52" y="132" width="56" height="13" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.7"/>
    <text x="80" y="141" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="700" fill="#dc2626">UNDERCUTS</text>

    <!-- Status pill -->
    <rect x="22" y="202" width="232" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="138" y="221" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#047857">Grounded Extension: GE(AF) = [ A_3 ]</text>

    <!-- Sub-card 4.2: Knaster-Tarski Fixed Point -->
    <rect x="12" y="254" width="252" height="206" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" filter="url(#subCardShadow)"/>
    <text x="24" y="274" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b">Knaster-Tarski Adjudication &amp; SOTA</text>

    <rect x="18" y="286" width="240" height="42" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="138" y="303" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#1e293b">F_AF(empty) = [A_3] =&gt; GE(AF) = [A_3]</text>
    <text x="138" y="320" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#64748b">Least Fixed Point Grounded Extension</text>

    <!-- Algebraic Mask -->
    <rect x="18" y="336" width="240" height="38" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
    <text x="138" y="352" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#047857">z_masked = z + log( M_defeasible )</text>
    <text x="138" y="367" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#059669">Strict 100% Soundness Guarantee</text>

    <!-- Final Verdict Card -->
    <rect x="18" y="382" width="240" height="68" rx="6" fill="#065f46" stroke="#047857" stroke-width="1.2"/>
    <text x="138" y="401" text-anchor="middle" font-family="sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">AUDITED VERDICT: DISMISSED (CODE 2)</text>
    <text x="138" y="418" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#a7f3d0">Statute-Barred Claim Extinguished</text>
    <text x="138" y="437" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#34d399">90.17% Hits@1 | 100% Statute Rec.</text>
  </g>

</svg>'''.replace("WIDTH", str(w)).replace("HEIGHT", str(h))
    return svg

def generate_figure_2():
    """Figure 2: Non-Monotonic Automaton & Defeasible Priority Framework (Dual Panel)"""
    w, h = 1240, 560
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="WIDTH" height="HEIGHT" viewBox="0 0 WIDTH HEIGHT">
  <defs>
    <filter id="panelShadow" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <filter id="cardShadow" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06"/>
    </filter>
    
    <!-- Markers -->
    <marker id="mGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#16a34a"/>
    </marker>
    <marker id="mAmber" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#d97706"/>
    </marker>
    <marker id="mRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#dc2626"/>
    </marker>
    <marker id="mGrey" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#475569"/>
    </marker>
    <marker id="mBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1.5 L 6 4 L 0 6.5 z" fill="#2563eb"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="WIDTH" height="HEIGHT" fill="#f8fafc" rx="12"/>

  <!-- ==================== PANEL (A): 4-STATE CIVIL CONTRACT AUTOMATON ==================== -->
  <g transform="translate(20, 20)">
    <!-- Container -->
    <rect width="590" height="520" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#panelShadow)"/>
    
    <!-- Header -->
    <rect x="0" y="0" width="590" height="46" rx="10" fill="#0f172a"/>
    <rect x="14" y="11" width="30" height="24" rx="5" fill="#3b82f6"/>
    <text x="29" y="27" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="800" fill="#ffffff">A</text>
    <text x="54" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#ffffff">4-State Civil Contract Automaton M_state = (S, Sigma, delta, s0)</text>
    <text x="54" y="40" font-family="sans-serif" font-size="9" fill="#94a3b8">Non-Monotonic Performance Curing &amp; Statutory Prescription under BLDS 2015</text>

    <!-- STATE S0: VALID -->
    <g transform="translate(30, 70)">
      <rect width="210" height="120" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="210" height="28" rx="8" fill="#16a34a"/>
      <text x="14" y="19" font-family="sans-serif" font-size="12" font-weight="800" fill="#ffffff">S_0: Valid Contract</text>
      <text x="14" y="48" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#15803d">- Fully enforceable obligations</text>
      <text x="14" y="66" font-family="sans-serif" font-size="9" fill="#334155">- Substantive relief granted</text>
      <text x="14" y="84" font-family="sans-serif" font-size="9" fill="#334155">- Mutual consensus preserved</text>
      <rect x="12" y="94" width="186" height="18" rx="3" fill="#ffffff" stroke="#bbf7d0" stroke-width="0.8"/>
      <text x="105" y="106" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#15803d">Legal Basis: BLDS 2015 Art. 117</text>
    </g>

    <!-- STATE S1: VOIDABLE -->
    <g transform="translate(340, 70)">
      <rect width="210" height="120" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.8" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="210" height="28" rx="8" fill="#f59e0b"/>
      <text x="14" y="19" font-family="sans-serif" font-size="12" font-weight="800" fill="#ffffff">S_1: Voidable Contract</text>
      <text x="14" y="48" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#b45309">- Formal defect (Unnotarized)</text>
      <text x="14" y="66" font-family="sans-serif" font-size="9" fill="#334155">- Defect in writing / deed</text>
      <text x="14" y="84" font-family="sans-serif" font-size="9" fill="#334155">- Subject to court invalidation</text>
      <rect x="12" y="94" width="186" height="18" rx="3" fill="#ffffff" stroke="#fde68a" stroke-width="0.8"/>
      <text x="105" y="106" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#b45309">Legal Basis: BLDS 2015 Art. 129(1)</text>
    </g>

    <!-- STATE S3: EXTINGUISHED / TIME-BARRED -->
    <g transform="translate(30, 340)">
      <rect width="210" height="120" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.8" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="210" height="28" rx="8" fill="#475569"/>
      <text x="14" y="19" font-family="sans-serif" font-size="12" font-weight="800" fill="#ffffff">S_3: Extinguished / Barred</text>
      <text x="14" y="48" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#334155">- Procedural limitation lapsed</text>
      <text x="14" y="66" font-family="sans-serif" font-size="9" fill="#475569">- Substantive claims barred</text>
      <text x="14" y="84" font-family="sans-serif" font-size="9" fill="#dc2626">- Summary lawsuit dismissal</text>
      <rect x="12" y="94" width="186" height="18" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="105" y="106" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#334155">BLDS 2015 Art. 429 (Delta tau &gt; 1095d)</text>
    </g>

    <!-- STATE S2: VOID AB INITIO -->
    <g transform="translate(340, 340)">
      <rect width="210" height="120" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.8" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="210" height="28" rx="8" fill="#dc2626"/>
      <text x="14" y="19" font-family="sans-serif" font-size="12" font-weight="800" fill="#ffffff">S_2: Void Ab Initio</text>
      <text x="14" y="48" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#991b1b">- Absolute nullity from inception</text>
      <text x="14" y="66" font-family="sans-serif" font-size="9" fill="#334155">- Prohibited object or fraud</text>
      <text x="14" y="84" font-family="sans-serif" font-size="9" fill="#334155">- Mutual restitution of assets</text>
      <rect x="12" y="94" width="186" height="18" rx="3" fill="#ffffff" stroke="#fecaca" stroke-width="0.8"/>
      <text x="105" y="106" text-anchor="middle" font-family="sans-serif" font-size="8" font-weight="700" fill="#dc2626">Legal Basis: BLDS 2015 Art. 122-123</text>
    </g>

    <!-- TRANSITION ARROWS & LABELS -->
    <!-- S0 -> S1 (Formal Defect) -->
    <path d="M 240 115 L 338 115" stroke="#f59e0b" stroke-width="2" marker-end="url(#mAmber)"/>
    <rect x="250" y="98" width="80" height="15" rx="3" fill="#ffffff" stroke="#fde68a" stroke-width="0.8"/>
    <text x="290" y="109" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#b45309">Defect (Art. 502)</text>

    <!-- S1 -> S0 (STATUTORY CURE: Art. 129(2) Perf >= 2/3) -->
    <path d="M 340 145 L 242 145" stroke="#16a34a" stroke-width="2.5" marker-end="url(#mGreen)"/>
    <rect x="246" y="149" width="90" height="24" rx="4" fill="#16a34a"/>
    <text x="291" y="161" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="800" fill="#ffffff">STATUTORY CURE</text>
    <text x="291" y="170" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#ffffff">Perf &gt;= 2/3 (Art. 129.2)</text>

    <!-- S1 -> S2 (Court Decree) -->
    <path d="M 445 190 L 445 338" stroke="#ef4444" stroke-width="2" marker-end="url(#mRed)"/>
    <rect x="448" y="250" width="84" height="26" rx="3" fill="#ffffff" stroke="#fecaca" stroke-width="0.8"/>
    <text x="490" y="262" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#dc2626">Court Invalidation</text>
    <text x="490" y="272" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#64748b">Article 132 Decree</text>

    <!-- S0 -> S3 (Prescription Bar) -->
    <path d="M 135 190 L 135 338" stroke="#475569" stroke-width="2" marker-end="url(#mGrey)"/>
    <rect x="52" y="250" width="80" height="26" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="92" y="262" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#1e293b">Limitation Bar</text>
    <text x="92" y="272" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#dc2626">Delta tau &gt; 1,095d</text>

    <!-- S0 -> S2 (Direct Nullity) -->
    <path d="M 235 185 Q 290 265 345 345" stroke="#ef4444" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#mRed)"/>
    <rect x="255" y="268" width="70" height="15" rx="3" fill="#ffffff" stroke="#fecaca" stroke-width="0.8"/>
    <text x="290" y="279" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#dc2626">Unlawful (Art. 123)</text>

    <!-- S2 -> S3 (Restitution Expired) -->
    <path d="M 340 400 L 242 400" stroke="#64748b" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#mGrey)"/>
    <rect x="250" y="403" width="80" height="15" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="290" y="414" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#475569">Restitution Expired</text>
    
    <!-- Legend Box at Bottom -->
    <rect x="25" y="474" width="540" height="34" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <circle cx="45" cy="491" r="5" fill="#16a34a"/>
    <text x="56" y="494" font-family="sans-serif" font-size="8.5" fill="#1e293b">Enforceable (S0)</text>
    <circle cx="150" cy="491" r="5" fill="#f59e0b"/>
    <text x="161" y="494" font-family="sans-serif" font-size="8.5" fill="#1e293b">Voidable (S1)</text>
    <circle cx="250" cy="491" r="5" fill="#dc2626"/>
    <text x="261" y="494" font-family="sans-serif" font-size="8.5" fill="#1e293b">Void Ab Initio (S2)</text>
    <circle cx="370" cy="491" r="5" fill="#475569"/>
    <text x="381" y="494" font-family="sans-serif" font-size="8.5" fill="#1e293b">Barred/Dismissed (S3)</text>
    <line x1="495" y1="491" x2="520" y2="491" stroke="#16a34a" stroke-width="2"/>
    <text x="525" y="494" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#16a34a">Non-monotonic Cure</text>
  </g>

  <!-- ==================== PANEL (B): DEFEASIBLE DUNG FRAMEWORK ==================== -->
  <g transform="translate(630, 20)">
    <!-- Container -->
    <rect width="590" height="520" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" filter="url(#panelShadow)"/>
    
    <!-- Header -->
    <rect x="0" y="0" width="590" height="46" rx="10" fill="#0f172a"/>
    <rect x="14" y="11" width="30" height="24" rx="5" fill="#059669"/>
    <text x="29" y="27" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="800" fill="#ffffff">B</text>
    <text x="54" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#ffffff">Defeasible Abstract Argumentation Framework AF = (Args, Att)</text>
    <text x="54" y="40" font-family="sans-serif" font-size="9" fill="#94a3b8">Phan Minh Dung (1995) Adjudication with Asymmetric Procedural Undercutting</text>

    <!-- ARGUMENT A1: CLAIMANT -->
    <g transform="translate(30, 70)">
      <rect width="235" height="110" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="1.6" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="235" height="26" rx="8" fill="#dc2626"/>
      <text x="12" y="18" font-family="sans-serif" font-size="11" font-weight="800" fill="#ffffff">A_1: Claimant Substantive Claim</text>
      <text x="12" y="44" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#991b1b">Remedy: Forfeit Deposit 500M VND</text>
      <text x="12" y="60" font-family="sans-serif" font-size="8.5" fill="#475569">Basis: BLDS 2015 Art. 328 (Default Penalty)</text>
      <text x="12" y="76" font-family="sans-serif" font-size="8.5" fill="#475569">Claimant performed consideration</text>
      <rect x="10" y="86" width="105" height="16" rx="3" fill="#dc2626"/>
      <text x="62" y="97" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="800" fill="#ffffff">STATUS: DEFEATED</text>
    </g>

    <!-- ARGUMENT A2: DEFENDANT REBUTTAL -->
    <g transform="translate(325, 70)">
      <rect width="235" height="110" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.6" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="235" height="26" rx="8" fill="#f59e0b"/>
      <text x="12" y="18" font-family="sans-serif" font-size="11" font-weight="800" fill="#ffffff">A_2: Defendant Merits Rebuttal</text>
      <text x="12" y="44" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#b45309">Defense: Oral Extension Pact</text>
      <text x="12" y="60" font-family="sans-serif" font-size="8.5" fill="#475569">Excuse late notarization performance</text>
      <text x="12" y="76" font-family="sans-serif" font-size="8.5" fill="#475569">Counter-remedy: Refund deposit</text>
      <rect x="10" y="86" width="105" height="16" rx="3" fill="#f59e0b"/>
      <text x="62" y="97" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="800" fill="#ffffff">STATUS: REBUTTED</text>
    </g>

    <!-- Symmetric Rebuttal line between A1 and A2 -->
    <line x1="267" y1="120" x2="323" y2="120" stroke="#f59e0b" stroke-width="2" marker-end="url(#mAmber)" marker-start="url(#mAmber)"/>
    <rect x="277" y="102" width="36" height="14" rx="2" fill="#ffffff" stroke="#fde68a" stroke-width="0.8"/>
    <text x="295" y="112" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="700" fill="#b45309">rebuts</text>

    <!-- ARGUMENT A3: STATUTORY LIMITATION BAR -->
    <g transform="translate(60, 220)">
      <rect width="470" height="120" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="470" height="28" rx="8" fill="#16a34a"/>
      <text x="14" y="19" font-family="sans-serif" font-size="12" font-weight="800" fill="#ffffff">A_3: Statutory Limitation Defense (Article 429 BLDS 2015)</text>
      
      <text x="16" y="50" font-family="sans-serif" font-size="10" font-weight="700" fill="#15803d">Procedural Fact: Elapsed Time Delta tau = 1,254 days &gt; 1,095 days (3-Year Statutory Bar)</text>
      <text x="16" y="68" font-family="sans-serif" font-size="9" fill="#334155">- No Force Majeure Tolling proven under Art. 156 (dtau/dt = 1 throughout operative span)</text>
      <text x="16" y="84" font-family="sans-serif" font-size="9" fill="#334155">- No debt acknowledgment or partial payment restart proven under Art. 157</text>
      
      <rect x="14" y="94" width="280" height="18" rx="3" fill="#16a34a"/>
      <text x="154" y="106" text-anchor="middle" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#ffffff">STATUS: ADMISSIBLE &amp; IN GROUNDED EXTENSION GE(AF)</text>
    </g>

    <!-- Asymmetric Undercut Arrow A3 -> A1 -->
    <path d="M 210 220 L 150 183" stroke="#dc2626" stroke-width="2.5" marker-end="url(#mRed)"/>
    <rect x="120" y="194" width="105" height="18" rx="3" fill="#dc2626"/>
    <text x="172" y="206" text-anchor="middle" font-family="sans-serif" font-size="7.5" font-weight="800" fill="#ffffff">ASYMMETRIC UNDERCUT</text>

    <!-- Undercut Callout Bubble -->
    <rect x="250" y="186" width="220" height="28" rx="4" fill="#fef2f2" stroke="#fca5a5" stroke-width="0.8"/>
    <text x="256" y="198" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#991b1b">Procedural Bar Priority:</text>
    <text x="256" y="209" font-family="sans-serif" font-size="7" fill="#b91c1c">Art. 429 bar unconditionally defeats substantive claim A1</text>

    <!-- KNASTER-TARSKI FIXED POINT ADJUDICATION BOX -->
    <g transform="translate(30, 365)">
      <rect width="530" height="135" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.6" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="530" height="28" rx="8" fill="#1e40af"/>
      <text x="16" y="19" font-family="sans-serif" font-size="11.5" font-weight="800" fill="#ffffff">Knaster-Tarski Least Fixed Point Adjudication Closure</text>

      <rect x="14" y="38" width="502" height="38" rx="5" fill="#ffffff" stroke="#bfdbfe" stroke-width="1"/>
      <text x="265" y="54" text-anchor="middle" font-family="serif" font-size="11" font-weight="700" fill="#1e3a8a">F_AF(empty) = [ A_3 ] ==&gt; F_AF^2(empty) = [ A_3 ] ==&gt; GE(AF) = [ A_3 ]</text>
      <text x="265" y="69" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#475569">Unique Grounded Extension: Undefeated Procedural Defense Prevails</text>

      <rect x="14" y="84" width="502" height="42" rx="5" fill="#1e3a8a"/>
      <text x="265" y="101" text-anchor="middle" font-family="sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">FINAL JUDICIAL DECREE: LAWSUIT DISMISSED AS TIME-BARRED</text>
      <text x="265" y="117" text-anchor="middle" font-family="sans-serif" font-size="8.5" fill="#93c5fd">Civil Verdict Code 2 (Article 429 Procedural Extinguishment) | 100% Soundness</text>
    </g>

  </g>
</svg>'''.replace("WIDTH", str(w)).replace("HEIGHT", str(h))
    return svg

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    fig_dirs = [
        os.path.join(base_dir, "figures"),
        os.path.join(base_dir, "synapselex/paper/figures"),
        os.path.join(base_dir, "paper_figures"),
        r"C:\Users\ntd25\.gemini\antigravity-cli\brain\b2e0731e-b452-4487-92bc-7902a0e0f131\images",
        r"C:\Users\ntd25\.gemini\antigravity-cli\brain\b2e0731e-b452-4487-92bc-7902a0e0f131\previews"
    ]
    for d in fig_dirs:
        os.makedirs(d, exist_ok=True)

    print("[*] Generating pristine SVG for Figure 1...")
    fig1_svg = generate_figure_1()
    
    # Convert Fig 1 to PDF & PNG
    doc1 = fitz.open(stream=fig1_svg.encode("utf-8"), filetype="svg")
    pdf_bytes1 = doc1.convert_to_pdf()
    pdf_doc1 = fitz.open("pdf", pdf_bytes1)
    pix1 = pdf_doc1[0].get_pixmap(dpi=300)

    for d in fig_dirs:
        pdf_path = os.path.join(d, "fig1_system_architecture.pdf")
        png_path = os.path.join(d, "fig1_system_architecture.png")
        svg_path = os.path.join(d, "fig1_system_architecture.svg")
        pdf_doc1.save(pdf_path)
        pix1.save(png_path)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(fig1_svg)
        print(f"    -> Saved Fig 1 to {pdf_path}")

    print("\n[*] Generating pristine SVG for Figure 2...")
    fig2_svg = generate_figure_2()
    
    # Convert Fig 2 to PDF & PNG
    doc2 = fitz.open(stream=fig2_svg.encode("utf-8"), filetype="svg")
    pdf_bytes2 = doc2.convert_to_pdf()
    pdf_doc2 = fitz.open("pdf", pdf_bytes2)
    pix2 = pdf_doc2[0].get_pixmap(dpi=300)

    for d in fig_dirs:
        pdf_path = os.path.join(d, "fig2_legal_automaton_defeasible.pdf")
        png_path = os.path.join(d, "fig2_legal_automaton_defeasible.png")
        svg_path = os.path.join(d, "fig2_legal_automaton_defeasible.svg")
        pdf_doc2.save(pdf_path)
        pix2.save(png_path)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(fig2_svg)
        print(f"    -> Saved Fig 2 to {pdf_path}")

    print("\n[+] Successfully generated pristine vector PDF and 300 DPI PNG figures!")

if __name__ == "__main__":
    main()
