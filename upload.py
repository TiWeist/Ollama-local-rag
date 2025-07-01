import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import json
import sys
import time

def print_progress_bar(iteration, total, prefix='', suffix='', length=40, fill='█'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()  # New line on complete

# Function to convert multiple PDFs to text and append to vault.txt
def convert_pdf_to_text():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    total_pdfs = len(file_paths)
    if total_pdfs:
        for idx, file_path in enumerate(file_paths, start=1):
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                text = ''

                print(f"Processing PDF {idx}/{total_pdfs}: '{os.path.basename(file_path)}' with {num_pages} pages:")

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    if page.extract_text():
                        text += page.extract_text() + " "
                    # Update progress bar for pages
                    print_progress_bar(page_num + 1, num_pages, prefix='Pages', suffix='Complete')

                # Normalize whitespace and clean up text
                text = re.sub(r'\s+', ' ', text).strip()

                # Split text into chunks by sentences, respecting a maximum chunk size
                sentences = re.split(r'(?<=[.!?]) +', text)
                chunks = []
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 < 1000:
                        current_chunk += (sentence + " ").strip()
                    else:
                        chunks.append(current_chunk)
                        current_chunk = sentence + " "
                if current_chunk:
                    chunks.append(current_chunk)

                with open("vault.txt", "a", encoding="utf-8") as vault_file:
                    for chunk in chunks:
                        vault_file.write(chunk.strip() + "\n")

            print(f"PDF {idx}/{total_pdfs} '{os.path.basename(file_path)}' content appended to vault.txt.\n")

def upload_txtfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()
            text = re.sub(r'\s+', ' ', text).strip()
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            print(f"Text file content appended to vault.txt.")

def upload_jsonfile():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            text = json.dumps(data, ensure_ascii=False)
            text = re.sub(r'\s+', ' ', text).strip()
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 1000:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            print(f"JSON file content appended to vault.txt.")

root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

pdf_button = tk.Button(root, text="Upload PDF(s)", command=convert_pdf_to_text)
pdf_button.pack(pady=10)

txt_button = tk.Button(root, text="Upload Text File", command=upload_txtfile)
txt_button.pack(pady=10)

json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

root.mainloop()
