#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox

def read_fasta(file_path):
    sequences = []
    cur_header = None
    cur_seq = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if cur_header:
                        sequences.append((cur_header, "".join(cur_seq)))
                    cur_header = line[1:]
                    cur_seq = []
                else:
                    cur_seq.append(line)
            if cur_header:
                sequences.append((cur_header, "".join(cur_seq)))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read FASTA file:\n{e}")
    return sequences

def get_stats(seq):
    seq_upper = seq.upper()
    total = len(seq_upper)
    alphabet = sorted(set(seq_upper))
    percentages = {ch: (seq_upper.count(ch) / total) * 100 for ch in alphabet} if total else {}
    return total, alphabet, percentages

class FastaViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FASTA Viewer")
        self.geometry("900x600")
        self.records = []

        # Top bar
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(top_frame, text="Open FASTA", command=self.open_fasta).pack(side=tk.LEFT)
        self.path_var = tk.StringVar()
        tk.Label(top_frame, textvariable=self.path_var).pack(side=tk.LEFT, padx=10)

        # Main area
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left: sequence list
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Sequences").pack(anchor="w")
        self.seq_listbox = tk.Listbox(left_frame, width=40)
        self.seq_listbox.pack(fill=tk.Y, expand=True)
        self.seq_listbox.bind("<<ListboxSelect>>", self.show_sequence)

        # Right: stats and sequence
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))

        # Stats labels
        self.len_var = tk.StringVar()
        self.alph_var = tk.StringVar()
        tk.Label(right_frame, textvariable=self.len_var).pack(anchor="w")
        tk.Label(right_frame, textvariable=self.alph_var).pack(anchor="w", pady=(2,5))

        # Counts table
        self.tree = ttk.Treeview(right_frame, columns=("char","count","percent"), show="headings")
        self.tree.heading("char", text="Symbol")
        self.tree.heading("count", text="Count")
        self.tree.heading("percent", text="Percent")
        self.tree.column("char", width=80, anchor="center")
        self.tree.column("count", width=100, anchor="e")
        self.tree.column("percent", width=100, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=False, pady=(0,5))

        # Scrollable full sequence
        tk.Label(right_frame, text="Full Sequence:").pack(anchor="w")
        self.seq_text = scrolledtext.ScrolledText(right_frame, height=8, wrap=tk.WORD)
        self.seq_text.pack(fill=tk.BOTH, expand=True)

    def open_fasta(self):
        path = filedialog.askopenfilename(
            title="Select FASTA file",
            filetypes=[("FASTA files", "*.fa *.fasta *.fna *.faa *.fas"), ("All files", "*.*")]
        )
        if not path:
            return
        self.path_var.set(path)
        self.records = read_fasta(path)
        if not self.records:
            messagebox.showinfo("Empty", "No sequences found in the file.")
            return
        self.seq_listbox.delete(0, tk.END)
        for i, (header, _) in enumerate(self.records, start=1):
            self.seq_listbox.insert(tk.END, f"{i}. {header}")
        self.seq_listbox.selection_set(0)
        self.show_sequence()

    def show_sequence(self, _event=None):
        if not self.records:
            return
        sel = self.seq_listbox.curselection()
        idx = sel[0] if sel else 0
        header, seq = self.records[idx]
        length, alphabet, percentages = get_stats(seq)
        self.len_var.set(f"{header} — Length: {length}")
        self.alph_var.set(f"Alphabet: {', '.join(alphabet)}")

        # Update table
        self.tree.delete(*self.tree.get_children())
        for ch in alphabet:
            self.tree.insert("", tk.END, values=(ch, seq.upper().count(ch), f"{percentages[ch]:.2f}%"))

        # Update full sequence
        self.seq_text.delete("1.0", tk.END)
        self.seq_text.insert(tk.END, seq)

if __name__ == "__main__":
    app = FastaViewer()
    app.mainloop()