import time, math, machine

### CONFIG ###
adcPinces = []

# Configure des broches GPIO comme entrées ADC des pinces
adcPinces.append(machine.ADC(machine.Pin(26)))
adcPinces.append(machine.ADC(machine.Pin(27)))

# Configure de la broche GPIO comme entrée ADC transformateur
# adcTransfo = machine.ADC(machine.Pin(999))

### PROGRAMME ###

def mesure(id, adc):
  ret = []
  VSmax = 0
  nb_lectures = 0
  end_time = time.ticks_add(time.ticks_ms(), 20)
  while time.ticks_diff(end_time, time.ticks_ms()) > 0:
    voltage = adc.read_u16() # TODO prendre le milieu et ramener à 3,3 V / 2
    nb_lectures +=1
    if voltage > VSmax:
      VSmax = voltage
  # Les mesures
  puissanceReelle = VSmax # TODO  
  ISmax = VSmax / 150 # TODO Paramétrer Ohm de la résistance de charge
  IEmax = ISmax * 2000 # TODO Paramétrer le nb tours dans la pince
  Irms = IEmax / math.sqrt(2) # TODO à recalculer
  Vrms = 230 # TODO à recalculer
  puissanceApparente = Vrms * IEmax # TODO à recalculer
  facteurdePuissance = 0 # TODO à recalculer
  ret.append(id)
  ret.append(puissanceReelle)
  ret.append(facteurdePuissance)
  ret.append(Vrms)
  ret.append(Irms)
  return ret

while True:
  idPince = 0
  for adcPince in adcPinces:
    idPince += 1
    print(mesure(idPince, adcPince))
  time.sleep(1)