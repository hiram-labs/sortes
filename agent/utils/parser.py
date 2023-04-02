def undo_stride(payload, step, stride):
    data = ""
    pointer = 0
    while pointer < len(payload):
        data += payload[pointer : pointer + stride]
        pointer = pointer + stride + int(step - stride)
    return data


def context_split(payload, num_words_per_split):
    words = payload.split()
    parts = []
    for i in range(0, len(words), num_words_per_split):
        part = " ".join(words[i : i + num_words_per_split])
        parts.append(part)
    return parts


def context_split_with_overlap(payload, num_words_per_split, window_size):
    words = payload.split()
    parts = []
    for i in range(0, len(words), window_size):
        part = " ".join(words[i : i + num_words_per_split])
        parts.append(part)
    return parts
