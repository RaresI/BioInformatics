import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def read_fasta(file_path):
    sequence = ""
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(">"):  # Ignore FASTA headers
                sequence += line
    return sequence.upper()

def analyze_sequence(seq):
    total_length = len(seq)
    alphabet = sorted(set(seq))
    percentages = {}
    for letter in alphabet:
        count = seq.count(letter)
        percentages[letter] = (count / total_length) * 100
    return alphabet, percentages

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Select FASTA file",
        filetypes=[("FASTA files", "*.fasta *.fa"), ("All files", "*.*")]
    )
    if file_path:
        try:
            seq = read_fasta(file_path)
            alphabet, percentages = analyze_sequence(seq)
            display_result(seq, alphabet, percentages)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")

def display_result(seq, alphabet, percentages):
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Sequence length: {len(seq)}\n")
    result_text.insert(tk.END, f"Alphabet: {alphabet}\n")
    result_text.insert(tk.END, "Percentages:\n")
    for letter, percent in percentages.items():
        result_text.insert(tk.END, f"{letter}: {percent:.2f}%\n")

# --- GUI setup ---
root = tk.Tk()
root.title("FASTA Analyzer")
root.geometry("500x400")

button = tk.Button(root, text="Select FASTA File", command=choose_file)
button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()