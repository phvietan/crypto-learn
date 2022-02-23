freq = [8.1, 1.5, 2.7, 4.2, 12, 2, 2, 6.1, 7, 0.15, 0.77, 4, 2.4, 6.7, 7.5, 1.9, 0.095, 6, 6.3, 9, 2.7, 0.98, 2.3, 0.15, 2, 0.074] # https://en.wikipedia.org/wiki/Letter_frequency
sum = 0.0
for i in range(len(freq)):
    sum += freq[i]
    freq[i] /= 100
others_freq = (100 - sum) / 100 # percentage of other chars

def score_frequency(length_s, num_space, cnt_others, cnt_chars):
    length_s = float(length_s)
    space_score = abs(length_s / 4.7 - num_space) # https://wolfgarbe.medium.com/the-average-word-length-in-english-language-is-4-7-35750344870f

    others_score = abs(length_s * others_freq - cnt_others)

    length_s = length_s - length_s*others_freq # now only count chars a-z
    chars_score = 0
    for i in range(26):
        chars_score += abs(length_s * freq[i] - cnt_chars[i])
    return -space_score -others_score -chars_score
