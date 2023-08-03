import machine
import time

# Configure la broche GPIO 26 comme entrée ADC
adc1 = machine.ADC(machine.Pin(26))
adc2 = machine.ADC(machine.Pin(27))

# # Boucle de lecture des valeurs analogiques
# while True:
#     adc_value = adc1.read_u16()  # Lit la valeur analogique (0-65535)
#     voltage = (adc_value / 65535) * 3.3  # Convertit la valeur en tension (3.3V est la tension de référence)
#     print("Valeur ADC:", adc_value)
#     print("Tension:", voltage, "V")
#     time.sleep(1)  # Attend 1 seconde avant la prochaine lecture

while True:
  nbLectures = 0
  start_time = time.time()  # Enregistre le temps de départ
  while time.time() - start_time < 1.0:
      lecture = adc1.read_u16()  # Lit la valeur analogique (0-65535)
      nbLectures += 1
      lecture = adc2.read_u16()  # Lit la valeur analogique (0-65535)
      nbLectures += 1

  print("Longueur du tableau:", nbLectures)

