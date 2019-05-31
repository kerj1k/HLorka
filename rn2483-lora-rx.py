import time
import serial
import datetime
import csv
import codecs

# your TTY
tty = 'COM5'
ttyb = 57600
# your devaddr here
#devaddr = "ABCDEF01"
#device = "nodes/" + devaddr



# config.append("mac reset 868")
# config.append("mac set pwridx 5")
# config.append("mac set dr 5")
# config.append("mac set adr off")
# config.append("mac set nwkskey 2B7E151628AED2A6ABF7158809CF4F3C")
# config.append("mac set appskey 2B7E151628AED2A6ABF7158809CF4F3C")
# config.append("mac set devaddr "+devaddr)
# config.append("mac save")
# config.append("mac join abp")


def command_with_answer(data, port):
    port.write(data.encode('ascii') + b"\x0d\x0a")
    # time.sleep(0.01)
    s = port.readline()
    if s == b'ok\r\n':
        command_with_answer.answer = port.readline()
        return command_with_answer.answer
    else:
        return s

# def send(data, port):
#     port.write(data.encode('ascii') + b"\x0d\x0a")
#     # print(data)
#     time.sleep(0.04)
#     # rx_data = port.readline()[:-2]
#     # print(rx_data)


def command(data, port):
    port.write(data.encode() + b"\x0d\x0a")
    # time.sleep(0.01)
    if port.readline() == b'ok\r\n':
        return 1


def hex_translate(s):
    res = ""
    if len(s) % 2 == 0 :
        for i in range(int(round(len(s) / 2))):
            realIdx = i * 2
            res = res + chr(int(s[realIdx:realIdx + 2], 16))
        return res
    else:
        return s


def reconfiguration(type):
    config = []
    # config.append("sys factoryRESET")
    config.append("sys reset")
    config.append("mac pause")
    config.append("radio set freq 869250000")
    config.append("radio set pwr 14")
    config.append("radio set afcbw 125")
    config.append("radio set rxbw 125")
    config.append("radio set fdev 5000")
    config.append("radio set prlen 8")
    config.append("radio set crc on")
    config.append("radio set cr 4/8")
    config.append("radio set wdt 5000")
    #config.append("radio set sync 12")
    config.append("radio set bw 250")
    if type == 1:
        reconfiguration.name = 'LoraSF12'
        config.append("radio set mod lora")
        config.append("radio set sf sf12")
    elif type == 2:  # Lora SF7
        reconfiguration.name = 'LoraSF7'
        config.append("radio set mod lora")
        config.append("radio set sf sf7")
    elif type == 3:  # FSK
        reconfiguration.name = 'fsk'
        config.append("radio set mod fsk")
        # config.append("radio set bitrate 40000")
    elif type == 4:
        reconfiguration.name = 'LoraSF9'
        config.append("radio set mod lora")
        config.append("radio set sf sf9")
    for c in config:
        command(c, port)


def get_packet(port):
    get_packet.circle = 0
    while get_packet.circle < 24:

        get_packet.configType = reconfiguration.name
        get_packet.datetime = datetime.datetime.now()

        s = command_with_answer("radio rx 1000", port)
        if s == b'busy\r\n':
            time.sleep(0.2)
            s = port.readline()
        get_packet.check = s[0:8]

        if get_packet.check == b'radio_err\r\n':
            get_packet.data = 'None'
            get_packet.dehex = 'None'
            get_packet.snr = 'None'

            if get_packet.circle >= 23:
                return 0
            else:
                continue

        elif get_packet.check == b'radio_rx':
            get_packet.data = s.decode('ascii').replace("radio_rx  ", "").replace("\r\n", "")
            #get_packet.dehex = hex_translate(get_packet.data)
            get_packet.snr = command_with_answer("radio get snr", port).decode('ascii').replace('\r\n', '')
            return 1
        get_packet.circle += 1



port = serial.Serial(tty, ttyb, timeout=1)
time.sleep(0.1)
print("READY FOR RX")

conf = 4
reconfiguration(conf)

#past = None
s = 1

while True:
    # while s < 10:
    if get_packet(port):
        Data = str(s) + ';' + str(get_packet.datetime) + ';' + str(get_packet.configType) + ';' + str(get_packet.data) +  ';' + str(get_packet.snr) + '\r'
#+ str(get_packet.dehex)+
    else:
        Data = str(s) + ';' + str(datetime.datetime.now()) + ';' + str(reconfiguration.name) + ';' + 'None'
    fd = open('data.csv', 'a')
    fd.write(Data)
    fd.close()
    s = s + 1
    print(Data)
