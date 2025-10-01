def analyze_sequence(seq):
    seq = seq.upper()
    total_length = len(seq)
    alphabet = sorted(set(seq))

    counts = {}
    percentages = {}
    for letter in alphabet:
        count = seq.count(letter)
        counts[letter] = count
        percentages[letter] = (count / total_length) * 100

    return alphabet, counts, percentages

S = 'ACGGGCATATGCGC'
alphabet, counts, percentages = analyze_sequence(S)

print("Alphabet of the sequence:", alphabet)
print("Counts of each component:")
for letter, count in counts.items():
    print(f"{letter}: {count}")
print("Percentages of each component:")
for letter, percent in percentages.items():
    print(f"{letter}: {percent:.2f}%")