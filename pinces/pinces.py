import time, math, machine
from pinces.configuration import config

# RP2040 lit sur 3.3 V et 2^16 bits
facteurCorrection = 3.3 / 65536

### PROGRAMME ###

def mesure(id, decalageV, decalageI, debug):
	if debug:
		print("***********************")
		print("--- pince ", config["pinces"][id]["id"], "---")
		print("***********************")
	ret = []
	nb_lectures = 0

	lectureV = 0
	sommeVcarre = 0
	sommeIcarre = 0
	sommePinstantanee = 0
	sommeI = 0 
	sommeV = 0
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
		lectureV = lectureVbrute - 32768 - decalageV
		lectureI = lectureIbrute - 32768 - decalageI
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
	puissanceReelle = max(0, sommePinstantanee / nb_lectures * facteurCorrection * VCAL * facteurCorrection * ICAL)
	puissanceApparente = Vrms * Irms
	facteurdePuissance = puissanceReelle / puissanceApparente
	moyenneV = sommeV/nb_lectures
	decalageV = decalageV + moyenneV / 64 # pour converger
	moyenneI = sommeI/nb_lectures
	decalageI = decalageI + moyenneI / 64 # pour converger
	ret.append(config["pinces"][id]["id"])
	ret.append(puissanceReelle)
	ret.append(facteurdePuissance)
	ret.append(Vrms)
	ret.append(Irms)
	if debug:
		print("moyenne V", moyenneV)
		print("moyenne I", moyenneI)
		print("puisssance apparente", puissanceApparente)
		print("nb lecture", nb_lectures)
		print("decalage V", decalageV)
		print("decalage I", decalageI)
	return ret, decalageV, decalageI

def main(decalageV, decalageI, debug = False):
	while True:
		idPince = 0
		for adcPince in config["pinces"]:
			m, decalageV, decalageI = mesure(idPince, decalageV, decalageI, debug)
			if debug:
				print(f"{int(m[1])} W, {m[2] * 100:.0f} %, {m[3]:.0f} V, {m[4]:.2f} A")
				print(m)
			print(f"[{int(m[1])}, {m[2] * 100:.0f}, {m[3]:.0f}, {m[4]:.2f}]")
			idPince += 1
		time.sleep(1)

# Pour facilement travailler avec VSCode :

decalageV = 0
decalageI = 0

main(decalageV, decalageI, True)		