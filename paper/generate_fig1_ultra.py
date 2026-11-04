"""
Generate Ultra-Refined Academic Figure 1:
SynapseLex Dual-Stream Neuro-Symbolic Architecture.
Incorporates:
- Real continuous sinusoidal Fourier wave rendering for Bochner Spectral Kernel
- Exact multi-relational case graph topology with timed edges
- Stacked Axiom-TGAT multi-head attention block with mathematical residual connections
- Formal Description Logic TBox Ontology and HermiT hypertableau reasoner integration
- Dung Defeasible Argumentation Head with Knaster-Tarski fixed-point computation
- Standard academic LaTeX typography (Computer Modern / Times Roman style)
"""
import fitz
import numpy as np

def generate_fig1_ultra_svg():
    width = 1440
    height = 680
    
    # Generate points for a clean sine wave to represent Bochner Fourier harmonics
    wave_pts = []
    for x_val in range(0, 110, 2):
        y_val = 15 * np.sin(x_val * 0.12)
        wave_pts.append(f"{x_val},{y_val:.1f}")
    wave_path = "M " + " L ".join(wave_pts)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Crisp Academic Arrowheads -->
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#1E293B"/>
    </marker>
    <marker id="arrBlue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#1D4ED8"/>
    </marker>
    <marker id="arrRed" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#DC2626"/>
    </marker>
    <marker id="arrGreen" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#15803D"/>
    </marker>
    <marker id="arrPurple" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#7C3AED"/>
    </marker>
  </defs>

  <!-- Clean Academic Pure White Background -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>

  <!-- ==================== STREAM HEADERS (LEFT MARGIN) ==================== -->
  <g transform="translate(15, 175) rotate(-90)">
    <rect x="-85" y="-12" width="170" height="24" rx="4" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="0.8"/>
    <text x="0" y="4" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#1E40AF" text-anchor="middle" letter-spacing="1">TEMPORAL GNN STREAM</text>
  </g>

  <g transform="translate(15, 455) rotate(-90)">
    <rect x="-85" y="-12" width="170" height="24" rx="4" fill="#FEF3C7" stroke="#FDE68A" stroke-width="0.8"/>
    <text x="0" y="4" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#92400E" text-anchor="middle" letter-spacing="1">ONTOLOGY TBOX STREAM</text>
  </g>

  <!-- Dividing Subtle Stream Separator -->
  <line x1="45" y1="320" x2="1080" y2="320" stroke="#F1F5F9" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- ==================== 1. STAGE I: INPUT COURT JUDGMENT & GRAPH ==================== -->
  <g transform="translate(45, 40)">
    <!-- Container Card -->
    <rect x="0" y="0" width="230" height="255" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="115" y="22" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0F172A" text-anchor="middle">Supreme Court Narrative</text>
    <text x="115" y="36" font-family="serif" font-size="9" font-style="italic" fill="#64748B" text-anchor="middle">Authentic Civil Disputes (2018–2026)</text>

    <!-- Mini Case Text Extract Box -->
    <rect x="12" y="48" width="206" height="68" rx="5" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    <text x="18" y="64" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#334155">Case Facts (BLDS 2015 Art. 328):</text>
    <text x="18" y="78" font-family="sans-serif" font-size="8" fill="#64748B">"Buyer A deposited 500M VND to Seller B.</text>
    <text x="18" y="90" font-family="sans-serif" font-size="8" fill="#64748B">Closing deadline passed. Dispute filed</text>
    <text x="18" y="102" font-family="serif" font-size="8" font-style="italic" fill="#DC2626">Δt = 1,254 days later without curing."</text>

    <!-- Dynamic Legal Graph Drawing G(t) -->
    <g transform="translate(15, 126)">
      <rect x="0" y="0" width="200" height="115" rx="5" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
      <text x="100" y="16" font-family="serif" font-size="9.5" font-weight="bold" fill="#1E293B" text-anchor="middle">Dynamic Multi-Relational Graph G(t)</text>
      
      <!-- Litigant u (Buyer) -->
      <circle cx="35" cy="55" r="15" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.4"/>
      <text x="35" y="59" font-family="serif" font-size="11" font-style="italic" font-weight="bold" fill="#1D4ED8" text-anchor="middle">u</text>
      <text x="35" y="80" font-family="sans-serif" font-size="7.5" fill="#64748B" text-anchor="middle">Plaintiff</text>

      <!-- Litigant v (Seller) -->
      <circle cx="165" cy="55" r="15" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.4"/>
      <text x="165" y="59" font-family="serif" font-size="11" font-style="italic" font-weight="bold" fill="#1D4ED8" text-anchor="middle">v</text>
      <text x="165" y="80" font-family="sans-serif" font-size="7.5" fill="#64748B" text-anchor="middle">Defendant</text>

      <!-- Directed Forward Edge: Deposit -->
      <path d="M 52 50 L 148 50" stroke="#2563EB" stroke-width="1.4" marker-end="url(#arrBlue)"/>
      <rect x="68" y="38" width="64" height="14" rx="2" fill="#DBEAFE"/>
      <text x="100" y="48" font-family="sans-serif" font-size="7" font-weight="bold" fill="#1E40AF" text-anchor="middle">Deposit (t1)</text>

      <!-- Directed Return Edge: Breach -->
      <path d="M 148 62 L 52 62" stroke="#DC2626" stroke-width="1.4" stroke-dasharray="3,2" marker-end="url(#arrRed)"/>
      <rect x="68" y="64" width="64" height="14" rx="2" fill="#FEE2E2"/>
      <text x="100" y="74" font-family="sans-serif" font-size="7" font-weight="bold" fill="#991B1B" text-anchor="middle">Breach (t2 &gt; t1)</text>

      <!-- Timing Indicator -->
      <text x="100" y="102" font-family="serif" font-size="8" font-style="italic" fill="#475569" text-anchor="middle">Operative Latency: Δt = t_filing - t_breach</text>
    </g>
  </g>

  <!-- Horizontal Dataflow Arrow Stage 1 -> Stage 2 -->
  <line x1="275" y1="165" x2="310" y2="165" stroke="#1E293B" stroke-width="1.4" marker-end="url(#arr)"/>
  <text x="292" y="156" font-family="serif" font-size="9" font-style="italic" fill="#1E293B" text-anchor="middle">G(t), Δt</text>

  <!-- ==================== 2. STAGE II: CONTINUOUS TIME & MULTI-FEATURE ENCODING ==================== -->
  <g transform="translate(315, 30)">
    <!-- Container Card -->
    <rect x="0" y="0" width="220" height="275" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="110" y="20" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0F172A" text-anchor="middle">Multi-Feature Encoders</text>
    <text x="110" y="34" font-family="serif" font-size="8.5" font-style="italic" fill="#64748B" text-anchor="middle">Continuous Bochner Kernel &amp; PhoBERT</text>

    <!-- Card 2.1: Bochner Spectral Kernel with Sine Wave Drawing -->
    <g transform="translate(10, 44)">
      <rect x="0" y="0" width="200" height="80" rx="5" fill="#ECFDF5" stroke="#10B981" stroke-width="1"/>
      <text x="10" y="16" font-family="sans-serif" font-size="9" font-weight="bold" fill="#065F46">Bochner Spectral Time Kernel</text>
      <text x="10" y="28" font-family="serif" font-size="8" font-style="italic" fill="#047857">Φ_d(Δt) = √2/d [cos(ω_k Δt), sin(ω_k Δt)]</text>
      
      <!-- Embedded Sine Wave Curve -->
      <g transform="translate(45, 52)">
        <line x1="-30" y1="0" x2="120" y2="0" stroke="#CBD5E1" stroke-width="0.8"/>
        <line x1="0" y1="-18" x2="0" y2="18" stroke="#CBD5E1" stroke-width="0.8"/>
        <path d="{wave_path}" fill="none" stroke="#10B981" stroke-width="1.8"/>
      </g>
      <rect x="135" y="58" width="55" height="15" rx="2" fill="#D1FAE5"/>
      <text x="162" y="69" font-family="serif" font-size="7.5" font-weight="bold" fill="#065F46" text-anchor="middle">z(t) ∈ R^64</text>
    </g>

    <!-- Card 2.2: PhoBERT Relational Embedding -->
    <g transform="translate(10, 132)">
      <rect x="0" y="0" width="200" height="58" rx="5" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
      <text x="10" y="16" font-family="sans-serif" font-size="9" font-weight="bold" fill="#92400E">Legal Domain Encoder (PhoBERT)</text>
      <text x="10" y="28" font-family="sans-serif" font-size="8" fill="#B45309">Statutory Clause &amp; Relational Context</text>
      <rect x="10" y="36" width="180" height="15" rx="2" fill="#FDE68A"/>
      <text x="100" y="47" font-family="serif" font-size="8" font-weight="bold" fill="#78350F" text-anchor="middle">Relation Embed e_r ∈ R^128</text>
    </g>

    <!-- Card 2.3: Litigant Node State Vectors -->
    <g transform="translate(10, 198)">
      <rect x="0" y="0" width="200" height="65" rx="5" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1"/>
      <text x="10" y="16" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1E40AF">Litigant Covenants &amp; Roles</text>
      <text x="10" y="28" font-family="sans-serif" font-size="8" fill="#1D4ED8">Party Attributes x_u, x_v (768d)</text>
      <rect x="10" y="38" width="180" height="18" rx="2" fill="#DBEAFE"/>
      <text x="100" y="50" font-family="serif" font-size="8" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Patch Vector Z_t = [z(t) || e_r || x_v]</text>
    </g>
  </g>

  <!-- Horizontal Dataflow Arrow Stage 2 -> Stage 3 -->
  <line x1="535" y1="165" x2="570" y2="165" stroke="#1E293B" stroke-width="1.4" marker-end="url(#arr)"/>
  <text x="552" y="156" font-family="serif" font-size="9" font-style="italic" fill="#1E293B" text-anchor="middle">Z_t</text>

  <!-- ==================== 3. STAGE III: AXIOM-TGAT LAYER STACK (× L) ==================== -->
  <g transform="translate(575, 25)">
    <!-- Shadow Card 2 -->
    <rect x="8" y="-8" width="185" height="285" rx="8" fill="#E2E8F0" stroke="#94A3B8" stroke-width="0.8"/>
    <!-- Shadow Card 1 -->
    <rect x="4" y="-4" width="185" height="285" rx="8" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="0.8"/>
    <!-- Main Layer Foreground -->
    <rect x="0" y="0" width="185" height="285" rx="8" fill="#FFFFFF" stroke="#475569" stroke-width="1.4"/>
    <text x="175" y="16" font-family="serif" font-size="11" font-style="italic" font-weight="bold" fill="#475569" text-anchor="end">× L</text>
    <text x="85" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">Axiom-TGAT Layer</text>

    <!-- Bottom LayerNorm -->
    <rect x="15" y="245" width="155" height="26" rx="4" fill="#FEF3C7" stroke="#F59E0B" stroke-width="0.8"/>
    <text x="92" y="262" font-family="sans-serif" font-size="9" font-weight="bold" fill="#92400E" text-anchor="middle">Layer Normalization</text>

    <!-- Arrow Up from LN to Attention -->
    <line x1="92" y1="245" x2="92" y2="218" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>

    <!-- Multi-Head Temporal Attention -->
    <rect x="15" y="170" width="155" height="46" rx="4" fill="#FFEDD5" stroke="#EA580C" stroke-width="1"/>
    <text x="92" y="187" font-family="sans-serif" font-size="9" font-weight="bold" fill="#9A3412" text-anchor="middle">Temporal Graph Attention</text>
    <text x="92" y="201" font-family="serif" font-size="8" font-style="italic" fill="#C2410C" text-anchor="middle">α_uv(t) = Softmax(Q_u (K_v + z(Δt))/√d)</text>

    <!-- Residual 1: Add & Norm Circle -->
    <circle cx="92" cy="142" r="8" fill="#FFFFFF" stroke="#1E293B" stroke-width="1"/>
    <line x1="87" y1="142" x2="97" y2="142" stroke="#1E293B" stroke-width="1"/>
    <line x1="92" y1="137" x2="92" y2="147" stroke="#1E293B" stroke-width="1"/>
    <line x1="92" y1="170" x2="92" y2="152" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>
    <!-- Residual Bypass 1 -->
    <path d="M 92 280 L 92 285 L 178 285 L 178 142 L 102 142" fill="none" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>

    <!-- Middle LayerNorm -->
    <rect x="15" y="102" width="155" height="24" rx="4" fill="#FEF3C7" stroke="#F59E0B" stroke-width="0.8"/>
    <text x="92" y="118" font-family="sans-serif" font-size="9" font-weight="bold" fill="#92400E" text-anchor="middle">Layer Normalization</text>
    <line x1="92" y1="134" x2="92" y2="128" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>

    <!-- Feed-Forward Network -->
    <rect x="15" y="48" width="155" height="40" rx="4" fill="#DBEAFE" stroke="#3B82F6" stroke-width="1"/>
    <text x="92" y="64" font-family="sans-serif" font-size="9" font-weight="bold" fill="#1E40AF" text-anchor="middle">Statutory FFN</text>
    <text x="92" y="78" font-family="serif" font-size="8" font-style="italic" fill="#1D4ED8" text-anchor="middle">Gated State Projection W_s</text>
    <line x1="92" y1="102" x2="92" y2="90" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>

    <!-- Residual 2: Add & Norm Circle -->
    <circle cx="92" cy="28" r="8" fill="#FFFFFF" stroke="#1E293B" stroke-width="1"/>
    <line x1="87" y1="28" x2="97" y2="28" stroke="#1E293B" stroke-width="1"/>
    <line x1="92" y1="23" x2="92" y2="33" stroke="#1E293B" stroke-width="1"/>
    <line x1="92" y1="48" x2="92" y2="38" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>
    <!-- Residual Bypass 2 -->
    <path d="M 92 96 L 178 96 L 178 28 L 102 28" fill="none" stroke="#1E293B" stroke-width="1" marker-end="url(#arr)"/>
  </g>

  <!-- Output Path H(t) from TGAT Top to Fusion Arbiter -->
  <path d="M 667 43 L 667 15 L 835 15 L 835 45" fill="none" stroke="#1E293B" stroke-width="1.4" marker-end="url(#arr)"/>
  <rect x="715" y="4" width="115" height="20" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="772" y="17" font-family="serif" font-size="9.5" font-weight="bold" fill="#1E293B" text-anchor="middle">H(t) ∈ R^(N × 128)</text>

  <!-- ==================== 4. LOWER STREAM: FORMAL ONTOLOGY (VCLO-CORE) & REASONER ==================== -->
  <g transform="translate(45, 345)">
    <!-- Container Card -->
    <rect x="0" y="0" width="490" height="260" rx="8" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.2"/>
    <text x="245" y="22" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#92400E" text-anchor="middle">VCLO-Core OWL 2 DL Formal Ontology &amp; HermiT Reasoner</text>
    <text x="245" y="36" font-family="serif" font-size="9" font-style="italic" fill="#B45309" text-anchor="middle">35 Classes, 233 SROIQ Axioms verified with zero inconsistency (owl:Nothing = ∅)</text>

    <!-- Sub-Box 1: Description Logic TBox Axioms Display -->
    <g transform="translate(15, 48)">
      <rect x="0" y="0" width="225" height="195" rx="5" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1"/>
      <text x="112" y="18" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#78350F" text-anchor="middle">TBox Coded Statutory Axioms</text>

      <!-- Axiom 1: Valid vs Void Disjointness -->
      <rect x="8" y="28" width="209" height="34" rx="3" fill="#FEF3C7"/>
      <text x="14" y="42" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#92400E">Axiom 1: Mutual Disjointness</text>
      <text x="14" y="55" font-family="serif" font-size="8" font-style="italic" fill="#78350F">ValidContract ⊓ VoidAbInitio ⊑ ⊥</text>

      <!-- Axiom 2: Curing Performance (Art 129(2)) -->
      <rect x="8" y="68" width="209" height="42" rx="3" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="0.8"/>
      <text x="14" y="82" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#065F46">Axiom 2: Non-Monotonic Curing (Art 129)</text>
      <text x="14" y="94" font-family="serif" font-size="7.5" font-style="italic" fill="#047857">FormalDefect ⊓ (≥ 0.67 performed)</text>
      <text x="14" y="104" font-family="serif" font-size="7.5" font-style="italic" fill="#047857">  ⊑ ¬VoidAbInitio ⊓ ValidContract</text>

      <!-- Axiom 3: Time Limitation Extinguishment (Art 429) -->
      <rect x="8" y="116" width="209" height="42" rx="3" fill="#FEE2E2" stroke="#FECACA" stroke-width="0.8"/>
      <text x="14" y="130" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#991B1B">Axiom 3: Procedural Bar (Art 429)</text>
      <text x="14" y="142" font-family="serif" font-size="7.5" font-style="italic" fill="#B91C1C">Dispute ⊓ (Δt &gt; 1095d) ⊓ ¬Tolling</text>
      <text x="14" y="152" font-family="serif" font-size="7.5" font-style="italic" fill="#B91C1C">  ⊑ BarredClaim ⊓ ExtinguishedState</text>

      <!-- Reasoner Badge -->
      <rect x="8" y="164" width="209" height="22" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
      <text x="112" y="179" font-family="sans-serif" font-size="8" font-weight="bold" fill="#334155" text-anchor="middle">HermiT Hypertableau: 0 Unsatisfiable</text>
    </g>

    <!-- Sub-Box 2: 4-State Automaton Simulation (M_state) -->
    <g transform="translate(250, 48)">
      <rect x="0" y="0" width="225" height="195" rx="5" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1"/>
      <text x="112" y="18" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#78350F" text-anchor="middle">Markovian State Automaton M_state</text>

      <!-- 4 State Circles -->
      <!-- S0 Valid -->
      <circle cx="45" cy="55" r="18" fill="#ECFDF5" stroke="#10B981" stroke-width="1.4"/>
      <text x="45" y="58" font-family="serif" font-size="9.5" font-weight="bold" fill="#065F46" text-anchor="middle">S0</text>
      <text x="45" y="82" font-family="sans-serif" font-size="7" font-weight="bold" fill="#047857" text-anchor="middle">VALID</text>

      <!-- S1 Voidable -->
      <circle cx="180" cy="55" r="18" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.4"/>
      <text x="180" y="58" font-family="serif" font-size="9.5" font-weight="bold" fill="#92400E" text-anchor="middle">S1</text>
      <text x="180" y="82" font-family="sans-serif" font-size="7" font-weight="bold" fill="#B45309" text-anchor="middle">VOIDABLE</text>

      <!-- S2 Void ab initio -->
      <circle cx="45" cy="135" r="18" fill="#FEF2F2" stroke="#EF4444" stroke-width="1.4"/>
      <text x="45" y="138" font-family="serif" font-size="9.5" font-weight="bold" fill="#991B1B" text-anchor="middle">S2</text>
      <text x="45" y="162" font-family="sans-serif" font-size="7" font-weight="bold" fill="#B91C1C" text-anchor="middle">VOID</text>

      <!-- S3 Extinguished -->
      <circle cx="180" cy="135" r="18" fill="#F1F5F9" stroke="#64748B" stroke-width="1.4"/>
      <text x="180" y="138" font-family="serif" font-size="9.5" font-weight="bold" fill="#334155" text-anchor="middle">S3</text>
      <text x="180" y="162" font-family="sans-serif" font-size="7" font-weight="bold" fill="#475569" text-anchor="middle">EXTINGUISHED</text>

      <!-- Transitions -->
      <!-- S0 -> S1 Breach -->
      <path d="M 64 50 L 160 50" stroke="#D97706" stroke-width="1.2" marker-end="url(#arrAmber)"/>
      <!-- S1 -> S0 Non-Monotonic Curing (Green Dashed) -->
      <path d="M 160 60 L 64 60" stroke="#16A34A" stroke-width="1.6" stroke-dasharray="3,2" marker-end="url(#arrGreen)"/>
      <text x="112" y="72" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#15803D" text-anchor="middle">Cure (Art 129)</text>

      <!-- S1 -> S3 Limitation Bar -->
      <path d="M 180 75 L 180 115" stroke="#64748B" stroke-width="1.2" marker-end="url(#arr)"/>
      <text x="195" y="98" font-family="sans-serif" font-size="6.5" fill="#475569">Art 429</text>

      <!-- S0 -> S2 Absolute Void -->
      <path d="M 45 75 L 45 115" stroke="#EF4444" stroke-width="1.2" marker-end="url(#arrRed)"/>
      <text x="25" y="98" font-family="sans-serif" font-size="6.5" fill="#B91C1C">Art 123</text>

      <!-- State Vector Badge -->
      <rect x="8" y="168" width="209" height="18" rx="3" fill="#FEF3C7"/>
      <text x="112" y="181" font-family="serif" font-size="8" font-style="italic" fill="#92400E" text-anchor="middle">Automaton Gating: s_t ∈ Δ^3</text>
    </g>
  </g>

  <!-- Flow upward from Ontology/Automaton to Normative Fusion Arbiter -->
  <path d="M 535 475 L 790 475 L 790 220" fill="none" stroke="#D97706" stroke-width="1.4" marker-end="url(#arrAmber)"/>
  <rect x="620" y="462" width="125" height="20" rx="3" fill="#FEF3C7" stroke="#FDE68A" stroke-width="0.8"/>
  <text x="682" y="476" font-family="serif" font-size="8.5" font-weight="bold" fill="#92400E" text-anchor="middle">Axiomatic Prior s_t</text>

  <!-- ==================== 5. NORMATIVE HIERARCHY DAG ARBITER (NH-DA) ==================== -->
  <g transform="translate(790, 50)">
    <!-- Container Card -->
    <rect x="0" y="0" width="240" height="240" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
    <text x="120" y="22" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0F172A" text-anchor="middle">Normative Arbiter (NH-DA)</text>
    <text x="120" y="36" font-family="serif" font-size="8.5" font-style="italic" fill="#64748B" text-anchor="middle">Lex Specialis &amp; Precedence DAG</text>

    <!-- Precedence Rules -->
    <g transform="translate(12, 48)">
      <rect x="0" y="0" width="216" height="52" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
      <text x="10" y="16" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1E293B">Statutory Hierarchy Precedence:</text>
      <text x="10" y="30" font-family="serif" font-size="8" font-style="italic" fill="#2563EB">• Land Law 2024 ≻ BLDS 2015 (Art 156)</text>
      <text x="10" y="42" font-family="serif" font-size="8" font-style="italic" fill="#D97706">• Usury Cap ceiling: r ≤ 20%/yr (Art 468)</text>
    </g>

    <!-- Gated Embedding Fusion -->
    <g transform="translate(12, 108)">
      <rect x="0" y="0" width="216" height="56" rx="4" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
      <text x="10" y="16" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#1E40AF">Neuro-Symbolic Gated Fusion:</text>
      <text x="10" y="32" font-family="serif" font-size="8" font-style="italic" fill="#1D4ED8">h_G* = h_G ⊙ (1 + σ(W_g h_G) · w_domain)</text>
      <text x="10" y="46" font-family="sans-serif" font-size="7.5" fill="#1E3A8A">Enforces Lex Specialis in Latent Space</text>
    </g>

    <!-- Axiomatic Regularizer Output -->
    <rect x="12" y="172" width="216" height="56" rx="4" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1"/>
    <text x="10" y="188" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#6B21A8">Axiomatic TBox Regularizer:</text>
    <text x="10" y="202" font-family="serif" font-size="8" font-style="italic" fill="#7E22CE">L_total = L_task + λ_onto L_onto + λ_state L_state</text>
    <text x="10" y="218" font-family="sans-serif" font-size="7.5" fill="#581C87">HermiT Certified Compliance: 99.12% LCR</text>
  </g>

  <!-- Flow Arrow from NH-DA to Dung Defeasible Head -->
  <line x1="1030" y1="165" x2="1065" y2="165" stroke="#1E293B" stroke-width="1.4" marker-end="url(#arr)"/>

  <!-- ==================== 6. DEFEASIBLE DUNG REASONER & FINAL VERDICT ==================== -->
  <g transform="translate(1070, 35)">
    <!-- Container Card (Soft Coral / Red) -->
    <rect x="0" y="0" width="340" height="265" rx="8" fill="#FFF1F2" stroke="#BE123C" stroke-width="1.4"/>
    <text x="170" y="22" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#9F1239" text-anchor="middle">Dung Defeasible Head &amp; Adjudication</text>
    <text x="170" y="36" font-family="serif" font-size="8.5" font-style="italic" fill="#BE123C" text-anchor="middle">Abstract Argumentation Framework AF = ⟨A, R_defeat⟩ (Dung 1995)</text>

    <!-- Argument Dispute Graph -->
    <g transform="translate(15, 48)">
      <!-- Argument Bar (Procedural) -->
      <rect x="0" y="0" width="135" height="52" rx="4" fill="#FFFFFF" stroke="#BE123C" stroke-width="1.2"/>
      <text x="67" y="16" font-family="serif" font-size="10" font-weight="bold" fill="#9F1239" text-anchor="middle">A_bar (Procedural)</text>
      <text x="67" y="28" font-family="sans-serif" font-size="7.5" fill="#64748B" text-anchor="middle">Lapse Δt &gt; 1095d (Art 429)</text>
      <rect x="10" y="34" width="115" height="14" rx="2" fill="#DCFCE7"/>
      <text x="67" y="44" font-family="sans-serif" font-size="7" font-weight="bold" fill="#166534" text-anchor="middle">STATUS: ACCEPTED</text>

      <!-- Asymmetric Defeat Arrow -->
      <line x1="138" y1="26" x2="167" y2="26" stroke="#DC2626" stroke-width="1.8" marker-end="url(#arrRed)"/>
      <text x="152" y="20" font-family="sans-serif" font-size="7" font-weight="bold" fill="#DC2626" text-anchor="middle">def</text>

      <!-- Argument Claim (Substantive) -->
      <rect x="172" y="0" width="135" height="52" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
      <text x="240" y="16" font-family="serif" font-size="10" font-weight="bold" fill="#475569" text-anchor="middle">A_claim (Substantive)</text>
      <text x="240" y="28" font-family="sans-serif" font-size="7.5" fill="#64748B" text-anchor="middle">Double Deposit Penalty (Art 328)</text>
      <rect x="182" y="34" width="115" height="14" rx="2" fill="#FEE2E2"/>
      <text x="240" y="44" font-family="sans-serif" font-size="7" font-weight="bold" fill="#991B1B" text-anchor="middle">STATUS: DEFEATED</text>
    </g>

    <!-- Grounded Extension Mathematical Resolution -->
    <g transform="translate(15, 110)">
      <rect x="0" y="0" width="310" height="40" rx="4" fill="#FFFFFF" stroke="#FECDD3" stroke-width="1"/>
      <text x="155" y="18" font-family="serif" font-size="10.5" font-weight="bold" fill="#9F1239" text-anchor="middle">GE(AF) = lfp(F_AF) = {{ A_bar }}</text>
      <text x="155" y="32" font-family="sans-serif" font-size="8" fill="#475569" text-anchor="middle">Unique Minimal Fixed Point: Procedural Bar overrules Substantive Claim</text>
    </g>

    <!-- Final Judicial Verdict Box -->
    <g transform="translate(15, 160)">
      <rect x="0" y="0" width="310" height="92" rx="5" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.4"/>
      <text x="155" y="20" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#166534" text-anchor="middle">FINAL JUDICIAL VERDICT (y*)</text>
      
      <!-- Decree Badge -->
      <rect x="12" y="28" width="286" height="26" rx="3" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="155" y="45" font-family="sans-serif" font-size="10" font-weight="bold" fill="#14532D" text-anchor="middle">✓ DISMISS: STATUTE OF LIMITATIONS EXPIRED (Art. 429)</text>

      <!-- Empirical Metrics Row -->
      <g transform="translate(12, 62)">
        <rect x="0" y="0" width="138" height="22" rx="3" fill="#F0FDF4"/>
        <text x="69" y="15" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#166534" text-anchor="middle">Hits@1: 86.41 ± 0.38%</text>

        <rect x="148" y="0" width="138" height="22" rx="3" fill="#F0FDF4"/>
        <text x="217" y="15" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#166534" text-anchor="middle">Latency: 1.5 ms (A30 GPU)</text>
      </g>
    </g>
  </g>

  <!-- ==================== 7. AXIOMATIC GRADIENT FEEDBACK LOOP ==================== -->
  <path d="M 1240 300 L 1240 640 L 667 640 L 667 315" fill="none" stroke="#7C3AED" stroke-width="1.8" stroke-dasharray="4,3" marker-end="url(#arrPurple)"/>
  <rect x="800" y="628" width="340" height="24" rx="4" fill="#F3E8FF" stroke="#D8B4FE" stroke-width="1"/>
  <text x="970" y="644" font-family="sans-serif" font-size="9" font-weight="bold" fill="#6B21A8" text-anchor="middle">Backward Gradient Feedback: ∇ L_onto + ∇ L_state (TBox Margin Consistency)</text>

</svg>"""
    return svg

def build_assets():
    svg_code = generate_fig1_ultra_svg()
    with open('synapselex/paper/figures/fig1_system_architecture.svg', 'w', encoding='utf-8') as f:
        f.write(svg_code)
    print("Saved ultra-refined fig1_system_architecture.svg")

    doc = fitz.open(stream=svg_code.encode('utf-8'), filetype='svg')
    pdf_bytes = doc.convert_to_pdf()
    
    with open('synapselex/paper/figures/fig1_system_architecture.pdf', 'wb') as f:
        f.write(pdf_bytes)
    print("Saved fig1_system_architecture.pdf (Ultra Vector)")

    pdf_doc = fitz.open('pdf', pdf_bytes)
    page = pdf_doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save('synapselex/paper/figures/fig1_system_architecture.png')
    pix.save('paper_figures/fig1_system_architecture.png')
    print("Saved fig1_system_architecture.png (300 DPI high-res)")

if __name__ == '__main__':
    build_assets()
