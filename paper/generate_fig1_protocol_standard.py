import os
import fitz

def generate_standard_protocol_figure():
    width = 1200
    height = 360
    
    # Precise geometry coordinates
    # u, v nodes
    u_x, u_y = 40, 75
    v_x, v_y = 40, 285
    
    # Extract boxes
    ext_w, ext_h = 108, 48
    ext_x = 80
    ext_u_y = u_y - ext_h / 2
    ext_v_y = v_y - ext_h / 2
    
    # Encoders
    enc_w, enc_h = 142, 54
    enc_x = 285
    enc_top_y = u_y - enc_h / 2
    enc_mid_y = 180 - enc_h / 2
    enc_bot_y = v_y - enc_h / 2
    
    # Token columns
    tok_x = 472
    
    # Patching boxes
    pat_w, pat_h = 112, 54
    pat_x = 525
    pat_top_y = u_y - pat_h / 2
    pat_bot_y = v_y - pat_h / 2
    
    # Transformer block
    tr_x, tr_y = 755, 20
    tr_w, tr_h = 165, 320
    
    # Right column (Average Pooling & Downstream)
    head_x = 1030
    pool_w, pool_h = 95, 42
    pool_x = head_x - pool_w / 2
    pool_y = 75
    
    down_w, down_h = 115, 48
    down_x = head_x - down_w / 2
    down_y = 225

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#1E293B"/>
    </marker>
    <style>
      .txt-serif {{ font-family: 'Times New Roman', Times, serif; font-style: italic; }}
      .txt-sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .box-title {{ font-size: 10px; font-weight: 600; text-anchor: middle; }}
      .math-lbl {{ font-size: 13px; font-weight: bold; fill: #0F172A; text-anchor: middle; }}
    </style>
  </defs>

  <!-- Clean Canvas -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>

  <!-- ==================== 1. LEFT: QUERY NODES & DYNAMIC GRAPH ==================== -->
  <!-- Node u -->
  <circle cx="{u_x}" cy="{u_y}" r="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.6"/>
  <text x="{u_x}" y="{u_y + 5}" class="txt-serif" font-size="14" font-weight="bold" fill="#1E293B" text-anchor="middle">u</text>

  <!-- Node v -->
  <circle cx="{v_x}" cy="{v_y}" r="12" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.6"/>
  <text x="{v_x}" y="{v_y + 5}" class="txt-serif" font-size="14" font-weight="bold" fill="#1E293B" text-anchor="middle">v</text>

  <!-- Dashed Link u-v with t? -->
  <line x1="{u_x}" y1="{u_y + 13}" x2="{u_x}" y2="162" stroke="#2563EB" stroke-width="1.2" stroke-dasharray="3,3"/>
  <line x1="{u_x}" y1="198" x2="{u_x}" y2="{v_y - 13}" stroke="#2563EB" stroke-width="1.2" stroke-dasharray="3,3"/>
  <text x="{u_x}" y="184" class="txt-serif" font-size="12.5" font-weight="bold" fill="#DC2626" text-anchor="middle">t?</text>

  <!-- Dynamic Graph Icon -->
  <g transform="translate(100, 140)">
    <circle cx="16" cy="22" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <circle cx="42" cy="10" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <circle cx="34" cy="44" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <circle cx="64" cy="26" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <circle cx="80" cy="50" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <circle cx="56" cy="65" r="4.2" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    
    <line x1="20" y1="20" x2="38" y2="12" stroke="#64748B" stroke-width="1.1"/>
    <line x1="19" y1="26" x2="31" y2="41" stroke="#64748B" stroke-width="1.1"/>
    <line x1="46" y1="13" x2="60" y2="23" stroke="#64748B" stroke-width="1.1"/>
    <line x1="38" y1="42" x2="60" y2="29" stroke="#64748B" stroke-width="1.1"/>
    <line x1="68" y1="30" x2="77" y2="47" stroke="#64748B" stroke-width="1.1"/>
    <line x1="38" y1="46" x2="52" y2="63" stroke="#64748B" stroke-width="1.1"/>
    <line x1="60" y1="64" x2="77" y2="53" stroke="#64748B" stroke-width="1.1"/>
    
    <text x="48" y="86" class="txt-sans" font-size="10.5" font-weight="600" fill="#334155" text-anchor="middle">Dynamic Graph</text>
  </g>

  <!-- Arrows from u, v to Extract boxes -->
  <line x1="{u_x + 13}" y1="{u_y}" x2="{ext_x - 2}" y2="{u_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="{v_x + 13}" y1="{v_y}" x2="{ext_x - 2}" y2="{v_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Vertical Arrows from Graph to Extract boxes -->
  <line x1="135" y1="138" x2="135" y2="{ext_u_y + ext_h + 3}" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>
  <line x1="135" y1="222" x2="135" y2="{ext_v_y - 3}" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- ==================== 2. EXTRACT FIRST-HOP INTERACTIONS ==================== -->
  <!-- Box u (Lavender) -->
  <rect x="{ext_x}" y="{ext_u_y}" width="{ext_w}" height="{ext_h}" rx="8" fill="#E8D7F1" stroke="#8E6CA8" stroke-width="1.2"/>
  <text x="{ext_x + ext_w/2}" y="{ext_u_y + 20}" class="txt-sans box-title" fill="#2E1045">Extract First-</text>
  <text x="{ext_x + ext_w/2}" y="{ext_u_y + 34}" class="txt-sans box-title" fill="#2E1045">hop Interactions</text>

  <line x1="{ext_x + ext_w}" y1="{u_y}" x2="{ext_x + ext_w + 22}" y2="{u_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="{ext_x + ext_w + 35}" y="{u_y + 4}" class="txt-serif math-lbl">S<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u</tspan></text>

  <!-- Box v (Lavender) -->
  <rect x="{ext_x}" y="{ext_v_y}" width="{ext_w}" height="{ext_h}" rx="8" fill="#E8D7F1" stroke="#8E6CA8" stroke-width="1.2"/>
  <text x="{ext_x + ext_w/2}" y="{ext_v_y + 20}" class="txt-sans box-title" fill="#2E1045">Extract First-</text>
  <text x="{ext_x + ext_w/2}" y="{ext_v_y + 34}" class="txt-sans box-title" fill="#2E1045">hop Interactions</text>

  <line x1="{ext_x + ext_w}" y1="{v_y}" x2="{ext_x + ext_w + 22}" y2="{v_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="{ext_x + ext_w + 35}" y="{v_y + 4}" class="txt-serif math-lbl">S<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v</tspan></text>

  <!-- Branching Paths from S_u^t and S_v^t to Encoders -->
  <path d="M 235 {u_y} L 260 {u_y} L 260 {u_y} L {enc_x - 3} {u_y}" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <path d="M 235 {u_y} L 260 {u_y} L 260 162 L {enc_x - 3} 162" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <path d="M 235 {v_y} L 260 {v_y} L 260 198 L {enc_x - 3} 198" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <path d="M 235 {v_y} L 260 {v_y} L 260 {v_y} L {enc_x - 3} {v_y}" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- ==================== 3. ENCODING MODULES ==================== -->
  <!-- Top Green Box (Neighbors, Links & Time) -->
  <rect x="{enc_x}" y="{enc_top_y}" width="{enc_w}" height="{enc_h}" rx="8" fill="#D4EDDA" stroke="#5A9E66" stroke-width="1.2"/>
  <text x="{enc_x + enc_w/2}" y="{enc_top_y + 22}" class="txt-sans box-title" fill="#14421E">Encoding Neighbors,</text>
  <text x="{enc_x + enc_w/2}" y="{enc_top_y + 37}" class="txt-sans box-title" fill="#14421E">Links &amp; Time Intervals</text>

  <!-- Middle Yellow Box (Neighbor Co-occurrences) -->
  <rect x="{enc_x}" y="{enc_mid_y}" width="{enc_w}" height="{enc_h}" rx="8" fill="#FFF3CD" stroke="#C9A844" stroke-width="1.2"/>
  <text x="{enc_x + enc_w/2}" y="{enc_mid_y + 23}" class="txt-sans box-title" fill="#4B3B0A">Encoding Neighbor</text>
  <text x="{enc_x + enc_w/2}" y="{enc_mid_y + 38}" class="txt-sans box-title" fill="#4B3B0A">Co-occurrences</text>

  <!-- Bottom Green Box (Neighbors, Links & Time) -->
  <rect x="{enc_x}" y="{enc_bot_y}" width="{enc_w}" height="{enc_h}" rx="8" fill="#D4EDDA" stroke="#5A9E66" stroke-width="1.2"/>
  <text x="{enc_x + enc_w/2}" y="{enc_bot_y + 22}" class="txt-sans box-title" fill="#14421E">Encoding Neighbors,</text>
  <text x="{enc_x + enc_w/2}" y="{enc_bot_y + 37}" class="txt-sans box-title" fill="#14421E">Links &amp; Time Intervals</text>

  <!-- Tokens and Curly Braces for Top Module -->
  <!-- Left Brace from Green Box -->
  <path d="M {enc_x + enc_w + 4} {u_y} L {enc_x + enc_w + 10} {u_y} 
           M {enc_x + enc_w + 10} {u_y - 20} Q {enc_x + enc_w + 14} {u_y - 20} {enc_x + enc_w + 14} {u_y - 10} 
           L {enc_x + enc_w + 14} {u_y - 3} Q {enc_x + enc_w + 14} {u_y} {enc_x + enc_w + 18} {u_y}
           Q {enc_x + enc_w + 14} {u_y} {enc_x + enc_w + 14} {u_y + 3}
           L {enc_x + enc_w + 14} {u_y + 10} Q {enc_x + enc_w + 14} {u_y + 20} {enc_x + enc_w + 10} {u_y + 20}"
        fill="none" stroke="#1E293B" stroke-width="1.1"/>

  <text x="{tok_x}" y="{u_y - 18}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u,N</tspan></text>
  <text x="{tok_x}" y="{u_y + 4}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u,E</tspan></text>
  <text x="{tok_x}" y="{u_y + 26}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u,T</tspan></text>

  <!-- Right Brace to Top Coral Box -->
  <path d="M {tok_x + 18} {u_y - 20} Q {tok_x + 22} {u_y - 20} {tok_x + 22} {u_y - 10}
           L {tok_x + 22} {u_y - 3} Q {tok_x + 22} {u_y} {tok_x + 26} {u_y}
           Q {tok_x + 22} {u_y} {tok_x + 22} {u_y + 3}
           L {tok_x + 22} {u_y + 10} Q {tok_x + 22} {u_y + 20} {tok_x + 18} {u_y + 20}
           M {tok_x + 26} {u_y} L {pat_x - 3} {u_y}"
        fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Tokens and Curly Braces for Bottom Module -->
  <!-- Left Brace from Green Box -->
  <path d="M {enc_x + enc_w + 4} {v_y} L {enc_x + enc_w + 10} {v_y} 
           M {enc_x + enc_w + 10} {v_y - 20} Q {enc_x + enc_w + 14} {v_y - 20} {enc_x + enc_w + 14} {v_y - 10} 
           L {enc_x + enc_w + 14} {v_y - 3} Q {enc_x + enc_w + 14} {v_y} {enc_x + enc_w + 18} {v_y}
           Q {enc_x + enc_w + 14} {v_y} {enc_x + enc_w + 14} {v_y + 3}
           L {enc_x + enc_w + 14} {v_y + 10} Q {enc_x + enc_w + 14} {v_y + 20} {enc_x + enc_w + 10} {v_y + 20}"
        fill="none" stroke="#1E293B" stroke-width="1.1"/>

  <text x="{tok_x}" y="{v_y - 18}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v,N</tspan></text>
  <text x="{tok_x}" y="{v_y + 4}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v,E</tspan></text>
  <text x="{tok_x}" y="{v_y + 26}" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v,T</tspan></text>

  <!-- Right Brace to Bottom Coral Box -->
  <path d="M {tok_x + 18} {v_y - 20} Q {tok_x + 22} {v_y - 20} {tok_x + 22} {v_y - 10}
           L {tok_x + 22} {v_y - 3} Q {tok_x + 22} {v_y} {tok_x + 26} {v_y}
           Q {tok_x + 22} {v_y} {tok_x + 22} {v_y + 3}
           L {tok_x + 22} {v_y + 10} Q {tok_x + 22} {v_y + 20} {tok_x + 18} {v_y + 20}
           M {tok_x + 26} {v_y} L {pat_x - 3} {v_y}"
        fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Tokens and Curly Braces for Middle Yellow Module -->
  <path d="M {enc_x + enc_w + 4} 180 L {enc_x + enc_w + 10} 180 
           M {enc_x + enc_w + 10} 165 Q {enc_x + enc_w + 14} 165 {enc_x + enc_w + 14} 172 
           L {enc_x + enc_w + 14} 177 Q {enc_x + enc_w + 14} 180 {enc_x + enc_w + 18} 180
           Q {enc_x + enc_w + 14} 180 {enc_x + enc_w + 14} 183
           L {enc_x + enc_w + 14} 188 Q {enc_x + enc_w + 14} 195 {enc_x + enc_w + 10} 195"
        fill="none" stroke="#1E293B" stroke-width="1.1"/>

  <text x="{tok_x}" y="172" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u,C</tspan></text>
  <text x="{tok_x}" y="196" class="txt-serif math-lbl">X<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v,C</tspan></text>

  <!-- Right Brace and Routing from Middle Tokens to Coral Boxes -->
  <path d="M {tok_x + 18} 165 Q {tok_x + 22} 165 {tok_x + 22} 170 
           L {tok_x + 22} 174 Q {tok_x + 22} 177 {tok_x + 26} 177
           Q {tok_x + 22} 177 {tok_x + 22} 180
           L {tok_x + 22} 184 Q {tok_x + 22} 189 {tok_x + 18} 189"
        fill="none" stroke="#1E293B" stroke-width="1.1"/>
  
  <path d="M {tok_x + 26} 177 L {tok_x + 38} 177 L {tok_x + 38} {u_y + 14} L {pat_x - 3} {u_y + 14}" fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>
  <path d="M {tok_x + 26} 177 L {tok_x + 38} 177 L {tok_x + 38} {v_y - 14} L {pat_x - 3} {v_y - 14}" fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- ==================== 4. PATCHING, ALIGNMENT & CONCATENATION ==================== -->
  <!-- Top Coral Box (u) -->
  <rect x="{pat_x}" y="{pat_top_y}" width="{pat_w}" height="{pat_h}" rx="8" fill="#F8D7DA" stroke="#BC707B" stroke-width="1.2"/>
  <text x="{pat_x + pat_w/2}" y="{pat_top_y + 18}" class="txt-sans box-title" fill="#4C1118">Patching &amp;</text>
  <text x="{pat_x + pat_w/2}" y="{pat_top_y + 32}" class="txt-sans box-title" fill="#4C1118">Alignment &amp;</text>
  <text x="{pat_x + pat_w/2}" y="{pat_top_y + 46}" class="txt-sans box-title" fill="#4C1118">Concatenation</text>

  <line x1="{pat_x + pat_w}" y1="{u_y}" x2="{pat_x + pat_w + 22}" y2="{u_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="{pat_x + pat_w + 35}" y="{u_y + 4}" class="txt-serif math-lbl">Z<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u</tspan></text>

  <!-- Bottom Coral Box (v) -->
  <rect x="{pat_x}" y="{pat_bot_y}" width="{pat_w}" height="{pat_h}" rx="8" fill="#F8D7DA" stroke="#BC707B" stroke-width="1.2"/>
  <text x="{pat_x + pat_w/2}" y="{pat_bot_y + 18}" class="txt-sans box-title" fill="#4C1118">Patching &amp;</text>
  <text x="{pat_x + pat_w/2}" y="{pat_bot_y + 32}" class="txt-sans box-title" fill="#4C1118">Alignment &amp;</text>
  <text x="{pat_x + pat_w/2}" y="{pat_bot_y + 46}" class="txt-sans box-title" fill="#4C1118">Concatenation</text>

  <line x1="{pat_x + pat_w}" y1="{v_y}" x2="{pat_x + pat_w + 22}" y2="{v_y}" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="{pat_x + pat_w + 35}" y="{v_y + 4}" class="txt-serif math-lbl">Z<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v</tspan></text>

  <!-- Joining Paths from Z_u^t and Z_v^t to Z^t -->
  <path d="M {pat_x + pat_w + 48} {u_y} L 696 {u_y} L 696 166 L 702 166" fill="none" stroke="#1E293B" stroke-width="1.2"/>
  <path d="M {pat_x + pat_w + 48} {v_y} L 696 {v_y} L 696 194 L 702 194" fill="none" stroke="#1E293B" stroke-width="1.2"/>

  <!-- Joint Label Z^t -->
  <text x="668" y="184" class="txt-serif math-lbl" font-size="13">Z<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="11.5" dy="5"> = [Z</tspan><tspan font-size="7.5" dy="-4">t</tspan><tspan font-size="7.5" dy="7">u</tspan><tspan font-size="11.5" dy="-3">; Z</tspan><tspan font-size="7.5" dy="-4">t</tspan><tspan font-size="7.5" dy="7">v</tspan><tspan font-size="11.5" dy="-3">]</tspan></text>
  <line x1="710" y1="180" x2="{tr_x - 3}" y2="180" stroke="#1E293B" stroke-width="1.2"/>

  <!-- ==================== 5. STACKED TRANSFORMER / GNN BLOCK (× L) ==================== -->
  <!-- Shadow Background Card 2 -->
  <rect x="{tr_x + 8}" y="{tr_y - 6}" width="{tr_w}" height="{tr_h}" rx="14" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1"/>
  <!-- Shadow Background Card 1 -->
  <rect x="{tr_x + 4}" y="{tr_y - 3}" width="{tr_w}" height="{tr_h}" rx="14" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/>
  <!-- Foreground Main Card -->
  <rect x="{tr_x}" y="{tr_y}" width="{tr_w}" height="{tr_h}" rx="14" fill="#EAECEF" stroke="#4B5563" stroke-width="1.3"/>

  <!-- \times L label -->
  <text x="{tr_x + tr_w - 12}" y="{tr_y + 22}" class="txt-serif" font-size="13" font-style="italic" font-weight="bold" fill="#374151" text-anchor="end">× L</text>

  <!-- Input path into bottom of block -->
  <path d="M {tr_x - 3} 180 L {tr_x + 12} 180 L {tr_x + 12} 302 L {tr_x + tr_w/2} 302 L {tr_x + tr_w/2} 286" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Layer Normalization 1 (Bottom, Yellow) -->
  <rect x="{tr_x + 16}" y="250" width="133" height="30" rx="6" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
  <text x="{tr_x + tr_w/2}" y="269" class="txt-sans box-title" fill="#92400E">Layer Normalization</text>

  <!-- Arrow from LN1 to Multi-Head Attention -->
  <line x1="{tr_x + tr_w/2}" y1="250" x2="{tr_x + tr_w/2}" y2="222" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Multi-head Self-Attention (Orange) -->
  <rect x="{tr_x + 16}" y="174" width="133" height="42" rx="6" fill="#FFE5D0" stroke="#EA580C" stroke-width="1.2"/>
  <text x="{tr_x + tr_w/2}" y="192" class="txt-sans box-title" fill="#9A3412">Multi-head</text>
  <text x="{tr_x + tr_w/2}" y="206" class="txt-sans box-title" fill="#9A3412">Self-Attention</text>

  <!-- Residual 1: Add Circle -->
  <circle cx="{tr_x + tr_w/2}" cy="146" r="7.5" fill="#FFFFFF" stroke="#1E293B" stroke-width="1.1"/>
  <line x1="{tr_x + tr_w/2 - 4.5}" y1="146" x2="{tr_x + tr_w/2 + 4.5}" y2="146" stroke="#1E293B" stroke-width="1.1"/>
  <line x1="{tr_x + tr_w/2}" y1="141.5" x2="{tr_x + tr_w/2}" y2="150.5" stroke="#1E293B" stroke-width="1.1"/>
  
  <line x1="{tr_x + tr_w/2}" y1="174" x2="{tr_x + tr_w/2}" y2="156" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <!-- Skip Connection 1 -->
  <path d="M {tr_x + tr_w/2} 294 L {tr_x + tr_w - 18} 294 L {tr_x + tr_w - 18} 146 L {tr_x + tr_w/2 + 10} 146" fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Layer Normalization 2 (Middle, Yellow) -->
  <rect x="{tr_x + 16}" y="98" width="133" height="30" rx="6" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
  <text x="{tr_x + tr_w/2}" y="117" class="txt-sans box-title" fill="#92400E">Layer Normalization</text>
  <line x1="{tr_x + tr_w/2}" y1="138" x2="{tr_x + tr_w/2}" y2="130" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Feed Forward Network (Blue) -->
  <rect x="{tr_x + 16}" y="42" width="133" height="38" rx="6" fill="#CCE5FF" stroke="#38BDF8" stroke-width="1.2"/>
  <text x="{tr_x + tr_w/2}" y="58" class="txt-sans box-title" fill="#0369A1">Feed Forward</text>
  <text x="{tr_x + tr_w/2}" y="72" class="txt-sans box-title" fill="#0369A1">Network</text>
  <line x1="{tr_x + tr_w/2}" y1="98" x2="{tr_x + tr_w/2}" y2="82" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Residual 2: Add Circle -->
  <circle cx="{tr_x + tr_w/2}" cy="18" r="7.5" fill="#FFFFFF" stroke="#1E293B" stroke-width="1.1"/>
  <line x1="{tr_x + tr_w/2 - 4.5}" y1="18" x2="{tr_x + tr_w/2 + 4.5}" y2="18" stroke="#1E293B" stroke-width="1.1"/>
  <line x1="{tr_x + tr_w/2}" y1="13.5" x2="{tr_x + tr_w/2}" y2="22.5" stroke="#1E293B" stroke-width="1.1"/>
  
  <line x1="{tr_x + tr_w/2}" y1="42" x2="{tr_x + tr_w/2}" y2="28" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <!-- Skip Connection 2 -->
  <path d="M {tr_x + tr_w/2} 90 L {tr_x + tr_w - 18} 90 L {tr_x + tr_w - 18} 18 L {tr_x + tr_w/2 + 10} 18" fill="none" stroke="#1E293B" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Exit from Transformer Top to Output Head -->
  <path d="M {tr_x + tr_w/2} 10 L {tr_x + tr_w/2} -6 L {head_x} -6 L {head_x} {pool_y - 4}" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  
  <!-- Label H^t above Average Pooling -->
  <text x="{head_x + 18}" y="32" class="txt-serif math-lbl">H<tspan font-size="8.5" dy="-5">t</tspan></text>

  <!-- ==================== 6. AVERAGE POOLING & DOWNSTREAM TASKS ==================== -->
  <!-- Average Pooling Box (Teal/Cyan) -->
  <rect x="{pool_x}" y="{pool_y}" width="{pool_w}" height="{pool_h}" rx="8" fill="#D1ECF1" stroke="#3FA7B3" stroke-width="1.2"/>
  <text x="{head_x}" y="{pool_y + 19}" class="txt-sans box-title" fill="#0C5460">Average</text>
  <text x="{head_x}" y="{pool_y + 33}" class="txt-sans box-title" fill="#0C5460">Pooling</text>

  <!-- Downward Arrows from Pooling to h_u^t and h_v^t -->
  <path d="M {head_x - 24} {pool_y + pool_h} L {head_x - 24} 150" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <path d="M {head_x + 24} {pool_y + pool_h} L {head_x + 24} 150" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <text x="{head_x - 24}" y="168" class="txt-serif math-lbl">h<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">u</tspan></text>
  <text x="{head_x + 24}" y="168" class="txt-serif math-lbl">h<tspan font-size="8.5" dy="-5">t</tspan><tspan font-size="8.5" dy="8">v</tspan></text>

  <!-- Arrows from h_u, h_v to Downstream Tasks -->
  <path d="M {head_x - 24} 178 L {head_x - 24} {down_y - 3}" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>
  <path d="M {head_x + 24} 178 L {head_x + 24} {down_y - 3}" fill="none" stroke="#1E293B" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Downstream Tasks Box (White with Crisp Border) -->
  <rect x="{down_x}" y="{down_y}" width="{down_w}" height="{down_h}" rx="8" fill="#FFFFFF" stroke="#374151" stroke-width="1.3"/>
  <text x="{head_x}" y="{down_y + 22}" class="txt-sans box-title" fill="#111827">Downstream</text>
  <text x="{head_x}" y="{down_y + 36}" class="txt-sans box-title" fill="#111827">Tasks</text>
</svg>"""

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)
    
    svg_path = os.path.join(out_dir, "fig1_system_architecture.svg")
    pdf_path = os.path.join(out_dir, "fig1_system_architecture.pdf")
    png_path = os.path.join(out_dir, "fig1_system_architecture.png")
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
        
    doc = fitz.open("svg", svg.encode("utf-8"))
    
    # Render PDF (pure vector)
    pdf_bytes = doc.convert_to_pdf()
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
        
    # Render PNG at 300 DPI
    page = doc[0]
    zoom = 300.0 / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(png_path)
    
    print(f"[+] Successfully generated Figure 1 conforming to standard scientific protocol:")
    print(f"    SVG: {svg_path}")
    print(f"    PDF: {pdf_path}")
    print(f"    PNG: {png_path} ({pix.width}x{pix.height}px, 300 DPI)")

if __name__ == "__main__":
    generate_standard_protocol_figure()
