import os
import machine
import sdcard           

corrente = 10;
tensao  = 8;
print(os.listdir('/'))

os.umount('/')
spi = machine.SPI(2,baudrate=100000,sck=machine.Pin(18),mosi=machine.Pin(23),
       miso=machine.Pin(19),polarity=0,phase=0)
sd = sdcard.SDCard(spi, machine.Pin(5))
os.mount(sd, '/sd')
# Exclua o arquivo
try:
    arquivo_remover = "/sd/dados.txt"  # Substitua pelo caminho do seu arquivo
    os.remove(arquivo_remover)
    print("Arquivo ", arquivo_remover, "removido!!")
    # Desmonte o cartão SD
    uos.umount("/sd")
except OSError as erro:
    print("Arquivo não localizado")
    print(erro)