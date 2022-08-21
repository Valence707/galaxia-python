# Galaxia
A Terraria-like side-scroller wherein you can break and place blocks and explore a procedurally-generated tile-based world. As of 8-20-2022, this is a WIP, and the code on Github is merely a basic demonstration of the idea of the game. 

Galaxia is made in Pygame and uses an older Perlin Noise library (aptly named "noise") that must be manually installed from the included wheel.

If you are reading this sentence, that means that this game is discontinued and will not be updated. Python and Pygame prove too slow for the type of computations required to make Galaxia work. Some specific limitations include:
  > Python being an interpreted high-level language,
  > Pygame being a wrapper for the SDL multimedia library,
  > Bulk-loading tiles synchronously in "chunks" causes frame stutter, and doing it asynchronously in Python is overkill and counterintuitive,
  > My own inexperience with Python's lower-level and more abstract functionality that I know I could leverage to solve the framerate issues this game has,
  > Things are just too high-level and all the clutter adds up to make the game run pretty slowly. I've implemented a framerate independence algorithm that keeps the game running at the same rate despite framerate, but it just isn't as fun to play if the framerate fluctuates constantly around 60 and dips every time the player traverses chunks. I hope to overcome these limitations by recreating the game in C++ or Java. I will post an update here if that plan ever comes to fruition.
