import time, math, machine

### CONFIG et initialisation ###
adcPinces = []

# Configure des broches GPIO comme entrées ADC des pinces
adcPinces.append(machine.ADC(machine.Pin(26)))
#adcPinces.append(machine.ADC(machine.Pin(27)))

# Configure de la broche GPIO comme entrée ADC transformateur
adcTransfo = machine.ADC(machine.Pin(28))

# Calibration de la phase
# Prend en compte le déphasage dû au transfo et au temps de lecture entre U de référence et I de la pince
PHASECAL = 0

# Calibration pour la mesure de la tension
tensionReseau = 230
resistances = [10_000, 200_000]
tensionSortieTransfo = 12.33
# Tension du réseau
VCAL = (resistances[0] + resistances[1]) * tensionReseau / resistances[0] / tensionSortieTransfo

# Calibration pour la mesure du courant
nbToursPince = 2000
resistanceTirage = 150
ICAL = nbToursPince / resistanceTirage


# RP2040 lit sur 3.3 V et 2^16 bits
facteurCorrection = 3.3 / 65536
decalageV = 0
decalageI = 0

### PROGRAMME ###

def mesure(id, adc, decalageV, decalageI):
	ret = []
	nb_lectures = 0

	lectureV = 0
	sommeVcarre = 0
	sommeIcarre = 0
	sommePinstantanee = 0
	sommeI = 0 
	sommeV = 0
	# On boucle pendant n ms
	end_time = time.ticks_add(time.ticks_ms(), 500)
	while time.ticks_diff(end_time, time.ticks_ms()) > 0:
		nb_lectures += 1	

		derniereLectureV = lectureV		

		# lecture ADC
		lectureVbrute = adcTransfo.read_u16()
		lectureIbrute = adc.read_u16()

		# valeurs corrigées
		# decalageV += (lectureVbrute - decalageV) / 65536
		# decalageI += (lectureIbrute - decalageI) / 65536
		lectureV = lectureVbrute - 32768 - decalageV
		lectureI = lectureIbrute - 32768 - decalageI
#		print(adc.read_u16() - 32768)
		sommeI += lectureI 
		sommeV += lectureV 

		# caclcul rms
		Vcarre = lectureV * lectureV
		sommeVcarre += Vcarre
		Icarre = lectureI * lectureI
		sommeIcarre += Icarre

		# calibration de la phase
		lectureVdecalee = derniereLectureV + PHASECAL * (lectureV - derniereLectureV)

		# puissance instantanée
		Pinstantanee = lectureVdecalee * lectureI
#		print(lectureVdecalee, lectureI)
		sommePinstantanee += Pinstantanee

	# calculs post boucle
	Vrms = math.sqrt(sommeVcarre / nb_lectures) * facteurCorrection * VCAL
	Irms = math.sqrt(sommeIcarre / nb_lectures) * facteurCorrection * ICAL
	puissanceReelle = sommePinstantanee / nb_lectures * facteurCorrection * VCAL * facteurCorrection * ICAL
	puissanceApparente = Vrms * Irms
	facteurdePuissance = puissanceReelle / puissanceApparente
	moyenneV = sommeV/nb_lectures
	print("moyenne V", moyenneV)
	decalageV = decalageV + moyenneV / 64 # pour converger
	moyenneI = sommeI/nb_lectures
	print("moyenne I", moyenneI)
	decalageI = decalageI + moyenneI / 64 # pour converger
	print("puisssance apparente", puissanceApparente)
	ret.append(id)
	ret.append(puissanceReelle)
	ret.append(facteurdePuissance)
	ret.append(Vrms)
	ret.append(Irms)
	print("nb lecture", nb_lectures)
	return ret, decalageV, decalageI

while True:
	idPince = 0
	for adcPince in adcPinces:
		idPince += 1
		ret, decalageV, decalageI = mesure(idPince, adcPince, decalageV, decalageI)
		print(ret, decalageV, decalageI)
	time.sleep(1)