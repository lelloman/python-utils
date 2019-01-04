from random import shuffle

sentences = [
    'sotto la panca la capra campa',
    'sopra la panca la capra crepa',
    'trentratre trentini entrarono a trento',
    'tutti e trentatre trotterellando'
]

hash_len_bytes = 3
hash_len_bits = hash_len_bytes * 8
byte_map = [index for index in range(256)]
shuffle(byte_map)


def compute_sim_hash(text):
    sim_hash = [0 for _ in range(hash_len_bits)]

    for i in range(0, len(text) - (hash_len_bytes - 1), hash_len_bytes):
        byte_list = [byte_map[ord(text[i + j])] for j in range(hash_len_bytes)]
        combined_bytes = sum([b << (j * 8) for j, b in enumerate(byte_list)])
        for j in range(hash_len_bits):
            sim_hash[j] += 1 if (combined_bytes & (1 << j)) else -1

    return sim_hash


for sentence in sentences:
    sim_hash = compute_sim_hash(sentence)
    print ''.join(['0' if x <= 0 else '1' for x in sim_hash]), sentence
