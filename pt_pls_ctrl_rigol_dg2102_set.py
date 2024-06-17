import pyvisa
import time
import numpy as np
rm = pyvisa.ResourceManager()
#rm.list_resources()
func_gen = rm.open_resource('TCPIP0::192.168.68.32::inst0::INSTR')
print(func_gen.query("*IDN?"))
func_gen.write(':OUTP1 OFF')
time.sleep(1)
#N = 16384
#volt = ""
#for i in range(N):
#    if i < int(N//2):
#        volt = volt+"0000" 
#    else:
#        volt = volt+"3FFF" 
#print(len(volt))
#func_gen.write(":SOUR1:APPL:SEQ 320000,1,0,0")
#func_gen.write("SOUR1:APPL:USER")
#func_gen.write(":SOUR1:FUNC:SEQ:FILT INSE")
#func_gen.write(":SOUR1:FUNC:SEQ:USER")
#func_gen.write("SOUR1:FUNC:SHAPE USER")
#data_str = f"#{N}{len(str(N))}"
#command = f"DATA VOLATILE,-1,0,-1,0,1"




func_gen.write(":SOURCE1:APPL:SEQ")
func_gen.write(":SOURCE1:FUNC:SEQ:FILT INSERT")
print(func_gen.query(":SOURCE1:FUNCTION?"))
func_gen.write(":SOUR1:TRACe:DATA:DAC16 VOLATILE,END,#216000102030405060708090a0b0c0d0f0g")
#func_gen.write(":SOUR1:TRACe:DATA:DAC16 VOLATILE,END,#3100")
#func_gen.write(":SOURCE1:FUNCTION:ARB:SAMPLE 10000") 
func_gen.write("SOURCE1:VOLTAGE 1.000000VPP")
func_gen.write("SOURCE1:FUNC:SEQ:SRAT 100.000000")

#func_gen.write(":SOUR1:VOLT:UNIT VPP")
#func_gen.write(":SOUR1:VOLT 1")
#func_gen.write(":SOUR1:FUNC:SEQ:SRAT 100000")
func_gen.write(':OUTP1 ON')  # Switch CH1 off
#func_gen.write()
