
def convert_input(contents):
    map = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    out = ''
    for c in contents:
        if c in map:
            out += map[c]
    return out

def read_num(data):
    bits = ""
    for i in range(0, len(data), 5):
        bits += data[i + 1: i + 5]
        if data[i] == '0':
            break
    return int(bits, base=2), len(bits), data[i+5:]

def read_packet(data):
    TOTAL = len(data)
    version, ptype, data = data[:3], data[3:6], data[6:]
    version = int(version, base=2)
    ptype = int(ptype, base=2)

    if ptype == 4:
            num, _, data = read_num(data)

            return num, data, TOTAL - len(data)

    else :# operator packet
        mode, data = data[0], data[1:]
        if mode == '1': # num of packets
            num, data = data[:11], data[11:]
            num = int(num, base=2)
            sub_packets = []
            while len(sub_packets) < num:
                pkt, data, _ = read_packet(data)
                sub_packets.append(pkt)

        else: # num of bits
            num, data = data[:15], data[15:]
            num = int(num, base=2)
            decoded = 0
            sub_packets = []
            while decoded < num:
                pkt, data, pkt_bits = read_packet(data)
                sub_packets.append(pkt)
                decoded += pkt_bits

        match ptype:
            case 0: # Sum
                res = sum(sub_packets)
            case 1: # product
                total = 1
                for n in sub_packets:
                    total *= n
                res = total
            case 2:
                res = min(sub_packets)
            case 3:
                res = max(sub_packets)
            case 5:
                res = 1 if sub_packets[0] > sub_packets[1] else 0
                assert len(sub_packets) == 2, 'Must have exactly 2 subpackets'
            case 6:
                res = 1 if sub_packets[0] < sub_packets[1] else 0
                assert len(sub_packets) == 2, 'Must have exactly 2 subpackets'
            case 7:
                res = 1 if sub_packets[0] == sub_packets[1] else 0
                assert len(sub_packets) == 2, 'Must have exactly 2 subpackets'
        return res, data, TOTAL - len(data)

def parse_message(data):
    total = 0
    while len(data) > 8 and int(data) != 0:
        version_sum, data, _ = read_packet(data)
        total += version_sum

    return total

if __name__ == "__main__":
    data = convert_input('9C0141080250320F1802104A08')
    print(parse_message(data))
    
    with open('day16/input.txt') as f:
        data = convert_input(f.read().strip())

    print(parse_message(data))
    