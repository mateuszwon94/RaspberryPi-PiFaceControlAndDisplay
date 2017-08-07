#/usr/bin/env python3

import sys
import subprocess
from time import *
import pifacecad

UPDATE_INTERVAL = 60 #s
GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"

IS_ON = True

temperature_symbol = pifacecad.LCDBitmap(
    [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
memory_symbol = pifacecad.LCDBitmap(
    [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
temp_symbol_index, memory_symbol_index = 0, 1

def runCmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8'
)

def getIP():
    return run_cmd(GET_IP_CMD)[:-1]

def getProcTemp():
    return run_cmd(GET_TEMP_CMD)[5:9]

def getFreeMem():
    total_mem = float(run_cmd(TOTAL_MEM_CMD))
    used_mem = float(run_cmd(USED_MEM_CMD))
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)

def waitForIP():
    ip = ""
    while len(ip) <= 0:
        sleep(1)
        ip = get_my_ip()

def show_sysinfo():
    cad.lcd.clear()
    cad.lcd.write("IP:{}\n".format(get_my_ip()))

    cad.lcd.write_custom_bitmap(temp_symbol_index)
    cad.lcd.write(":{}C ".format(get_my_temp()))

    cad.lcd.write_custom_bitmap(memory_symbol_index)
    cad.lcd.write(":{}".format(get_my_free_mem()))
    sleep(UPDATE_INTERVAL)

def display():
    if IS_ON:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.clear()
        cad.lcd.display_on()
        cad.lcd.backlight_on()

if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()

    if "clear" in sys.argv:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.store_custom_bitmap(temp_symbol_index, temperature
_symbol)
        cad.lcd.store_custom_bitmap(memory_symbol_index, memory_sy
mbol)
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for IP..")
        wait_for_ip()
        show_sysinfo()
