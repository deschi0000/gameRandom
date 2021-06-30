from random import randint


def genre():
	GENRES = [ 
        "action", "indie", "adventure", "rpg", "strategy", "casual", 
        "simulation","puzzle", "arcade", "platformer",
         "racing", "sports", "fighting", "family"
        ]
	index = randint(0, len(GENRES)-1)
	return GENRES[index]

def platform():
	PLATFORMS = [
        "pc", "playstation5", "playstation4", "playstation3", "playstation2",
        "playstation", "xboxone", "xbox360", "xbox", "nintendoswitch", "wiiu",
        "wii", "gamecube", "supernintendo", "nes", "genesis", "dreamcast"
        ] 
	index = randint(0, len(PLATFORMS)-1)
	return PLATFORMS[index]	

'''
def random_url(genre_chooser, platform_chooser, random_page=randint(100,200)):
        random_url = f"https://api.rawg.io/api/games?genre={genre_chooser}&platform={platform_chooser}&key=c81b9645113443c78b9de09a1b561ac9&page={random_page}"
        return random_url     
'''
