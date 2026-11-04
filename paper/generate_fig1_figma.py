"""
Generate Figma-Grade Figure 1: SynapseLex System Architecture & Pipeline.
Uses pure SVG vector elements with explicit attributes (solid fills, crisp rounded cards,
readable typography, and clear dataflow routing) ensuring 100% perfect rendering in PyMuPDF.
"""
import fitz

def generate_fig1_svg():
    width = 1440
    height = 760
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <!-- Definitions for Markers -->
  <defs>
    <marker id="arrSky" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#0284C7"/>
    </marker>
    <marker id="arrIndigo" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#4F46E5"/>
    </marker>
    <marker id="arrAmber" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#D97706"/>
    </marker>
    <marker id="arrRose" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#BE123C"/>
    </marker>
    <marker id="arrPurple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#7C3AED"/>
    </marker>
  </defs>

  <!-- Background Canvas -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" rx="16" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Top Title Banner -->
  <g transform="translate(30, 22)">
    <text x="0" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="bold" fill="#0F172A">SynapseLex: Neuro-Symbolic Temporal State-Transition Architecture</text>
    <text x="0" y="40" font-family="system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="500" fill="#475569">End-to-End Pipeline: Dynamic Case Graph Stream ➔ Inductive Spectral Attention ➔ Normative Axiomatic Governance ➔ Defeasible Adjudication</text>
  </g>

  <!-- ==================== STAGE 1: GRAPH FORMATION ==================== -->
  <g transform="translate(30, 75)">
    <!-- Column Container -->
    <rect x="0" y="0" width="310" height="605" rx="12" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.8"/>
    <!-- Stage Header Pill -->
    <rect x="0" y="0" width="310" height="42" rx="12" fill="#0284C7"/>
    <rect x="0" y="24" width="310" height="18" fill="#0284C7"/>
    <text x="155" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">STAGE 1: GRAPH FORMATION</text>

    <!-- Card 1.1: Authentic Case Narrative -->
    <g transform="translate(14, 54)">
      <rect x="0" y="0" width="282" height="150" rx="8" fill="#F0F9FF" stroke="#E0F2FE" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#0284C7"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">§</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#0369A1">Authentic Court Judgment</text>
      
      <text x="12" y="54" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">Extracts factual narrative &amp; procedural</text>
      <text x="12" y="72" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">chronology from Supreme Court gazette</text>
      <text x="12" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">(congbobanan.toaan.gov.vn, 2018–2026).</text>
      
      <rect x="12" y="112" width="122" height="22" rx="5" fill="#E0F2FE"/>
      <text x="73" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">N = 2,840 Judgments</text>
      <rect x="142" y="112" width="128" height="22" rx="5" fill="#E0F2FE"/>
      <text x="206" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">Supreme Court Gazette</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="214" x2="155" y2="236" stroke="#0284C7" stroke-width="2" marker-end="url(#arrSky)"/>

    <!-- Card 1.2: Event & Entity Parsing -->
    <g transform="translate(14, 242)">
      <rect x="0" y="0" width="282" height="142" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#0EA5E9"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">⚙</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Temporal Event &amp; Entity Parser</text>
      
      <text x="12" y="54" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">Extracts litigants, contractual covenants,</text>
      <text x="12" y="72" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">breaches, and exact operative dates with</text>
      <text x="12" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">strict forward-chaining chronology.</text>

      <rect x="12" y="108" width="122" height="22" rx="5" fill="#F1F5F9"/>
      <text x="73" y="123" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">PhoBERT Embed (768d)</text>
      <rect x="142" y="108" width="128" height="22" rx="5" fill="#FEF3C7"/>
      <text x="206" y="123" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#B45309" text-anchor="middle">Zero Leakage (p=0.00)</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="394" x2="155" y2="416" stroke="#0284C7" stroke-width="2" marker-end="url(#arrSky)"/>

    <!-- Card 1.3: Dynamic Graph -->
    <g transform="translate(14, 422)">
      <rect x="0" y="0" width="282" height="168" rx="8" fill="#F0F9FF" stroke="#E0F2FE" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#0284C7"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">☍</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#0369A1">Dynamic Case Graph G(t)</text>
      
      <!-- Graph Drawing -->
      <g transform="translate(15, 46)">
        <circle cx="35" cy="35" r="18" fill="#FFFFFF" stroke="#0284C7" stroke-width="2"/>
        <text x="35" y="39" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">Buyer</text>
        
        <circle cx="215" cy="35" r="18" fill="#FFFFFF" stroke="#0284C7" stroke-width="2"/>
        <text x="215" y="39" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0369A1" text-anchor="middle">Seller</text>

        <path d="M 55 35 L 195 35" stroke="#0284C7" stroke-width="2" marker-end="url(#arrSky)"/>
        <rect x="75" y="22" width="100" height="18" rx="4" fill="#E0F2FE"/>
        <text x="125" y="35" font-family="sans-serif" font-size="9" font-weight="bold" fill="#0369A1" text-anchor="middle">Deposit (t1, Art 328)</text>

        <path d="M 195 45 Q 125 80 55 45" fill="none" stroke="#EF4444" stroke-width="1.8" stroke-dasharray="3,3"/>
        <rect x="75" y="68" width="100" height="18" rx="4" fill="#FEE2E2"/>
        <text x="125" y="81" font-family="sans-serif" font-size="9" font-weight="bold" fill="#B91C1C" text-anchor="middle">Breach (t2 &gt; t1)</text>
      </g>
      
      <rect x="12" y="136" width="258" height="20" rx="4" fill="#E0F2FE"/>
      <text x="141" y="150" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#0369A1" text-anchor="middle">Timed Nodes V, Timed Edges E(t)</text>
    </g>
  </g>

  <!-- Flow Connector 1 -> 2 -->
  <g transform="translate(348, 360)">
    <line x1="0" y1="0" x2="38" y2="0" stroke="#4F46E5" stroke-width="3" marker-end="url(#arrIndigo)"/>
    <rect x="-8" y="-24" width="54" height="18" rx="4" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1"/>
    <text x="19" y="-11" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#4F46E5" text-anchor="middle">G(t), Δt</text>
  </g>

  <!-- ==================== STAGE 2: TEMPORAL ATTENTION ==================== -->
  <g transform="translate(395, 75)">
    <!-- Column Container -->
    <rect x="0" y="0" width="310" height="605" rx="12" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.8"/>
    <!-- Stage Header Pill -->
    <rect x="0" y="0" width="310" height="42" rx="12" fill="#4F46E5"/>
    <rect x="0" y="24" width="310" height="18" fill="#4F46E5"/>
    <text x="155" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">STAGE 2: TEMPORAL ATTENTION</text>

    <!-- Card 2.1: Bochner Spectral Kernel -->
    <g transform="translate(14, 54)">
      <rect x="0" y="0" width="282" height="150" rx="8" fill="#EEF2FF" stroke="#E0E7FF" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#4F46E5"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">∿</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#3730A3">Bochner Spectral Time Kernel</text>
      
      <text x="12" y="54" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">Projects continuous elapsed latency Δt</text>
      <text x="12" y="72" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">into harmonic Fourier space (R^64).</text>
      <text x="12" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">Captures quarantine tolling smoothly.</text>

      <rect x="12" y="112" width="122" height="22" rx="5" fill="#E0E7FF"/>
      <text x="73" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#3730A3" text-anchor="middle">Dual-Clock: Δt + τ(t)</text>
      <rect x="142" y="112" width="128" height="22" rx="5" fill="#E0E7FF"/>
      <text x="206" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#3730A3" text-anchor="middle">Fourier Dim: 64</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="214" x2="155" y2="236" stroke="#4F46E5" stroke-width="2" marker-end="url(#arrIndigo)"/>

    <!-- Card 2.2: Axiom-TGAT Attention -->
    <g transform="translate(14, 242)">
      <rect x="0" y="0" width="282" height="152" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#6366F1"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">⊞</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#1E293B">Axiom-TGAT Multi-Head Attention</text>
      
      <text x="12" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">Temporal neighborhood inductive routing:</text>
      
      <!-- Formula Box -->
      <rect x="12" y="64" width="258" height="34" rx="5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
      <text x="141" y="85" font-family="serif" font-size="11.5" font-style="italic" fill="#1E293B" text-anchor="middle">α(u,v,t) = Softmax( Q_u (K_v + Φ(Δt)) / √d )</text>

      <rect x="12" y="112" width="122" height="22" rx="5" fill="#EEF2FF"/>
      <text x="73" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#4338CA" text-anchor="middle">4 Attention Heads</text>
      <rect x="142" y="112" width="128" height="22" rx="5" fill="#EEF2FF"/>
      <text x="206" y="127" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#4338CA" text-anchor="middle">Inductive Message</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="404" x2="155" y2="426" stroke="#4F46E5" stroke-width="2" marker-end="url(#arrIndigo)"/>

    <!-- Card 2.3: Contextual Representation -->
    <g transform="translate(14, 432)">
      <rect x="0" y="0" width="282" height="158" rx="8" fill="#EEF2FF" stroke="#E0E7FF" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#4F46E5"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">▥</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#3730A3">Dynamic Case Embedding H(t)</text>
      
      <text x="12" y="54" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">Synthesizes temporal litigant interactions,</text>
      <text x="12" y="72" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">statutory covenants, and breach delays</text>
      <text x="12" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#334155">into continuous contextual embeddings.</text>

      <rect x="12" y="118" width="258" height="24" rx="5" fill="#E0E7FF"/>
      <text x="141" y="134" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#3730A3" text-anchor="middle">Context Tensor: H(t) ∈ R^(N × 128)</text>
    </g>
  </g>

  <!-- Flow Connector 2 -> 3 -->
  <g transform="translate(713, 360)">
    <line x1="0" y1="0" x2="38" y2="0" stroke="#D97706" stroke-width="3" marker-end="url(#arrAmber)"/>
    <rect x="-8" y="-24" width="54" height="18" rx="4" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
    <text x="19" y="-11" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#D97706" text-anchor="middle">H(t)</text>
  </g>

  <!-- ==================== STAGE 3: NORMATIVE GOVERNANCE ==================== -->
  <g transform="translate(760, 75)">
    <!-- Column Container -->
    <rect x="0" y="0" width="310" height="605" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.8"/>
    <!-- Stage Header Pill -->
    <rect x="0" y="0" width="310" height="42" rx="12" fill="#D97706"/>
    <rect x="0" y="24" width="310" height="18" fill="#D97706"/>
    <text x="155" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">STAGE 3: NORMATIVE GOVERNANCE</text>

    <!-- Card 3.1: Normative Hierarchy DAG -->
    <g transform="translate(14, 54)">
      <rect x="0" y="0" width="282" height="142" rx="8" fill="#FFFBEB" stroke="#FEF3C7" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#D97706"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">⚖</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#92400E">Normative Hierarchy DAG (NH-DA)</text>
      
      <text x="12" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">Resolves conflicts by statutory precedence:</text>
      <text x="12" y="70" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#78350F">• Lex Specialis: Land Law 2024 ≻ BLDS 2015</text>
      <text x="12" y="88" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#78350F">• Usury Cap: Art. 468 ceiling (20%/year)</text>

      <rect x="12" y="106" width="122" height="22" rx="5" fill="#FEF3C7"/>
      <text x="73" y="121" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#92400E" text-anchor="middle">Deterministic DAG</text>
      <rect x="142" y="106" width="128" height="22" rx="5" fill="#FEF3C7"/>
      <text x="206" y="121" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="bold" fill="#92400E" text-anchor="middle">Conflict Resolution</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="206" x2="155" y2="228" stroke="#D97706" stroke-width="2" marker-end="url(#arrAmber)"/>

    <!-- Card 3.2: 4-State Automaton -->
    <g transform="translate(14, 234)">
      <rect x="0" y="0" width="282" height="210" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#F59E0B"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">⇄</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#1E293B">Contract State Automaton (M_state)</text>
      <text x="12" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">4 discrete states under BLDS 2015:</text>

      <!-- 4 State Pills Grid -->
      <g transform="translate(12, 60)">
        <rect x="0" y="0" width="124" height="34" rx="5" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.2"/>
        <text x="62" y="16" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#065F46" text-anchor="middle">S0: VALID</text>
        <text x="62" y="28" font-family="sans-serif" font-size="8.5" fill="#047857" text-anchor="middle">Enforceable (Art 398)</text>

        <rect x="134" y="0" width="124" height="34" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1.2"/>
        <text x="196" y="16" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#92400E" text-anchor="middle">S1: VOIDABLE</text>
        <text x="196" y="28" font-family="sans-serif" font-size="8.5" fill="#B45309" text-anchor="middle">Formal Defect (Art 129)</text>

        <rect x="0" y="40" width="124" height="34" rx="5" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.2"/>
        <text x="62" y="56" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#991B1B" text-anchor="middle">S2: VOID AB INITIO</text>
        <text x="62" y="68" font-family="sans-serif" font-size="8.5" fill="#B91C1C" text-anchor="middle">Prohibited (Art 123)</text>

        <rect x="134" y="40" width="124" height="34" rx="5" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
        <text x="196" y="56" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#334155" text-anchor="middle">S3: EXTINGUISHED</text>
        <text x="196" y="68" font-family="sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Lapsed &gt;1095d (Art 429)</text>
      </g>

      <!-- Non-Monotonic Curing Banner -->
      <rect x="12" y="152" width="258" height="42" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
      <text x="141" y="169" font-family="sans-serif" font-size="10" font-weight="bold" fill="#B45309" text-anchor="middle">Non-Monotonic Curing: S1 ➔ S0</text>
      <text x="141" y="184" font-family="sans-serif" font-size="9.5" fill="#78350F" text-anchor="middle">if ≥ 2/3 performance completed (Art. 129(2))</text>
    </g>

    <!-- Down Connector -->
    <line x1="155" y1="454" x2="155" y2="476" stroke="#D97706" stroke-width="2" marker-end="url(#arrAmber)"/>

    <!-- Card 3.3: Description Logic TBox -->
    <g transform="translate(14, 482)">
      <rect x="0" y="0" width="282" height="108" rx="8" fill="#FFFBEB" stroke="#FEF3C7" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#D97706"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">🛡</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#92400E">OWL 2 DL Ontology (VCLO-Core)</text>
      
      <text x="12" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">35 Classes, 233 SROIQ Axioms verified</text>
      <text x="12" y="70" font-family="system-ui, -apple-system, sans-serif" font-size="11.5" fill="#475569">by HermiT Reasoner: Zero Incoherence.</text>

      <rect x="12" y="82" width="258" height="18" rx="4" fill="#FEF3C7"/>
      <text x="141" y="95" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#92400E" text-anchor="middle">HermiT Checked: 0 Unsatisfiable Classes</text>
    </g>
  </g>

  <!-- Flow Connector 3 -> 4 -->
  <g transform="translate(1078, 360)">
    <line x1="0" y1="0" x2="38" y2="0" stroke="#BE123C" stroke-width="3" marker-end="url(#arrRose)"/>
    <rect x="-8" y="-24" width="54" height="18" rx="4" fill="#FFE4E6" stroke="#FECDD3" stroke-width="1"/>
    <text x="19" y="-11" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#BE123C" text-anchor="middle">s_t, AF</text>
  </g>

  <!-- ==================== STAGE 4: DEFEASIBLE VERDICT ==================== -->
  <g transform="translate(1125, 75)">
    <!-- Column Container -->
    <rect x="0" y="0" width="285" height="605" rx="12" fill="#FFFFFF" stroke="#FECDD3" stroke-width="1.8"/>
    <!-- Stage Header Pill -->
    <rect x="0" y="0" width="285" height="42" rx="12" fill="#BE123C"/>
    <rect x="0" y="24" width="285" height="18" fill="#BE123C"/>
    <text x="142" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">STAGE 4: DEFEASIBLE VERDICT</text>

    <!-- Card 4.1: Dung Defeasible Head -->
    <g transform="translate(12, 54)">
      <rect x="0" y="0" width="261" height="175" rx="8" fill="#FFF1F2" stroke="#FFE4E6" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#BE123C"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">⚔</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="bold" fill="#9F1239">Dung Defeasible Head</text>
      
      <text x="12" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#475569">Resolves asymmetric claim defeat:</text>

      <!-- Argumentation Graph Nodes -->
      <g transform="translate(8, 60)">
        <rect x="0" y="0" width="105" height="42" rx="5" fill="#FFFFFF" stroke="#BE123C" stroke-width="1.5"/>
        <text x="52" y="16" font-family="sans-serif" font-size="9" font-weight="bold" fill="#9F1239" text-anchor="middle">A_bar (Procedural)</text>
        <text x="52" y="27" font-family="sans-serif" font-size="8" fill="#475569" text-anchor="middle">Lapse &gt; 1095d</text>
        <text x="52" y="37" font-family="sans-serif" font-size="8" font-weight="bold" fill="#047857" text-anchor="middle">ACCEPTED</text>

        <path d="M 108 21 L 132 21" stroke="#BE123C" stroke-width="2.2" marker-end="url(#arrRose)"/>

        <rect x="138" y="0" width="105" height="42" rx="5" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2"/>
        <text x="190" y="16" font-family="sans-serif" font-size="9" font-weight="bold" fill="#475569" text-anchor="middle">A_claim (Substantive)</text>
        <text x="190" y="27" font-family="sans-serif" font-size="8" fill="#64748B" text-anchor="middle">Deposit Penalty</text>
        <text x="190" y="37" font-family="sans-serif" font-size="8" font-weight="bold" fill="#DC2626" text-anchor="middle">DEFEATED</text>
      </g>

      <!-- Grounded Extension Formula -->
      <rect x="8" y="118" width="245" height="45" rx="5" fill="#FFFFFF" stroke="#FECDD3" stroke-width="1"/>
      <text x="130" y="136" font-family="serif" font-size="11" font-weight="bold" fill="#9F1239" text-anchor="middle">GE(AF) = lfp(F_AF) = {{ A_bar }}</text>
      <text x="130" y="152" font-family="sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Grounded Extension guarantees 0 remedy bias</text>
    </g>

    <!-- Down Connector -->
    <line x1="142" y1="239" x2="142" y2="259" stroke="#BE123C" stroke-width="2" marker-end="url(#arrRose)"/>

    <!-- Card 4.2: Certified Judicial Verdict -->
    <g transform="translate(12, 265)">
      <rect x="0" y="0" width="261" height="152" rx="8" fill="#F0FDF4" stroke="#DCFCE7" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#16A34A"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">✓</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="bold" fill="#166534">Judicial Verdict (y*)</text>
      
      <!-- Verdict Options -->
      <g transform="translate(8, 48)">
        <rect x="0" y="0" width="245" height="24" rx="4" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1"/>
        <text x="8" y="16" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#166534">✓ DISMISS: Statute Lapsed (Art. 429)</text>

        <rect x="0" y="28" width="245" height="20" rx="4" fill="#F1F5F9"/>
        <text x="8" y="42" font-family="sans-serif" font-size="9" fill="#64748B">✗ Enforce Deposit Penalty (Defeated)</text>

        <rect x="0" y="52" width="245" height="20" rx="4" fill="#F1F5F9"/>
        <text x="8" y="66" font-family="sans-serif" font-size="9" fill="#64748B">✗ Order Contract Curing (Inapplicable)</text>
      </g>
      
      <rect x="8" y="122" width="118" height="22" rx="4" fill="#DCFCE7"/>
      <text x="67" y="136" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#166534" text-anchor="middle">Hits@1: 86.41%</text>
      <rect x="134" y="122" width="118" height="22" rx="4" fill="#DCFCE7"/>
      <text x="193" y="136" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#166534" text-anchor="middle">Latency: 1.5 ms</text>
    </g>

    <!-- Down Connector -->
    <line x1="142" y1="427" x2="142" y2="447" stroke="#BE123C" stroke-width="2" marker-end="url(#arrRose)"/>

    <!-- Card 4.3: Description Logic Loss -->
    <g transform="translate(12, 453)">
      <rect x="0" y="0" width="261" height="137" rx="8" fill="#FAF5FF" stroke="#F3E8FF" stroke-width="1.2"/>
      <rect x="12" y="12" width="24" height="24" rx="5" fill="#7C3AED"/>
      <text x="24" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">∇</text>
      <text x="44" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="bold" fill="#581C87">Axiomatic Regularization Loss</text>
      
      <rect x="8" y="46" width="245" height="28" rx="4" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="1"/>
      <text x="130" y="64" font-family="serif" font-size="9.5" font-style="italic" fill="#581C87" text-anchor="middle">L_total = L_task + λ_onto L_onto + λ_state L_state</text>
      
      <text x="8" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#475569">Backpropagates margin violations of</text>
      <text x="8" y="104" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#475569">HermiT OWL 2 DL axioms into TGAT.</text>

      <rect x="8" y="112" width="245" height="18" rx="4" fill="#F3E8FF"/>
      <text x="130" y="125" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#6B21A8" text-anchor="middle">Certified Compliance: 99.12% LCR</text>
    </g>
  </g>

  <!-- ==================== BACKWARD FEEDBACK ARROW ==================== -->
  <g transform="translate(0, 0)">
    <path d="M 1250 680 L 1250 720 L 550 720 L 550 680" fill="none" stroke="#7C3AED" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrPurple)"/>
    <rect x="740" y="708" width="320" height="22" rx="4" fill="#F3E8FF" stroke="#D8B4FE" stroke-width="1"/>
    <text x="900" y="723" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#6B21A8" text-anchor="middle">Axiomatic Feedback: ∇ L_onto + ∇ L_state (HermiT TBox Consistency)</text>
  </g>

</svg>"""
    return svg

def build_assets():
    svg_code = generate_fig1_svg()
    with open('synapselex/paper/figures/fig1_system_architecture.svg', 'w', encoding='utf-8') as f:
        f.write(svg_code)
    print("Saved fig1_system_architecture.svg")

    doc = fitz.open(stream=svg_code.encode('utf-8'), filetype='svg')
    pdf_bytes = doc.convert_to_pdf()
    
    with open('synapselex/paper/figures/fig1_system_architecture.pdf', 'wb') as f:
        f.write(pdf_bytes)
    print("Saved fig1_system_architecture.pdf (Vector)")

    pdf_doc = fitz.open('pdf', pdf_bytes)
    page = pdf_doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save('synapselex/paper/figures/fig1_system_architecture.png')
    pix.save('paper_figures/fig1_system_architecture.png')
    print("Saved fig1_system_architecture.png (300 DPI high-res)")

if __name__ == '__main__':
    build_assets()
