import os
import struct


def load(path):
    SHORT_INT_SIZE = 2
    MAX_LINK_LENGTH = int(os.environ["MAX_LABEL_LENGTH"])
    MAX_SEQ_LENGTH = int(os.environ["MAX_SEQ_LENGTH"])

    def first(short_tuple):
        return short_tuple[0]

    def join(char_tuple):
        out = ""
        for l in char_tuple:
            if l == b"\x00":
                break
            else:
                out += l.decode("utf-8", "replace")
        return out

    def group(char_tuple, size):
        out = []
        pointer = 0
        while len(char_tuple[pointer:]):
            seq = join(char_tuple[pointer - size : pointer])
            out.append(seq) if len(seq) else None
            pointer += size
        return out

    with open(path, "rb") as file:
        binary_data = file.read()
        payload = dict(
            ranges=[],
            labels=[],
            seqs=[],
        )
        seek_pointer = 0
        while seek_pointer < os.stat(path).st_size:
            seqs_len = first(struct.unpack_from("h", binary_data, seek_pointer))
            link = join(
                struct.unpack_from(
                    f"{MAX_LINK_LENGTH}c", binary_data, seek_pointer + SHORT_INT_SIZE
                )
            )
            seqs = group(
                struct.unpack_from(
                    f"{seqs_len*MAX_SEQ_LENGTH}c",
                    binary_data,
                    seek_pointer + MAX_LINK_LENGTH + SHORT_INT_SIZE,
                ),
                MAX_SEQ_LENGTH,
            )
            payload["labels"].append(link)
            payload["ranges"].append(len(seqs))
            payload["seqs"].extend(seqs)
            seek_pointer = (
                seek_pointer
                + seqs_len * MAX_SEQ_LENGTH
                + MAX_LINK_LENGTH
                + SHORT_INT_SIZE
            )
        return payload


def dump(path, data):
    ...
