from machine import Pin, ADC
from time import sleep, ticks_ms
import time
import os
import machine
import sdcard

t0 = ticks_ms()
#Corrente
SENSOR_PIN = 32
media = 0
# Inicialização do pino ADC
adc = ADC(Pin(SENSOR_PIN))
adc.atten(ADC.ATTN_11DB) 
i = 0
media = 0


#Velocidade
pin_hall = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
pulsos = 0
rpm = 0
tempo_ant = time.ticks_ms()
tempo_inicio = time.time()
circunferencia_roda = 2 * 3.14 * 0.256 # Circunferência da roda em metros (ajuste de acordo com a roda do seu projeto)
distancia = 0  # Distância percorrida em km
velocidade = 0  # Velocidade em km/h
velocidade_ant = 0
tempo_decorrido = 0

def correnteDC(sensor):
              #  sensor_valor = sensor.read()
              #  volts = (sensor_valor * 3.3) / 4095
                
                media = 0
                for i in range (100):
                        sensor_valor = sensor.read()
                        media = media + sensor_valor
                        i = i +1
                media = media/100
                corrente = -(((media-2993)/4095)*3.3)/0.066
                corrente = corrente - 5
                # Converte o valor analógico em corrente (em A)
               # volts = (corrente * 3.3) / 4095
              
                #corrente = ((volts - 2.5) / 0.066)
                #corrente = corrente + 1.1
                
                return corrente

def tratador_interrupcao(p):
    # Ações a serem executadas quando o sinal do sensor Hall detectar uma borda de subida
                global pulsos, pulsos_ant, rpm, tempo_ant, tempo_inicio, tempo_decorrido, circunferencia_roda, distancia, velocidade, velocidade_ant, parametro, tempo_diferenca
                
                tempo_atual = time.ticks_ms()
                tempo_diferenca = time.ticks_diff(tempo_atual, tempo_ant)/1000  # Diferença de tempo em segundos
                tempo_ant = tempo_atual
                pulsos = pulsos + 1
                distancia += circunferencia_roda / 1000  # Distância percorrida em km
                tempo_decorrido = (time.time() - tempo_inicio)  # Tempo decorrido durante o percurso em minutos
                
                velocidade = (circunferencia_roda / tempo_diferenca) * 3.6
                
                
                return velocidade

# Cartão SD
print(os.listdir('/'))

os.umount('/')
spi = machine.SPI(2,baudrate=100000,sck=machine.Pin(18),mosi=machine.Pin(23),
       miso=machine.Pin(19),polarity=0,phase=0)
sd = sdcard.SDCard(spi, machine.Pin(5))
os.mount(sd, '/sd')
arquivo = open("/sd/dados.txt", "a")
arquivo.write("Corrente;Velocidade;Distância Percorrida;Tempo""\n")
arquivo.close()

while True:
    
                pin_hall.irq(trigger=Pin.IRQ_RISING, handler=tratador_interrupcao)
                corrente = correnteDC(adc)
                if corrente < 0.35:
                    corrente = 0
                print("Corrente", (round(corrente,2))," Velocidade: ", round(velocidade,2),"Distância Percorrida", round(distancia,3),"Tempo: ", round(tempo_decorrido,2))
                print("Gravando dados: ")
                
                arquivo = open("/sd/dados.txt", "a")
                arquivo.write(str(round(corrente,2)))
                arquivo.write(";")
                arquivo.write(str(round(velocidade,2)))
                arquivo.write(";")
                arquivo.write(str(round(distancia,2)))
                arquivo.write(";")
                arquivo.write(";")
                arquivo.write(str(round(tempo_decorrido,2)))
                arquivo.write("\n")
                arquivo.close()
                
                
                time.sleep_ms(10)

