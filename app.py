from flask import Flask, render_template, request, redirect
from random import randint
import requests
import json

# import the folder from the helpers path
import helpers

# creat instance of app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

GENRES = [
	"action", "indie", "adventure", "rpg", "strategy", "casual",
	"simulation","puzzle", "arcade", "platformer",
		"racing", "sports", "fighting", "family"
	]

PLATFORMS = [
	"pc", "playstation5", "playstation4", "playstation3", "playstation2",
	"playstation", "xboxone", "xbox360", "xbox", "nintendoswitch", "wiiu",
	"wii", "gamecube", "supernintendo", "nes"
	]

# the home directory, return index
@app.route("/", methods=["GET", "POST"])
def home():

	return render_template("index.html", genres=GENRES, platforms=PLATFORMS)

# random page, returing random game
@app.route("/random", methods=["GET", "POST"])
def random():

	if request.method == 'POST':

		# check if there is a request to return home
		if request.form.get("return"):
			return redirect("/")

		if request.form.get("refresh"):
			return render_template("random.html", game_name=game_name, game_image=image_url,genres=actual_genres,
				metascore=metascore, avg_play=avg_play, released=released, platforms=platforms,
				description=description, stores=stores, website=website, developers=developers)

		else:

			# determine size of data relative to options chosen, else statement is a generic option with the widest range
			if request.form.get("genrechoice") == "level1":
				random_page = randint(1,50)

			elif request.form.get("genrechoice") == "level2":
				random_page = randint(50, 500)

			# if the user wants fully random, everything will be chosen at random
			elif request.form.get("genrechoice") == "level3":
				random_page = randint(500, 2000)

			else:
				random_page = randint(1,1000)

			# after data size is determined, randomly choose genre and platform
			genre_chooser = helpers.genre()
			platform_chooser = helpers.platform()

			# random page number; can be increased or decreased to lower, increase the data pool accordingly (factors of 20 as per page results)
			first_url = f"https://api.rawg.io/api/games?genre={genre_chooser}&platform={platform_chooser}&key=c81b9645113443c78b9de09a1b561ac9&page={random_page}"


			# upload the json data as text and retrieve a random index from the results
			r = requests.get(first_url)
			name_data = json.loads(r.text)
			index = randint(1, 3)

			# with the index this will get the id of the chosen game, hence all the necessary info
			game_id = name_data["results"][index]["id"]


			# now we finally have our game
			# we need to use the {id} endpoint to access all the data in for the game
			url = f"https://api.rawg.io/api/games/{game_id}?key=c81b9645113443c78b9de09a1b561ac9"
			p = requests.get(url)
			data = json.loads(p.text)

			# Make sure that there is data
			if data is None:
				return redirect("/")

			#retrieve all relevant information from the uploaded json data
			game_name = data["name"]
			image_url = data["background_image"]

			# check the data if 0/None, to which we can adjust what we render on the html page
			if data["playtime"] != 0:
				time = data["playtime"]
				if time == 1:
					avg_play = str(time) + " Hour"
				else:
					avg_play = str(time) + " Hours"
			else:
				avg_play = " "

			# Error check the following data values for None values and adjust accordingly
			if data["released"] is None:
				released = " "
			else:
				released = data["released"]


			if data["metacritic"] is None:
				metascore = "- -"
			else:
				metascore = data["metacritic"]


			if data["description_raw"] is None:
				description = " "
			else:
				description = data["description_raw"]


			# time to get the platforms / genres available for this game
			platforms = []
			for i in data["platforms"]:
				platforms.append(i["platform"]["slug"])

			actual_genres = []
			for i in data["genres"]:
				actual_genres.append(i["name"].lower())

			# obtain websites for the store available to getting the game
			if data["stores"] is None:
				stores = " "
			else:
				stores = []
				for i in data["stores"]:
					stores.append(i["store"]["domain"])


			# get the website for the game for more details
			if data["website"] is None:
				website = "  "
			else:
				website = data["website"]

			# get the developers
			if data["developers"] is None:
				developers = " "
			else:
				developers = []
				for i in data["developers"]:
					developers.append(i["name"])


			return render_template(
				"random.html", game_name=game_name, game_image=image_url,genres=actual_genres,
				metascore=metascore, avg_play=avg_play, released=released, platforms=platforms,
				description=description, stores=stores, website=website, developers=developers, url=url
				)


	return render_template("random.html")



if __name__ == "__main__":
    app.run(debug=True)

