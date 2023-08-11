import time, math, machine
from pinces.configuration import config

# RP2040 lit sur 3.3 V et 2^16 bits
facteurCorrection = 3.3 / 65536

# On etteint les leds du XIAO RP2040
userLed = machine.Pin(16, machine.Pin.OUT)
userLed.value(1)
userLed = machine.Pin(17, machine.Pin.OUT)
userLed.value(1)
userLed = machine.Pin(25, machine.Pin.OUT)
userLed.value(1)

### PROGRAMME ###

def mesure(id, decalageV, decalageI, debug):
	if debug:
		print("----------------")
		print("--- pince ", config["pinces"][id], "---")
		print("--- transfo ", config["transfo"], "---")
	ret = []
	nb_lectures = 0

	lectureV = 0
	sommeVcarre = 0
	sommeIcarre = 0
	sommePinstantanee = 0
	sommeI = 0 
	sommeV = 0
	maxI = 0
	maxV = 0
	adcTransfo = machine.ADC(machine.Pin(config["transfo"]["pin"]))
	adcPince = machine.ADC(machine.Pin(config["pinces"][id]["pin"]))

	# Calibration pour la mesure de la tension
	tensionReseau = config["transfo"]["Ventree"]
	resistances = config["transfo"]["resistancePontDiviseur"]
	tensionSortieTransfo = config["transfo"]["Vsortie"]
	# Tension du réseau
	VCAL = (resistances[0] + resistances[1]) * tensionReseau / resistances[0] / tensionSortieTransfo

	# Calibration pour la mesure du courant
	nbToursPince = config["pinces"][id]["nbTours"]
	resistanceTirage = config["pinces"][id]["resistanceTirage"]
	ICAL = nbToursPince / resistanceTirage

	# On boucle pendant n ms
	end_time = time.ticks_add(time.ticks_ms(), 100)
	while time.ticks_diff(end_time, time.ticks_ms()) > 0:
		nb_lectures += 1	

		derniereLectureV = lectureV		

		# lecture ADC
		lectureVbrute = adcTransfo.read_u16()
		lectureIbrute = adcPince.read_u16()
#		print(lectureVbrute, lectureIbrute)
		lectureV = lectureVbrute - 32768
		lectureI = lectureIbrute - 32768
		if debug:
			if lectureV > maxV:
				maxV = lectureV
			if lectureI:
				maxI = lectureI
		lectureV -= decalageV
		lectureI -= decalageI
		sommeI += lectureI 
		sommeV += lectureV 

		# caclcul rms
		Vcarre = lectureV * lectureV
		sommeVcarre += Vcarre
		Icarre = lectureI * lectureI
		sommeIcarre += Icarre

		# calibration de la phase
		lectureVdecalee = derniereLectureV + config["PHASECAL"] * (lectureV - derniereLectureV)

		# puissance instantanée
		Pinstantanee = lectureVdecalee * lectureI
		sommePinstantanee += Pinstantanee

	# calculs post boucle
	Vrms = math.sqrt(sommeVcarre / nb_lectures) * facteurCorrection * VCAL
	Irms = math.sqrt(sommeIcarre / nb_lectures) * facteurCorrection * ICAL
	puissanceReelle = sommePinstantanee / nb_lectures * facteurCorrection * VCAL * facteurCorrection * ICAL
	puissanceApparente = Vrms * Irms
	facteurdePuissance = puissanceReelle / puissanceApparente
	moyenneV = sommeV/nb_lectures
	decalageV = int(decalageV + moyenneV / 64) # pour converger
	moyenneI = sommeI/nb_lectures
	decalageI = int(decalageI + moyenneI / 64) # pour converger
	ret.append(config["pinces"][id]["id"])
	ret.append(puissanceReelle)
	ret.append(facteurdePuissance)
	ret.append(Vrms)
	ret.append(Irms)
	if debug:
		print("nb lecture", nb_lectures)
		print(f'  | {"max (nb)":14} | {"moyenne (nb)":14} | {"delacage (nb)":14} | {"rms (V ou A)":14} |')
		print(f"V |{maxV:15} |{moyenneV:15.0f} |{decalageV:15} |{Vrms:15.2f} |")
		print(f"I |{maxI:15} |{moyenneI:15.0f} |{decalageI:15} |{Irms:15.2f} |")
		print(f"puisssance apparente : {puissanceApparente:.0f} W")
		print(ret)	
		print(f"[{int(ret[1])} W, {ret[2] * 100:.0f} %, {ret[3]:.0f} V, {ret[4]:.2f} A]")
	return ret, decalageV, decalageI

def main(decalageV, decalageI, debug = False):
	while True:
		idPince = 0
		if debug:
			print("---------------- Lecture des pinces -------------------------")
		for pinces in config["pinces"]:
			m, decalageV, decalageI = mesure(idPince, decalageV, decalageI, debug)
			print(f"[{int(m[1])}, {m[2] * 100:.0f}, {m[3]:.0f}, {m[4]:.2f}]")
			idPince += 1
		time.sleep(1)
		userLed.toggle()

# Pour facilement travailler avec VSCode :

decalageV = -1000
decalageI = -1000

main(decalageV, decalageI, True)		