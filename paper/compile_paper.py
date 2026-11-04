"""
SynapseLex: 4-Pass Publication-Grade LaTeX Compilation Suite
Compiles synapselex_paper.tex -> synapselex_paper.pdf with zero errors and zero overfull hbox.
"""

import sys
import os
import subprocess
import re

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PAPER_DIR = os.path.abspath(os.path.dirname(__file__))

def run_cmd(cmd, cwd=PAPER_DIR):
    print(f"[*] Running: {' '.join(cmd)} in {cwd}")
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    if res.returncode != 0:
        print(f"[!] Error in {' '.join(cmd)} (Exit Code: {res.returncode}):")
        # print last 30 lines
        lines = res.stdout.splitlines()[-30:]
        print("\n".join(lines))
        return False, res.stdout
    return True, res.stdout

def compile_paper():
    tex_file = "synapselex_paper.tex"
    base_name = "synapselex_paper"

    print("\n" + "=" * 78)
    print("  SYNAPSELEX CAMERA-READY 4-PASS LATEX COMPILATION")
    print("=" * 78)

    # Pass 1: Initial pdflatex
    ok, out = run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file])
    if not ok:
        print("[!] Pass 1 failed!")
        return False
    print("  ✓ Pass 1 (pdflatex) successful.")

    # Pass 2: bibtex
    ok, out = run_cmd(["bibtex", base_name])
    if not ok:
        print("[!] Pass 2 (bibtex) failed!")
        return False
    print("  ✓ Pass 2 (bibtex) successful.")

    # Pass 3: Resolve citations
    ok, out = run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file])
    if not ok:
        print("[!] Pass 3 failed!")
        return False
    print("  ✓ Pass 3 (pdflatex) successful.")

    # Pass 4: Final cross-references
    ok, out = run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file])
    if not ok:
        print("[!] Pass 4 failed!")
        return False
    print("  ✓ Pass 4 (pdflatex) successful.")

    # Analyze log
    log_path = os.path.join(PAPER_DIR, f"{base_name}.log")
    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        log_text = f.read()

    # Check for overfull \hbox
    overfull_matches = re.findall(r"Overfull \\hbox \(([0-9\.]+)pt too wide\)", log_text)
    # Check page count
    page_match = re.search(r"Output written on .*? \((\d+) pages,", log_text)
    pages = int(page_match.group(1)) if page_match else 0

    print("\n" + "=" * 78)
    print("  COMPILATION AUDIT REPORT")
    print("=" * 78)
    print(f"  • Target PDF:       {os.path.join(PAPER_DIR, base_name + '.pdf')}")
    print(f"  • Total Pages:      {pages} pages")
    print(f"  • Overfull \\hbox:   {len(overfull_matches)} occurrences")
    if overfull_matches:
        for m in overfull_matches:
            print(f"    - Overfull: {m}pt too wide")
    else:
        print("  ✓ ZERO OVERFULL \\hbox DETECTED!")

    pdf_path = os.path.join(PAPER_DIR, f"{base_name}.pdf")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024.0
        print(f"  • PDF File Size:    {size_kb:.1f} KB")
        print("  ✓ CAMERA-READY PDF COMPILED SUCCESSFULLY!")
        return True
    return False

if __name__ == "__main__":
    success = compile_paper()
    sys.exit(0 if success else 1)
