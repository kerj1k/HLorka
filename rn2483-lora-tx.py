import time
import serial
import codecs
import datetime

# your TTY
tty= 'COM9'
ttyb=57600
# your devaddr here
#devaddr="ABCDEF01"
#device="nodes/"+devaddr

#инициализация и конфигурация
def configuration(type):
    config = []
    # config.append("sys factoryRESET")
    config.append('sys reset')
    config.append('mac pause')
    config.append('radio set freq 868250000')
    config.append('radio set pwr 14')
    config.append('radio set afcbw 125')
    config.append('radio set rxbw 125')
    config.append('radio set fdev 5000')
    config.append('radio set prlen 8')
    config.append('radio set crc on')
    config.append('radio set cr 4/8')
    config.append('radio set wdt 0')
    config.append('radio set sync 12')
    config.append('radio set bw 125')
    if type == 1:
        configuration.name = 'LoraSF12'
        config.append('radio set mod lora')
        config.append('radio set sf sf12')
    elif type == 2:  # Lora SF7
        configuration.name = 'LoraSF7'
        config.append('radio set mod lora')
        config.append('radio set sf sf7')
    elif type == 3:  # FSK
        configuration.name = 'FSK'
        config.append('radio set mod fsk')
        # config.append('radio set bitrate 40000')
    for c in config:
        send(c, p)

# изменение настроек в процессе отправки пакетов
def reconfig(type):
    config = []
    if type == 1:
        configuration.name = 'LoraSF12'
        config.append('radio set mod lora')
        config.append('radio set sf sf12')
    elif type == 2:  # Lora SF7
        configuration.name = 'LoraSF7'
        config.append('radio set mod lora')
        config.append('radio set sf sf7')
    elif type == 3:  # FSK
        configuration.name = 'fsk'
        config.append('radio set mod fsk')
        # config.append('radio set bitrate 5000')
    for c in config:
        send(c, p)


#config.append('mac reset 868')
#config.append('mac set pwridx 5')
#config.append('mac set dr 5')
#config.append('mac set adr off')
#config.append('mac set nwkskey 2B7E151628AED2A6ABF7158809CF4F3C')
#config.append('mac set appskey 2B7E151628AED2A6ABF7158809CF4F3C')
#config.append('mac set devaddr '+devaddr)
#config.append('mac save')
#config.append('mac join abp')

# тупая отправка команд на модуль
def send(data, p):
    data_bytes = data.encode('ascii')
    p.write(data_bytes + b'\x0d\x0a')
    # print(data)
    time.sleep(0.05)
    rdata = p.readline()
    rdata = rdata[:-2]
    # print(rdata)
    return 1

# отправка команд на модуль чтобы сразу передавать в эфир 
def sendtx(data, p):
    data_bytes = data.encode('ascii')
    p.write(data_bytes + b'\x0d\x0a')
    time.sleep(0.05)
    rdata = p.readline()
    if rdata == b'ok\r\n':
        rdata = p.readline()
    if rdata == b'radio_tx_ok\r\n':
        return 1
    else:
        return 0
# инициализация серийника
p = serial.Serial(tty , ttyb)

# процесс отправки пакетов с иницализацией и настройкой сначала
time.sleep(1)
i = 3
configuration(i)
j = 1
while True:
    msg = configuration.name+' BobrovLoh #' + str(j)
    print(msg)
    #send('mac tx uncnf 1 '+msg, p)
    if sendtx('radio tx ' + msg.encode('utf-8').hex(), p):
        time.sleep(2.5)
        reconfig(j % 3 + 1)
    j = j + 1
