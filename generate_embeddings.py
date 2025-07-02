import torch
import ollama
import os
from tqdm import tqdm

EMBEDDINGS_FILE = "vault_embeddings.pt"
INDEX_FILE = "vault_index.txt"
VAULT_FILE = "vault.txt"
MODEL = "mxbai-embed-large"

# Load vault content
print("Loading vault content...")
vault_content = []
if os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        vault_content = f.readlines()

# Determine where to resume
start_index = 0
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "r") as f:
        index = f.read().strip()
        if index.isdigit():
            start_index = int(index)
            print(f"Resuming from line {start_index}...")

# Load existing embeddings if any
if os.path.exists(EMBEDDINGS_FILE) and start_index > 0:
    existing_tensor = torch.load(EMBEDDINGS_FILE)
    vault_embeddings = existing_tensor.tolist()
else:
    vault_embeddings = []

# Start embedding remaining lines
print("Generating embeddings (with resume support)...")
for i in tqdm(range(start_index, len(vault_content)), desc="Embedding lines", unit="line"):
    line = vault_content[i].strip()
    if not line:
        continue
    try:
        response = ollama.embeddings(model=MODEL, prompt=line)
        embedding = response["embedding"]
        vault_embeddings.append(embedding)

        # Save every 100 lines or on the last line
        if (i + 1) % 100 == 0 or (i + 1) == len(vault_content):
            torch.save(torch.tensor(vault_embeddings), EMBEDDINGS_FILE)
            with open(INDEX_FILE, "w") as f:
                f.write(str(i + 1))  # Next line to process
    except Exception as e:
        print(f"\n⚠️ Error embedding line {i}: {e}")
        break

print("\n✅ Done! Embeddings saved to", EMBEDDINGS_FILE)
