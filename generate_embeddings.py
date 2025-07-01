import torch
import ollama
import os
from tqdm import tqdm

print("Loading vault content...")
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

print("Generating embeddings for the vault content...")
vault_embeddings = []
for content in tqdm(vault_content, desc="Embedding lines", unit="line"):
    response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
    vault_embeddings.append(response["embedding"])

print("Converting embeddings to tensor...")
vault_embeddings_tensor = torch.tensor(vault_embeddings) 

print("Saving embeddings to vault_embeddings.pt...")
torch.save(vault_embeddings_tensor, "vault_embeddings.pt")

print("Done! Embeddings saved.")
