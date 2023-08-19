import machine
import time

# Configuração dos pinos dos botões
BUTTON_PIN_1 = 14  # Pino do botão 1
BUTTON_PIN_2 = 27  # Pino do botão 2
BUTTON_PIN_3 = 33  # Pino do botão 3

# Configuração do pino de saída PWM
PWM_PIN = 26      # Pino de saída PWM

# Configuração dos valores de duty cycle para cada botão
DUTY_LOW = 10     # Valor de duty cycle baixo (10%)
DUTY_MEDIUM = 50  # Valor de duty cycle médio (50%)
DUTY_HIGH = 90    # Valor de duty cycle alto (90%)

# Inicialização dos pinos
button1 = machine.Pin(BUTTON_PIN_1, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BUTTON_PIN_2, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(BUTTON_PIN_3, machine.Pin.IN, machine.Pin.PULL_UP)

pwm = machine.PWM(machine.Pin(PWM_PIN))
pwm.freq(1000)  # Frequência do PWM

# Estado anterior dos botões e valor do último botão pressionado
prev_button1_state = 1
prev_button2_state = 1
prev_button3_state = 1

last_pressed_button = None

# Loop principal
while True:
    button1_state = button1.value()
    button2_state = button2.value()
    button3_state = button3.value()
    
    if button1_state != prev_button1_state:
        if button1_state == 0:
            pwm.duty(DUTY_LOW)
            last_pressed_button = "button1"
        prev_button1_state = button1_state
    
    if button2_state != prev_button2_state:
        if button2_state == 0:
            pwm.duty(DUTY_MEDIUM)
            last_pressed_button = "button2"
        prev_button2_state = button2_state
    
    if button3_state != prev_button3_state:
        if button3_state == 0:
            pwm.duty(DUTY_HIGH)
            last_pressed_button = "button3"
        prev_button3_state = button3_state
    
    # Verificar se nenhum botão está pressionado e manter o último valor
    if button1_state == 1 and button2_state == 1 and button3_state == 1:
        if last_pressed_button == "button1":
            pwm.duty(DUTY_LOW)
        elif last_pressed_button == "button2":
            pwm.duty(DUTY_MEDIUM)
        elif last_pressed_button == "button3":
            pwm.duty(DUTY_HIGH)
    
    time.sleep(0.1)  # Pequeno delay para evitar detecção falsa de múltiplos cliques
