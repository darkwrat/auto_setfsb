import os
import binascii
import subprocess

# http://stackoverflow.com/a/7397689
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def get_freq_for_bit(bit=None):
    if bit == None:
        return 100 # fixme: specify default FSB frequency

    return 120 if bit == "0" else 130 # fixme: specify frequencies for 0 and 1 bits


def set_freq(freq, clock_gen=None):
    proc = subprocess.Popen([os.path.abspath("setfsb.exe"),
                                 "-w0",
                                 "-q",
                                 "-s{}".format(freq),
                                 "-cg{}".format(clock_gen) if clock_gen != None else ""
                             ], shell=True)
    print("set_freq() : pid: {}, freq: {}".format(proc.pid, freq))
    proc.wait()


def reset_freq(clock_gen=None):
    return set_freq(get_freq_for_bit(None), clock_gen)


def main():
    clock_gen = None # fixme: specify clock generator

    print("clock gen: {}".format(clock_gen))
    reset_freq(clock_gen)

    while True:
        with open("in_file.txt") as file:
            for line in file:
                for char in text_to_bits(line + '\n'):
                    set_freq(get_freq_for_bit(char), clock_gen)
                    reset_freq(clock_gen)
        reset_freq(clock_gen)
        print("--> wrap")
        
                    
if __name__ == "__main__":
    main()
