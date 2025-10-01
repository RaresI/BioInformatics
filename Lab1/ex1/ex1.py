def find_alphabet(seq):
    seq = seq.upper()
    unique_chars = set(seq)
    alphabet = sorted(unique_chars)
    return alphabet

#Examples
dna_seq = "ATCGATCGAATCG"
rna_seq = "AUCGGAUCAU"
protein_seq = "MKTIIALSYIFCLVFADYKDDDDK"

print("ARN:", find_alphabet(rna_seq))
print("ADN:", find_alphabet(dna_seq))
print("Protein:", find_alphabet(protein_seq))