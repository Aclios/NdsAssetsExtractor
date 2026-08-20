"""
MIT License

Copyright (c) 2025 PhoenixBound

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Original code: https://github.com/PhoenixBound/999-tools/tree/main
"""


def _at6p_decompress(data: bytes):
    assert data[0:4] == b"AT6P"
    unk = data[4]
    compressed_size = int.from_bytes(data[5:7], "little") | (data[19] << 16)
    assert compressed_size == len(data)
    # assert int.from_bytes(data[7:16], 'little') == 0
    decompressed_size = int.from_bytes(data[16:19], "little")

    previous = data[20]
    current = previous

    output = bytearray()
    output.append(current)

    # assert data[21] == 0

    i_byte = 0x16
    i_bit = 0

    while len(output) < decompressed_size:
        bit_count = 0
        while (data[i_byte] >> i_bit) & 1 == 0:
            bit_count += 1
            i_bit += 1
            if i_bit == 8:
                i_bit = 0
                i_byte += 1

            if bit_count > 8:
                raise RuntimeError("Exponential-Golomb decoding failure")

        # Advance past the 1 bit
        i_bit += 1
        if i_bit == 8:
            i_bit = 0
            i_byte += 1
        # Read the actual data
        d = 0
        for j in range(bit_count):
            bit = (data[i_byte] >> i_bit) & 1
            i_bit += 1
            if i_bit == 8:
                i_bit = 0
                i_byte += 1
            d |= bit << j
        # Add bias to complete exponential-golomb decoding
        d += (1 << bit_count) - 1

        # Chunsoft loves encoding sign-magnitude values as variable-width positive integers
        # IMPORTANT: `previous` is not updated when repeating the current byte (sign == 1 and magnitude == 0)
        sign = (d & 1) * -2 + 1
        magnitude = d >> 1
        if sign == -1 and magnitude == 0:
            # -0 means "output the previous byte"
            previous, current = current, previous
        elif magnitude != 0:
            previous = current
            current += magnitude * sign
            current &= 0xFF
        output.append(current)

    return output


def at6p_compress(data: bytes):
    output = bytearray()
    output.extend(b"AT6P")
    # I dunno how to calculate this. I originally put an F (for "frustrating" of course...)
    # but I want to see if it's maybe a checksum or what
    output.extend(b"\x00")
    # Placeholder: compressed size
    output.extend(b"\x00\x00")
    output.extend(b"\x00" * 9)
    output.extend(len(data).to_bytes(3, "little"))
    output.append(0)
    output.append(data[0])
    output.append(0)

    compressed_byte = 0
    compressed_bit_pos = 0

    previous = data[0]

    for i, b in zip(range(1, len(data)), data[1:]):
        delta = b - data[i - 1]
        # Make signed
        delta = ((delta + 0x80) & 0xFF) - 0x80
        sign_bit = int(delta < 0)
        magnitude = abs(delta)

        word = None
        if magnitude == 0:
            word = 0
        elif b == previous:
            word = 1
            previous = data[i - 1]
        else:
            word = magnitude * 2 + sign_bit
            previous = data[i - 1]

        # Encode the word as bits, using the method mentioned on the "exponential-golomb"
        # Wikipedia page
        word += 1

        # Add initial 0 bits
        for j in range(word.bit_length() - 1):
            # compressed_byte |= 0
            compressed_bit_pos += 1
            if compressed_bit_pos == 8:
                compressed_bit_pos = 0
                output.append(compressed_byte)
                compressed_byte = 0
        # Then add data bits
        # Starting with the initial 1
        compressed_byte |= 1 << compressed_bit_pos
        compressed_bit_pos += 1
        if compressed_bit_pos == 8:
            compressed_bit_pos = 0
            output.append(compressed_byte)
            compressed_byte = 0
        # Then proceeding through the number with all the least significant bits
        for j in range(word.bit_length() - 1):
            compressed_byte |= ((word >> j) & 1) << compressed_bit_pos
            compressed_bit_pos += 1
            if compressed_bit_pos == 8:
                compressed_bit_pos = 0
                output.append(compressed_byte)
                compressed_byte = 0

    if compressed_bit_pos != 0:
        output.append(compressed_byte)

    # Fill in the compressed size, now that we know it
    sz = len(output).to_bytes(3, "little")
    output[5:7] = sz[0:2]
    output[19] = sz[2]

    # return bytes(output)
    return output


def atxp_decompress(data: bytes):
    if data[0:4] == b"AT6P":
        return _at6p_decompress(data)

    if data[0:4] == b"AT5P":
        compressed_size = data[5] | (data[6] << 8) | (data[0x13] << 16)
        decompressed_size = int.from_bytes(data[0x10:0x13], "little")
        i = 0x14
    elif data[0:4] == b"AT4P":
        compressed_size = int.from_bytes(data[5:7], "little")
        decompressed_size = int.from_bytes(data[0x10:0x12], "little")
        i = 0x12
    elif data[0:4] == b"AT3P":
        compressed_size = int.from_bytes(data[5:7], "little")
        decompressed_size = 0x7FFFFFFF
        i = 7

    if data[4] == ord("N"):
        return data[7 : 7 + compressed_size]

    nybble_list = data[7:16]
    assert compressed_size == len(data)
    flags = data[i]
    i += 1
    flags_read = 0
    dest = bytearray()
    while i < compressed_size:
        if flags_read == 8:
            flags = data[i]
            i += 1
            flags_read = 0

        if (flags & 0x80) != 0:
            # Literal byte
            dest.append(data[i])
            i += 1
        else:
            length = data[i] >> 4
            cmd = nybble_list.find(length.to_bytes(1, "little"))
            if cmd == -1:
                # LZ pointer reference
                length += 3
                offset = ((data[i] & 0xF) << 8) | data[i + 1]
                for _ in range(length):
                    dest.append(dest[len(dest) - 4096 + offset])
                i += 2
            else:
                n = data[i] & 0xF
                h = (n + 1) & 0xF
                l = (n - 1) & 0xF
                if cmd == 0:
                    dest.append(n * 0x11)
                    dest.append(n * 0x11)
                elif cmd == 1:
                    dest.append((n << 4) | h)
                    dest.append(h * 0x11)
                elif cmd == 2:
                    dest.append((n << 4) | l)
                    dest.append(n * 0x11)
                elif cmd == 3:
                    dest.append(n * 0x11)
                    dest.append((l << 4) | n)
                elif cmd == 4:
                    dest.append(n * 0x11)
                    dest.append((n << 4) | l)
                elif cmd == 5:
                    dest.append((n << 4) | l)
                    dest.append(l * 0x11)
                elif cmd == 6:
                    dest.append((n << 4) | h)
                    dest.append(n * 0x11)
                elif cmd == 7:
                    dest.append(n * 0x11)
                    dest.append((h << 4) | n)
                else:
                    dest.append(n * 0x11)
                    dest.append((n << 4) | h)
                i += 1
        flags_read += 1
        flags <<= 1
    assert decompressed_size == len(dest)
    return dest
