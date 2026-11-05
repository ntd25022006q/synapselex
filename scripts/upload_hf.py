import os
import sys
from pathlib import Path
from huggingface_hub import HfApi

REPO_ID = "datbazuka2502/synapse-civil-bench"
REPO_TYPE = "dataset"

api = HfApi()
ROOT_DIR = Path(__file__).resolve().parent.parent

files_to_upload = [
    ("dataset_card/README.md", "README.md"),
    ("data/benchmarks/synapse_civil_bench_train.json", "benchmarks/synapse_civil_bench_train.json"),
    ("data/benchmarks/synapse_civil_bench_val.json", "benchmarks/synapse_civil_bench_val.json"),
    ("data/benchmarks/synapse_civil_bench_test.json", "benchmarks/synapse_civil_bench_test.json"),
    ("data/benchmarks/synapse_civil_bench_quarantine.jsonl", "benchmarks/synapse_civil_bench_quarantine.jsonl"),
    ("data/benchmarks/synapse_civil_bench_counterfactual_320.json", "benchmarks/synapse_civil_bench_counterfactual_320.json"),
    ("data/benchmarks/synapse_civil_bench_full.jsonl", "benchmarks/synapse_civil_bench_full.jsonl"),
    ("ontology/vclo_core.owl", "ontology/vclo_core.owl"),
    ("ontology/vclo_core.ttl", "ontology/vclo_core.ttl"),
]

print(f"Uploading artifacts to Hugging Face Hub: {REPO_ID} ...")

for rel_path, path_in_repo in files_to_upload:
    local_path = ROOT_DIR / rel_path
    if local_path.exists():
        size = local_path.stat().st_size
        print(f"  -> Uploading {local_path} ({size:,} bytes) as {path_in_repo}...")
        api.upload_file(
            path_or_fileobj=str(local_path),
            path_in_repo=path_in_repo,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"Upload {path_in_repo} for SynapseCivil-Bench release"
        )
        print(f"     [OK] Uploaded {path_in_repo}")
    else:
        print(f"  [!] Missing file: {local_path}")

print("All Hugging Face Hub uploads complete!")
