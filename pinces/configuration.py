config = {
	"pinces": [
		# {
		# 	"id": 1,
		# 	"pin": 26,
		# 	"nbTours": 2000,
		# 	"resistanceTirage": 150 # en Ohm
		# },		
    {
			"id": 2,
			"pin": 27,
			"nbTours": 3000,
			"resistanceTirage": 150 # en Ohm
		},		
    # {
		# 	"id": 3,
		# 	"pin": 28,
		# 	"nbTours": 2000,
		# 	"resistanceTirage": 150 # en Ohm
		# }
	],
	"transfo": {
		"pin": 29,
		"Ventree": 230, # en Volt
		"Vsortie": 12.2, # en Volt
		"resistancePontDiviseur": [10_000, 200_000]
	},
	"PHASECAL": 0
}
