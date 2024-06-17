import codecs
import pyvisa
import time

class FunctionGenerator:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.rm = pyvisa.ResourceManager()
        self.func_gen = self.rm.open_resource(f'TCPIP0::{self.ip_address}::inst0::INSTR')
        self.func_gen.timeout = 5000
        self.time_unit = 1e-3
        self.dt = 1
        self.sample_rate = 1 / (self.dt * self.time_unit)
        
    def dec_code(self, x):
        return "abcdef"[x-10] if x >= 10 else str(x)
    
    def dec_to_hex(self, x):
        hex_value = ""
        for i in range(4):
            hex_value = self.dec_code(x % 16) + hex_value
            x //= 16
        return hex_value

    def gen_bit_string(self, dec_list):
        bit_string = ""
        for num in dec_list:
            dec_dat = self.dec_to_hex(num)
            bit_string += f'\\x{dec_dat[:2]}\\x{dec_dat[2:]}'
        return bit_string

    def gen_xhex_text(self, text):
        return ''.join(f'\\x{self.dec_to_hex(ord(char))[2:]}' for char in text)

    def generate_command_string(self, pulse_data):
        num_list = self.process_pulse_data(pulse_data)
        bit_string = '\\x22' + '\\x' + self.dec_to_hex(16383)[2:4]
        bit_length = str(len(num_list) * 2)
        bit_start = str(len(bit_length))

        command_str = ('\\x3A\\x53\\x4F\\x55\\x52\\x31\\x3A\\x54\\x52\\x41\\x43\\x65'
                       '\\x3A\\x44\\x41\\x54\\x41\\x3A\\x44\\x41\\x43\\x31\\x36\\x20'
                       '\\x56\\x4F\\x4C\\x41\\x54\\x49\\x4C\\x45\\x2C\\x45\\x4E\\x44\\x2C\\x23' 
                       + self.gen_xhex_text(bit_start) + self.gen_xhex_text(bit_length) 
                       + self.gen_bit_string(num_list))
        
        return codecs.escape_decode(command_str)[0]

    def process_pulse_data(self, pulse_data):
        num_list = []
        for amplitude, duration in pulse_data:
            rep = int(duration / self.dt)
            for _ in range(rep):
                if amplitude < 0:
                    num_list.append(int(((amplitude + 0.5) / 0.5) * 128) + 128)
                else:
                    num_list.append(int((amplitude / 0.5) * 127))
        return num_list

    def setup_function_generator(self, command_str):
        print(self.func_gen.query("*IDN?"))

        # Turn off the output before configuring
        self.func_gen.write(':OUTP1 OFF')
        time.sleep(1)

        # Configure the function generator
        self.func_gen.write(":SOURCE1:APPL:SEQ")
        self.func_gen.write(":SOURCE1:FUNC:SEQ:FILT INSERT")
        print(self.func_gen.query(":SOURCE1:FUNCTION?"))

        # Insert the ASCII sequence into the command
        self.func_gen.write_raw(command_str)
        self.func_gen.write(f"SOURCE1:VOLTAGE 1.000000VPP")
        self.func_gen.write(f"SOURCE1:FUNC:SEQ:SRAT {self.sample_rate:.6f}")

        # Switch CH1 on
        self.func_gen.write_raw(b'\x3a\x4F\x55\x54\x50\x31\x20\x4f\x4e')
        print(self.func_gen.query("OUTP1?"))

if __name__ == "__main__":
    ip_address = '192.168.68.32'
    pulse_data = [(0,100),(0.5,10),(0.3,80),(0,100),(-0.4,30),(0.5,10),(0,100)]

    func_gen = FunctionGenerator(ip_address)
    command_str = func_gen.generate_command_string(pulse_data)
    func_gen.setup_function_generator(command_str)
