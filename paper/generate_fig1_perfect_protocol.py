import os
import fitz

def generate_perfect_protocol_figure():
    width = 1380
    height = 400
    
    # Mathematical SVG curly brace generator
    def curly_brace(x, y1, y2, orientation='right', w=10, r=4):
        ym = (y1 + y2) / 2.0
        if orientation == 'right': # points to right: }
            d = (f"M {x} {y1} "
                 f"Q {x+w/2} {y1} {x+w/2} {y1+r} "
                 f"L {x+w/2} {ym-r} "
                 f"Q {x+w/2} {ym} {x+w} {ym} "
                 f"Q {x+w/2} {ym} {x+w/2} {ym+r} "
                 f"L {x+w/2} {y2-r} "
                 f"Q {x+w/2} {y2} {x} {y2}")
        else: # points to left: {
            d = (f"M {x} {y1} "
                 f"Q {x-w/2} {y1} {x-w/2} {y1+r} "
                 f"L {x-w/2} {ym-r} "
                 f"Q {x-w/2} {ym} {x-w} {ym} "
                 f"Q {x-w/2} {ym} {x-w/2} {ym+r} "
                 f"L {x-w/2} {y2-r} "
                 f"Q {x-w/2} {y2} {x} {y2}")
        return d

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M 0 0 L 6 3 L 0 6 z" fill="#1E1E1E"/>
    </marker>
    <style>
      .txt-serif {{ font-family: 'Times New Roman', Times, serif; }}
      .txt-sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .box-title {{ font-size: 11px; font-weight: 500; text-anchor: middle; fill: #111111; }}
      .math-lbl {{ font-size: 13.5px; font-weight: bold; font-style: italic; fill: #000000; text-anchor: middle; }}
    </style>
  </defs>

  <!-- Clean Canvas -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>

  <!-- ==================== 1. LEFT: QUERY NODES & DYNAMIC GRAPH ==================== -->
  <!-- Node u -->
  <circle cx="65" cy="80" r="13" fill="#FFFFFF" stroke="#1F77B4" stroke-width="1.6"/>
  <text x="65" y="85" class="txt-serif" font-size="15" font-style="italic" font-weight="bold" fill="#111111" text-anchor="middle">u</text>

  <!-- Node v -->
  <circle cx="65" cy="310" r="13" fill="#FFFFFF" stroke="#1F77B4" stroke-width="1.6"/>
  <text x="65" y="315" class="txt-serif" font-size="15" font-style="italic" font-weight="bold" fill="#111111" text-anchor="middle">v</text>

  <!-- Dashed Link u-v with t? -->
  <line x1="65" y1="96" x2="65" y2="180" stroke="#1F77B4" stroke-width="1.2" stroke-dasharray="3,3"/>
  <line x1="65" y1="210" x2="65" y2="294" stroke="#1F77B4" stroke-width="1.2" stroke-dasharray="3,3"/>
  <text x="65" y="198" class="txt-serif" font-size="13.5" font-style="italic" font-weight="bold" fill="#D9383A" text-anchor="middle">t?</text>

  <!-- Extract First-hop Interactions Boxes (Lavender) -->
  <rect x="115" y="54" width="145" height="52" rx="8" fill="#DECCD8" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="187.5" y="75" class="txt-sans box-title">Extract First-</text>
  <text x="187.5" y="91" class="txt-sans box-title">hop Interactions</text>

  <rect x="115" y="284" width="145" height="52" rx="8" fill="#DECCD8" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="187.5" y="305" class="txt-sans box-title">Extract First-</text>
  <text x="187.5" y="321" class="txt-sans box-title">hop Interactions</text>

  <!-- Arrows from u, v to Extract boxes -->
  <line x1="80" y1="80" x2="112" y2="80" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="80" y1="310" x2="112" y2="310" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Dynamic Graph Icon & Organic Edges -->
  <g transform="translate(130, 135)">
    <!-- Nodes -->
    <circle cx="15" cy="40" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="45" cy="18" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="82" cy="12" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="38" cy="52" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="70" cy="42" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="102" cy="30" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="118" cy="55" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="25" cy="85" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="62" cy="88" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="88" cy="68" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    <circle cx="108" cy="88" r="4.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.2"/>
    
    <!-- Edges -->
    <line x1="18" y1="37" x2="42" y2="21" stroke="#444444" stroke-width="1.1"/>
    <line x1="18" y1="43" x2="35" y2="50" stroke="#444444" stroke-width="1.1"/>
    <line x1="16" y1="44" x2="24" y2="81" stroke="#444444" stroke-width="1.1"/>
    <line x1="48" y1="17" x2="78" y2="13" stroke="#444444" stroke-width="1.1"/>
    <line x1="47" y1="21" x2="67" y2="39" stroke="#444444" stroke-width="1.1"/>
    <line x1="41" y1="54" x2="67" y2="44" stroke="#444444" stroke-width="1.1"/>
    <line x1="39" y1="56" x2="60" y2="84" stroke="#444444" stroke-width="1.1"/>
    <line x1="28" y1="85" x2="58" y2="88" stroke="#444444" stroke-width="1.1"/>
    <line x1="74" y1="41" x2="98" y2="32" stroke="#444444" stroke-width="1.1"/>
    <line x1="72" y1="45" x2="86" y2="65" stroke="#444444" stroke-width="1.1"/>
    <line x1="64" y1="86" x2="85" y2="70" stroke="#444444" stroke-width="1.1"/>
    <line x1="91" y1="71" x2="105" y2="85" stroke="#444444" stroke-width="1.1"/>
    <line x1="90" y1="66" x2="115" y2="57" stroke="#444444" stroke-width="1.1"/>
    <line x1="84" y1="15" x2="100" y2="27" stroke="#444444" stroke-width="1.1"/>
    
    <text x="58" y="112" class="txt-serif" font-size="12" font-weight="bold" fill="#222222" text-anchor="middle">Dynamic Graph</text>
  </g>

  <!-- Arrows from Dynamic Graph to Extract Boxes -->
  <line x1="188" y1="130" x2="188" y2="110" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="188" y1="258" x2="188" y2="280" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- ==================== 2. BRANCHING S_u^t and S_v^t ==================== -->
  <!-- Out of top Extract Box -->
  <line x1="260" y1="80" x2="282" y2="80" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="296" y="85" class="txt-serif math-lbl">S<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u</tspan></text>

  <!-- Out of bottom Extract Box -->
  <line x1="260" y1="310" x2="282" y2="310" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="296" y="315" class="txt-serif math-lbl">S<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v</tspan></text>

  <!-- Arrows branching from S_u^t and S_v^t -->
  <line x1="310" y1="80" x2="346" y2="80" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="305" y1="92" x2="346" y2="180" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <line x1="305" y1="298" x2="346" y2="210" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="310" y1="310" x2="346" y2="310" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- ==================== 3. THREE ENCODING MODULES ==================== -->
  <!-- Top Green Box -->
  <rect x="350" y="46" width="165" height="68" rx="8" fill="#D5E8C8" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="432.5" y="66" class="txt-sans box-title">Encoding Neighbors,</text>
  <text x="432.5" y="82" class="txt-sans box-title">Links &amp; Time</text>
  <text x="432.5" y="98" class="txt-sans box-title">Intervals</text>

  <!-- Middle Yellow Box -->
  <rect x="350" y="165" width="165" height="60" rx="8" fill="#F1DC6C" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="432.5" y="193" class="txt-sans box-title">Encoding Neighbor</text>
  <text x="432.5" y="210" class="txt-sans box-title">Co-occurrences</text>

  <!-- Bottom Green Box -->
  <rect x="350" y="276" width="165" height="68" rx="8" fill="#D5E8C8" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="432.5" y="296" class="txt-sans box-title">Encoding Neighbors,</text>
  <text x="432.5" y="312" class="txt-sans box-title">Links &amp; Time</text>
  <text x="432.5" y="328" class="txt-sans box-title">Intervals</text>

  <!-- ==================== 4. CURLY BRACES & TOKENS ==================== -->
  <!-- Top Right Brace  -->
  <path d="{curly_brace(520, 48, 112, 'right', w=12, r=5)}" fill="none" stroke="#1E1E1E" stroke-width="1.2"/>
  <text x="555" y="62" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u,N</tspan></text>
  <text x="555" y="84" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u,E</tspan></text>
  <text x="555" y="106" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u,T</tspan></text>

  <!-- Middle Right Brace  -->
  <path d="{curly_brace(520, 170, 220, 'right', w=12, r=5)}" fill="none" stroke="#1E1E1E" stroke-width="1.2"/>
  <text x="555" y="184" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u,C</tspan></text>
  <text x="555" y="212" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v,C</tspan></text>

  <!-- Bottom Right Brace  -->
  <path d="{curly_brace(520, 278, 342, 'right', w=12, r=5)}" fill="none" stroke="#1E1E1E" stroke-width="1.2"/>
  <text x="555" y="292" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v,N</tspan></text>
  <text x="555" y="314" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v,E</tspan></text>
  <text x="555" y="336" class="txt-serif math-lbl">X<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v,T</tspan></text>

  <!-- Left Brace  grouping 4 tokens into Top Patching Box -->
  <path d="{curly_brace(582, 50, 192, 'left', w=14, r=6)}" fill="none" stroke="#1E1E1E" stroke-width="1.2"/>
  <line x1="568" y1="121" x2="606" y2="121" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Left Brace  grouping 4 tokens into Bottom Patching Box -->
  <path d="{curly_brace(582, 204, 346, 'left', w=14, r=6)}" fill="none" stroke="#1E1E1E" stroke-width="1.2"/>
  <line x1="568" y1="275" x2="606" y2="275" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- ==================== 5. PATCHING & ALIGNMENT BOXES ==================== -->
  <!-- Top Pink Box -->
  <rect x="610" y="60" width="145" height="74" rx="8" fill="#FBDBD0" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="682.5" y="83" class="txt-sans box-title">Patching &amp;</text>
  <text x="682.5" y="99" class="txt-sans box-title">Alignment &amp;</text>
  <text x="682.5" y="115" class="txt-sans box-title">Concatenation</text>

  <!-- Bottom Pink Box -->
  <rect x="610" y="254" width="145" height="74" rx="8" fill="#FBDBD0" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="682.5" y="277" class="txt-sans box-title">Patching &amp;</text>
  <text x="682.5" y="293" class="txt-sans box-title">Alignment &amp;</text>
  <text x="682.5" y="309" class="txt-sans box-title">Concatenation</text>

  <!-- Arrows to Z_u^t and Z_v^t -->
  <line x1="755" y1="97" x2="780" y2="97" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="794" y="102" class="txt-serif math-lbl">Z<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u</tspan></text>

  <line x1="755" y1="291" x2="780" y2="291" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <text x="794" y="296" class="txt-serif math-lbl">Z<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v</tspan></text>

  <!-- Arrows from Z_u^t and Z_v^t towards Joint Z^t -->
  <line x1="794" y1="112" x2="794" y2="175" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="794" y1="278" x2="794" y2="215" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Joint Z^t Label -->
  <text x="794" y="198" class="txt-serif math-lbl">Z<tspan font-size="9" dy="-5">t</tspan><tspan font-size="12" dy="5"> = [Z</tspan><tspan font-size="8" dy="-4">t</tspan><tspan font-size="8" dy="7">u</tspan><tspan font-size="12" dy="-3">; Z</tspan><tspan font-size="8" dy="-4">t</tspan><tspan font-size="8" dy="7">v</tspan><tspan font-size="12" dy="-3">]</tspan></text>

  <!-- Routing Bracket into Transformer Block -->
  <path d="M 838 190 L 850 190 L 850 380 L 965 380 L 965 362" fill="none" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- ==================== 6. STACKED TRANSFORMER / TGAT BLOCK (× L) ==================== -->
  <!-- Stack Card 2 (Back) -->
  <rect x="897" y="18" width="160" height="332" rx="12" fill="#EDEDED" stroke="#555555" stroke-width="1.0"/>
  <!-- Stack Card 1 (Middle) -->
  <rect x="891" y="24" width="160" height="332" rx="12" fill="#E3E3E3" stroke="#444444" stroke-width="1.0"/>
  <!-- Stack Card 0 (Front) -->
  <rect x="885" y="30" width="160" height="332" rx="12" fill="#DADADA" stroke="#2B2B2B" stroke-width="1.2"/>

  <!-- × L text -->
  <text x="1042" y="24" class="txt-serif" font-size="14" font-style="italic" font-weight="bold" fill="#222222">× L</text>

  <!-- Inside Front Card -->
  <!-- Layer Normalization 1 (Bottom, Cream) -->
  <rect x="902" y="265" width="126" height="34" rx="6" fill="#FFF2CC" stroke="#2B2B2B" stroke-width="1.1"/>
  <text x="965" y="286" class="txt-sans box-title">Layer Normalization</text>

  <!-- Triple Arrows (Q, K, V) from LN1 to Multi-Head Attention -->
  <line x1="935" y1="265" x2="935" y2="242" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>
  <line x1="965" y1="265" x2="965" y2="242" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>
  <line x1="995" y1="265" x2="995" y2="242" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Multi-head Self-Attention (Terracotta/Orange) -->
  <rect x="902" y="196" width="126" height="44" rx="6" fill="#EBB788" stroke="#2B2B2B" stroke-width="1.1"/>
  <text x="965" y="214" class="txt-sans box-title">Multi-head</text>
  <text x="965" y="229" class="txt-sans box-title">Self-Attention</text>

  <!-- Residual 1: Circle + -->
  <circle cx="965" cy="173" r="6.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.1"/>
  <line x1="961" y1="173" x2="969" y2="173" stroke="#2B2B2B" stroke-width="1.1"/>
  <line x1="965" y1="169" x2="965" y2="177" stroke="#2B2B2B" stroke-width="1.1"/>

  <line x1="965" y1="196" x2="965" y2="182" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Skip Connection 1 (around MHA) -->
  <path d="M 965 315 L 1034 315 L 1034 173 L 974 173" fill="none" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Arrow from Residual 1 to LN2 -->
  <line x1="965" y1="166" x2="965" y2="152" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Layer Normalization 2 (Middle, Cream) -->
  <rect x="902" y="116" width="126" height="34" rx="6" fill="#FFF2CC" stroke="#2B2B2B" stroke-width="1.1"/>
  <text x="965" y="137" class="txt-sans box-title">Layer Normalization</text>

  <!-- Arrow from LN2 to FFN -->
  <line x1="965" y1="116" x2="965" y2="99" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Feed Forward Network (Soft Blue) -->
  <rect x="902" y="53" width="126" height="44" rx="6" fill="#B2D2EC" stroke="#2B2B2B" stroke-width="1.1"/>
  <text x="965" y="71" class="txt-sans box-title">Feed Forward</text>
  <text x="965" y="86" class="txt-sans box-title">Network</text>

  <!-- Residual 2: Circle + -->
  <circle cx="965" cy="40" r="6.5" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.1"/>
  <line x1="961" y1="40" x2="969" y2="40" stroke="#2B2B2B" stroke-width="1.1"/>
  <line x1="965" y1="36" x2="965" y2="44" stroke="#2B2B2B" stroke-width="1.1"/>

  <line x1="965" y1="53" x2="965" y2="48.5" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- Skip Connection 2 (around FFN) -->
  <path d="M 965 160 L 1034 160 L 1034 40 L 974 40" fill="none" stroke="#1E1E1E" stroke-width="1.1" marker-end="url(#arr)"/>

  <!-- ==================== 7. OUTPUT HEAD: POOLING & DOWNSTREAM ==================== -->
  <!-- Exit arrow straight up out of card -->
  <line x1="965" y1="33.5" x2="965" y2="18" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- Orthogonal path from Card Top to Average Pooling -->
  <path d="M 965 10 L 1170 10 L 1170 70" fill="none" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- H^t Label -->
  <text x="1170" y="52" class="txt-serif math-lbl">H<tspan font-size="9" dy="-5">t</tspan></text>

  <!-- Average Pooling Box (Pastel Mint/Teal) -->
  <rect x="1110" y="74" width="120" height="46" rx="8" fill="#C4EEEA" stroke="#2B2B2B" stroke-width="1.2"/>
  <text x="1170" y="94" class="txt-sans box-title">Average</text>
  <text x="1170" y="109" class="txt-sans box-title">Pooling</text>

  <!-- Downward Arrows from Pooling to Downstream Tasks -->
  <line x1="1140" y1="120" x2="1140" y2="248" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="1200" y1="120" x2="1200" y2="248" stroke="#1E1E1E" stroke-width="1.2" marker-end="url(#arr)"/>

  <!-- h_u^t and h_v^t Labels beside arrows -->
  <text x="1126" y="184" class="txt-serif math-lbl">h<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">u</tspan></text>
  <text x="1214" y="184" class="txt-serif math-lbl">h<tspan font-size="9" dy="-5">t</tspan><tspan font-size="9" dy="8">v</tspan></text>

  <!-- Downstream Tasks Box (Clean White) -->
  <rect x="1110" y="252" width="120" height="54" rx="8" fill="#FFFFFF" stroke="#2B2B2B" stroke-width="1.3"/>
  <text x="1170" y="275" class="txt-sans box-title">Downstream</text>
  <text x="1170" y="292" class="txt-sans box-title">Tasks</text>

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
    generate_perfect_protocol_figure()
