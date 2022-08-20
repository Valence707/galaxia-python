import pygame, math, noise, random

pygame.init()

# Constants
TARGET_FPS = 60
WIN_SIZE = (1200, 800)
DISPLAY_SIZE = (600, 400)
DISPLAY_CENTER = (math.floor(DISPLAY_SIZE[0]/2), math.floor(DISPLAY_SIZE[1]/2))
DISPLAY_TO_WIN = (DISPLAY_SIZE[0]/WIN_SIZE[0], DISPLAY_SIZE[1]/WIN_SIZE[1])
TILE_SIZE = (16, 16)
CHUNK_TILES = (25, 25)
CHUNK_SIZE = (CHUNK_TILES[0]*TILE_SIZE[0], CHUNK_TILES[1]*TILE_SIZE[1])
WORLD_TILES = (1000, 750)
GRAVITY = 0.25

pygame.display.set_caption("Galaxia")

class Rectangle(pygame.sprite.Sprite):
    def __init__(self, size=[10, 10], image=None, color=None, pos=[0, 0]):
        super().__init__()
        if image:
            self.image = image
        elif color:
            self.image = pygame.Surface(size)
            pygame.Surface.fill(self.image, color)
        else:
            self.image = pygame.Surface(size)
            pygame.Surface.fill(self.image, (0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

class Tile(pygame.sprite.Sprite):
    def __init__(self, posInChunk, chunk, tileType, pos=None):
        super().__init__()

        if tileType == '1':
            self.image = textures['grass_dirt']
            self.tileType = 'dirt'

        elif tileType == '2':
            self.image = textures['dirt']
            self.tileType = 'dirt'

        elif tileType == '3':
            self.image = textures['stone']
            self.tileType = 'stone'

        elif tileType == '4':
            self.image = textures['coal_ore']
            self.tileType = 'stone'
        elif tileType == '5':
            self.image = textures['copper_ore']
            self.tileType = 'stone'
        elif tileType == '6':
            self.image = textures['iron_ore']
            self.tileType = 'stone'
        elif tileType == '7':
            self.image = textures['gold_ore']
            self.tileType = 'stone'
        
        self.rect = self.image.get_rect()

        self.chunk = chunk
        self.posInChunk = posInChunk
        if pos:
            self.rect.x, self.rect.y = pos
            self.add(solidTiles)

class Wall(Rectangle):
    def __init__(self, posInChunk, chunk, wallType, pos=None):
        super().__init__()

        if pos:
            self.rect.x, self.rect.y = pos
            self.add(walls)

        if wallType == '1':
            self.image = textures['dirt_wall']
            self.wallType = 'dirt_wall'

        elif wallType == '3':
            self.image = textures['stone_wall']
            self.wallType = 'stone_wall'

        elif wallType == 'g1':
            self.image = textures['grass_0']
            self.wallType = 'grass_0'
        elif wallType == 'g2':
            self.image = textures['grass_1']
            self.wallType = 'grass_1'
        elif wallType == 'g3':
            self.image = textures['grass_2']
            self.wallType = 'grass_2'
        elif wallType == 'g4':
            self.image = textures['grass_3']
            self.wallType = 'grass_3'
        elif wallType == 'g5':
            self.image = textures['grass_4']
            self.wallType = 'grass_4'
        elif wallType == 'g6':
            self.image = textures['grass_5']
            self.wallType = 'grass_5'

        elif wallType == 'tb':
            self.image = textures['tree_bottom']
            self.wallType = 'tree'
        elif wallType == 'tm':
            self.image = textures['tree_middle']
            self.wallType = 'tree'
        elif wallType == 'tt':
            self.image = textures['tree_top']
            self.wallType = 'tree'

        if wallType[0] == 'g':
            self.rect.y -= TILE_SIZE[1]

        self.chunk = chunk
        self.posInChunk = posInChunk

    def hide(self):
        self.remove(walls)

    def show(self, pos):
        self.rect.x, self.rect.y = pos
        if self.wallType[0] == 'g':
            self.rect.y -= TILE_SIZE[1]
        self.add(walls)

class Player(Rectangle):
    def __init__(self, size=[10, 10], color=None, image=None, pos=[0, 0]):
        super().__init__(size=size, image=image, color=color, pos=pos)
        self.worldPos = [math.floor(DISPLAY_SIZE[0]/2-12.5), math.floor(DISPLAY_SIZE[1]/2-12.5)]
        self.truePos = [math.floor(DISPLAY_SIZE[0]/2-12.5), -100]
        self.velocity = [0, 0]
        self.maxVelocity = [3, 3]
        self.acceleration = [0.25, 0.25]
        self.flyVelocity = -16
        self.fallVelocity = 12
        self.jumpTimer = 0
        self.chunk = [0, 0]
        self.useTimer = 0

        self.hotbar = {
            'items': [
                {
                    'type': 'tool',
                    'itemId': 'stone_club',
                    'image': 'stone_club',
                    'displayName': 'Stone Club',
                    'inventorySlot': [0, 0]
                },
                {
                    'type': 'tool',
                    'itemId': 'stone_axe',
                    'image': 'stone_axe',
                    'displayName': 'Stone Axe',
                    'inventorySlot': [1, 0]
                },
                {
                    'type': 'tool',
                    'itemId': 'stone_shovel',
                    'image': 'stone_shovel',
                    'displayName': 'Stone Shovel',
                    'inventorySlot': [2, 0]
                },
                {
                    'type': 'tool',
                    'itemId': 'stone_pickaxe',
                    'image': 'stone_pickaxe',
                    'displayName': 'Stone Pickaxe',
                    'inventorySlot': [3, 0]
                },
                {
                    'type': 'tile',
                    'tileId': '2',
                    'itemId': 'dirt',
                    'image': 'dirt',
                    'displayName': 'Dirt Tile',
                    'inventorySlot': [4, 0],
                    'amount': 999
                },
                {
                    'type': 'tile',
                    'tileId': '1',
                    'itemId': 'grass_dirt',
                    'image': 'grass_dirt',
                    'displayName': 'Grass Dirt Tile',
                    'inventorySlot': [5, 0],
                    'amount': 999
                },
                {
                    'type': 'tile',
                    'tileId': '3',
                    'itemId': 'stone',
                    'image': 'stone',
                    'displayName': 'Stone Tile',
                    'inventorySlot': [6, 0],
                    'amount': 999
                },
                {
                    'type': None,
                    'itemId': None,
                    'image': None,
                    'displayName': '',
                    'inventorySlot': [7, 0],
                },
                {
                    'type': None,
                    'itemId': None,
                    'image': None,
                    'displayName': '',
                    'inventorySlot': [8, 0],
                }
            ],
            'selected': 0
        }

    def action(self):
        if self.useTimer <= 0:
            mouseButtonsPressed = pygame.mouse.get_pressed(num_buttons=3)

            if mouseButtonsPressed[0]:
                mouseCollided = pygame.sprite.spritecollideany(mouse, solidTiles)
                if mouseCollided and isinstance(mouseCollided, Tile):
                    distance = int(math.sqrt(abs(player.rect.centerx - mouseCollided.rect.centerx)**2+abs(player.rect.centery - mouseCollided.rect.centery)**2))

                    if distance < 100:
                        if player.hotbar['items'][player.hotbar['selected']]['itemId'] == 'stone_shovel' and mouseCollided.tileType == 'dirt':
                            mouseCollided.kill()
                            world[F'{mouseCollided.chunk[0]},{mouseCollided.chunk[1]}']['tiles'][mouseCollided.posInChunk[1]][mouseCollided.posInChunk[0]] = '`'
                            del mouseCollided

                        elif player.hotbar['items'][player.hotbar['selected']]['itemId'] == 'stone_pickaxe' and mouseCollided.tileType == 'stone':
                            mouseCollided.kill()
                            world[F'{mouseCollided.chunk[0]},{mouseCollided.chunk[1]}']['tiles'][mouseCollided.posInChunk[1]][mouseCollided.posInChunk[0]] = '`'
                            del mouseCollided

                self.useTimer = 15

            elif mouseButtonsPressed[2] and player.hotbar['items'][player.hotbar['selected']]['type'] == 'tile' and not pygame.sprite.spritecollideany(mouse, solidTiles):

                tileIndexInWorld = [
                    math.floor((self.worldPos[0] + mouse.rect.x - DISPLAY_CENTER[0]) / TILE_SIZE[0]),
                    math.floor((self.worldPos[1] + mouse.rect.y - DISPLAY_CENTER[1]) / TILE_SIZE[1])
                ]

                tileIndexInChunk = [
                    tileIndexInWorld[0] % CHUNK_TILES[0],
                    tileIndexInWorld[1] % CHUNK_TILES[1]
                ]

                tileChunk = [
                    math.floor(tileIndexInWorld[0] / CHUNK_TILES[0]),
                    math.floor(tileIndexInWorld[1] / CHUNK_TILES[1])
                ]

                if not F'{tileChunk[0]},{tileChunk[1]}' in world:
                    world[F'{tileChunk[0]},{tileChunk[1]}'] = {
                        'tiles': [],
                        'sprites': pygame.sprite.Group()
                    }

                    for row in range(CHUNK_TILES[1]):
                        world[F'{tileChunk[0]},{tileChunk[1]}']['tiles'].append([])
                        for col in range(CHUNK_TILES[0]):
                            world[F'{tileChunk[0]},{tileChunk[1]}']['tiles'][row].append('`')

                pos = [
                    tileIndexInChunk[0]*TILE_SIZE[0] + DISPLAY_CENTER[0] + tileChunk[0]*CHUNK_SIZE[0] - player.worldPos[0],
                    tileIndexInChunk[1]*TILE_SIZE[1] + DISPLAY_CENTER[1] + tileChunk[1]*CHUNK_SIZE[1] - player.worldPos[1],
                ]

                distance = int(math.sqrt(abs(player.rect.centerx - pos[0]-TILE_SIZE[0]/2)**2+abs(player.rect.centery - pos[1]-TILE_SIZE[1]/2)**2))

                if distance < 50:

                    playerCollideCheckRect = Rectangle(size=TILE_SIZE, color=(0, 0, 0), pos=pos)

                    if not player.rect.colliderect(playerCollideCheckRect.rect):

                        world[F'{tileChunk[0]},{tileChunk[1]}']['tiles'][tileIndexInChunk[1]][tileIndexInChunk[0]] = player.hotbar['items'][player.hotbar['selected']]['tileId']

                        world[F'{tileChunk[0]},{tileChunk[1]}']['sprites'].add(
                            Tile(
                                posInChunk = (tileIndexInChunk[0], tileIndexInChunk[1]), 
                                chunk = tileChunk, 
                                tileType = player.hotbar['items'][player.hotbar['selected']]['tileId'], 
                                pos=pos
                                )
                            )

                    del playerCollideCheckRect

                self.useTimer = 5
        else:
            self.useTimer -= dt

    def update(self):
        pass

class Cloud(Rectangle):
    def __init__(self, image):
        super().__init__(image=image)
        self.truePos = [random.randrange(-50, DISPLAY_SIZE[0] - self.rect.width), random.randrange(-50, DISPLAY_CENTER[1] - self.rect.height)]
        self.rect.y = self.truePos[1]
        self.velocity = (random.random() + 0.1) * 0.3

    def move(self):
        self.truePos[0] += self.velocity
        self.rect.x = math.floor(self.truePos[0])
        if self.rect.x > DISPLAY_SIZE[0]:
            self.truePos[0] = -1 * self.rect.width - 50
            self.rect.y = random.randrange(0, DISPLAY_CENTER[1])
            self.velocity = (random.random() + 0.1) * 0.75

# World generation.
def generate_world(size):

    # INITIALIZATION
    startTime = pygame.time.get_ticks()
    tileMap = []
    wallMap = []
    newWorld = {}

    # Initialize tile and wall maps
    for row in range(WORLD_TILES[1]):
        tileMap.append([])
        wallMap.append([])

        for col in range(WORLD_TILES[0]):
            tileMap[row].append('`')
            wallMap[row].append('`')

    # Generate solid terrain
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row
            newTileType = ''
            newWallType = ''
                    
            # Stone
            if tileHeight > 60:
                newTileType = '3'
                newWallType = '3'

            # Dirt
            elif tileHeight > 50:

                # DRAW CHUNK BORDERS
                # if xBlock % CHUNK_TILES[0] == 0 or xBlock % CHUNK_TILES[0] == CHUNK_TILES[0]-1:
                #     newWorld[F'{xChunk-math.floor(size[0]/2)},{yChunk-3}']['tiles'][yBlock][xBlock] = '3'
                # else:

                newTileType = '2'
                newWallType = '1'

            # Grass Dirt
            elif tileHeight > 49:
                newTileType = '1'
                newWallType = '1'

            else:
                newTileType = '`'
                newWallType = '`'

            if newTileType != '':
                tileMap[row][col] = newTileType

            if newWallType != '`':
                wallMap[row][col] = newWallType

    # Generate caves
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):

            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row

            if tileHeight > 55:
                noiseResult = int(noise.pnoise2(((col)/80), ((row)/80), octaves=4, lacunarity=2, persistence=1)*20)

                if noiseResult < 0:
                    tileMap[row][col] = '`'

    # Generate Ores

    # Coal Ore
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row
            
            if tileHeight > 55 and tileMap[row][col] == '3':
                noiseResult = int(noise.pnoise2(((col)/10), ((row)/10), octaves=5, lacunarity=4, persistence=0.25)*100)+27

                if noiseResult < 0:
                    tileMap[row][col] = '4'

    # Copper Ore
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row

            if tileHeight > 55 and tileMap[row][col] == '3':
                noiseResult = int(noise.pnoise2(((col+200)/20), ((row+200)/20), octaves=3, lacunarity=3, persistence=0.25)*100)+36

                if noiseResult < 0:
                    tileMap[row][col] = '5'

    # Iron Ore
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row

            if tileHeight > 55 and tileMap[row][col] == '3':
                noiseResult = int(noise.pnoise2(((col+400)/20), ((row+400)/20), octaves=3, lacunarity=3, persistence=0.25)*100)+36

                if noiseResult < 0:
                    tileMap[row][col] = '6'

    # Gold Ore
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            tileHeight = abs(int(noise.pnoise1((col+200)/600, octaves=5, lacunarity=3, persistence=0.5)*50))+row
            
            if tileHeight > 55 and tileMap[row][col] == '3':
                noiseResult = int(noise.pnoise2(((col+600)/20), ((row+600)/20), octaves=3, lacunarity=3, persistence=0.2)*100)+38

                if noiseResult < 0:
                    tileMap[row][col] = '7'
            
    with open('world.txt', 'w') as worldFile:
        for row in tileMap:
            lineToWrite = ''
            for col in row:
                lineToWrite += col
            lineToWrite += '\n'
            worldFile.write(lineToWrite)

    # Generate Surface Foliage
    for row in range(WORLD_TILES[1]):
        for col in range(WORLD_TILES[0]):
            if tileMap[row][col] == '1':
                foliage = random.randrange(0, 100)
                newPlant = None

                # Generate grass
                if foliage < 75:
                    newPlant = F'g{random.randrange(1, 7)}'

                # Generate trees
                elif foliage >= 95:
                    newPlant = 'tree'

                if newPlant and newPlant != 'tree':
                    wallMap[row][col] = newPlant

                elif newPlant == 'tree':
                    treeHeight = random.randrange(1, 10)
                    wallMap[row-1][col] = 'tb'
                    for height in range(treeHeight):
                        wallMap[row-height-2][col] = 'tm'

                    wallMap[row-4-treeHeight][col-1] = 'tt'

    # Initialize empty world chunks based on generated tileMap
    for yChunk in range(math.floor(WORLD_TILES[1] / CHUNK_TILES[1])):
        for xChunk in range(math.floor(WORLD_TILES[0] / CHUNK_TILES[0])):
            chunkString = F'{xChunk-math.floor(size[0]/2)},{yChunk-3}'

            newWorld[chunkString] = {
                'tiles': [],
                'walls': [],
                'sprites': pygame.sprite.Group()
            }

            for yBlock in range(CHUNK_TILES[1]):
                newWorld[chunkString]['tiles'].append([])
                newWorld[chunkString]['walls'].append([])

                for xBlock in range(CHUNK_TILES[0]):
                    newWorld[chunkString]['tiles'][yBlock].append('`')
                    newWorld[chunkString]['walls'][yBlock].append('`')

    # Convert tile and wall maps to chunk maps
    for yChunk in range(math.floor(WORLD_TILES[1] / CHUNK_TILES[1])):
        for xChunk in range(math.floor(WORLD_TILES[0] / CHUNK_TILES[0])):
            chunkString = F'{xChunk-math.floor(size[0]/2)},{yChunk-3}'
            
            for yBlock in range(CHUNK_TILES[1]):
                for xBlock in range(CHUNK_TILES[0]):

                    newWorld[chunkString]['tiles'][yBlock][xBlock] = tileMap[abs(yChunk)*CHUNK_TILES[1] + yBlock][abs(xChunk)*CHUNK_TILES[0] + xBlock]
                    newWorld[chunkString]['walls'][yBlock][xBlock] = wallMap[abs(yChunk)*CHUNK_TILES[1] + yBlock][abs(xChunk)*CHUNK_TILES[0] + xBlock]

    print(F'GENERATED WORLD IN {pygame.time.get_ticks() - startTime} MS')

    return newWorld

def update_memory_region():
    pass

def unload_chunk(chunk):
    chunkString = F'{chunk[0]},{chunk[1]}'
    if chunk in drawnChunks:
        drawnChunks.remove(chunk)
        if chunkString in world:
            for sprite in world[chunkString]['sprites']:
                sprite.kill()
                del sprite

    print(len(solidTiles), len(walls))

def load_chunk(chunk):
    chunkString = F'{chunk[0]},{chunk[1]}'

    drawnChunks.append(chunk)

    if chunkString in world:
        tilePosOffset = [
            DISPLAY_CENTER[0] + chunk[0]*CHUNK_SIZE[0] - player.worldPos[0] - scrollAmount[0],
            DISPLAY_CENTER[1] + chunk[1]*CHUNK_SIZE[1] - player.worldPos[1] - scrollAmount[1]
        ]

        for row in enumerate(world[chunkString]['tiles']):
            for col in enumerate(row[1]):
                pos = [
                    col[0]*TILE_SIZE[0] + tilePosOffset[0],
                    row[0]*TILE_SIZE[1] + tilePosOffset[1]
                ]

                tileType = col[1]
                wallType = world[chunkString]['walls'][row[0]][col[0]]

                if tileType != '`':
                    world[chunkString]['sprites'].add(Tile(posInChunk=(col[0], row[0]), chunk=chunk, tileType=col[1], pos=pos))

                if wallType != '`':
                    world[chunkString]['sprites'].add(Wall(posInChunk=(col[0], row[0]), chunk=chunk, wallType=wallType, pos=pos))

def scroll_screen(amount):
    scrollAmount = amount.copy()
    scrollAmount = [(scrollAmount[0]), (scrollAmount[1])]
            
    player.truePos = [player.truePos[0]+scrollAmount[0], player.truePos[1]+scrollAmount[1]]
    player.rect.x, player.rect.y = player.truePos
    player.worldPos = [player.worldPos[0]-scrollAmount[0], player.worldPos[1]-scrollAmount[1]]

    for sprite in solidTiles:
        sprite.rect = sprite.rect.move(scrollAmount)

    for sprite in walls:
        sprite.rect = sprite.rect.move(scrollAmount)

# Game objects
clock = pygame.time.Clock()
win = pygame.display.set_mode(WIN_SIZE)
display = pygame.Surface(DISPLAY_SIZE)

textures = {
    'dirt': pygame.image.load('./images/dirt.png').convert(),
    'grass_dirt': pygame.image.load('./images/grass_dirt.png').convert(),
    'stone': pygame.image.load('./images/stone.png').convert(),
    'cloud_1': pygame.image.load('./images/cloud_1.png').convert(),
    'cloud_2': pygame.image.load('./images/cloud_2.png').convert(),
    'cloud_3': pygame.image.load('./images/cloud_3.png').convert(),
    'cloud_4': pygame.image.load('./images/cloud_4.png').convert(),
    'mountains': pygame.image.load('./images/mountains.png').convert(),
    'hotbar': pygame.image.load('./images/hotbar.png').convert(),
    'hotbar_selected': pygame.image.load('./images/hotbar_selected.png').convert(),
    'stone_pickaxe': pygame.image.load('./images/stone_pickaxe.png').convert(),
    'stone_shovel': pygame.image.load('./images/stone_shovel.png').convert(),
    'stone_axe': pygame.image.load('./images/stone_axe.png').convert(),
    'stone_club': pygame.image.load('./images/stone_club.png').convert(),
    'dirt_wall': pygame.image.load('./images/dirt_wall.png').convert(),
    'stone_wall': pygame.image.load('./images/stone_wall.png').convert(),
    'grass_0': pygame.image.load('./images/grass_0.png').convert(),
    'grass_1': pygame.image.load('./images/grass_1.png').convert(),
    'grass_2': pygame.image.load('./images/grass_2.png').convert(),
    'grass_3': pygame.image.load('./images/grass_3.png').convert(),
    'grass_4': pygame.image.load('./images/grass_4.png').convert(),
    'grass_5': pygame.image.load('./images/grass_5.png').convert(),
    'tree_top': pygame.image.load('./images/tree_top.png').convert(),
    'tree_middle': pygame.image.load('./images/tree_middle.png').convert(),
    'tree_bottom': pygame.image.load('./images/tree_bottom.png').convert(),
    'coal_ore': pygame.image.load('./images/coal_ore.png').convert(),
    'copper_ore': pygame.image.load('./images/copper_ore.png').convert(),
    'iron_ore': pygame.image.load('./images/iron_ore.png').convert(),
    'gold_ore': pygame.image.load('./images/gold_ore.png').convert()
}

# Texture processing
for key in textures:
    textures[key].set_colorkey((0, 255, 0))

textures['hotbar'].set_alpha(255)

# Sprite groups
solidTiles = pygame.sprite.Group()
nonSolidTiles = pygame.sprite.Group()
walls = pygame.sprite.Group()
lightingTiles = pygame.sprite.Group()
items = pygame.sprite.Group()
enemies = pygame.sprite.Group()

clouds = pygame.sprite.Group()

mountains = pygame.transform.scale(textures['mountains'], (DISPLAY_SIZE[0], (DISPLAY_SIZE[0] / textures['mountains'].get_rect().width) * textures['mountains'].get_rect().height))

for i in range(12):
    cloudToAdd = Cloud(textures[F'cloud_{random.randrange(1, 5)}'])
    cloudToAdd.image.set_alpha(150)
    clouds.add(cloudToAdd)

player = Player(color=(255, 0, 0), size=(20, 20), pos=[math.floor(DISPLAY_SIZE[0]/2-10), 0])
mouse = Rectangle(size=[1, 1], color=(0, 0, 0))

timeElapsed = 0

gameTitle = {
    'sprite': pygame.font.SysFont(None, 64).render('GALAXIA', True, (255, 255, 255))
}

gameTitle['width'] = gameTitle['sprite'].get_width()
gameTitle['xPos'] = DISPLAY_CENTER[0] - math.floor(gameTitle['sprite'].get_width() / 2)

startText = {
    'sprite': pygame.font.SysFont(None, 36).render('Press the \'S\' key to start', True, (255, 255, 255))
}

startText['width'] = startText['sprite'].get_width()
startText['xPos'] = DISPLAY_CENTER[0] - math.floor(startText['sprite'].get_width() / 2)

fpsDisplay = pygame.font.SysFont(None, 16)
hotbarText = pygame.font.SysFont(None, 16)
startButtonText = pygame.font.SysFont(None, 24)

invHoverBox = Rectangle()

# Variables
world = {}
drawnChunks = []
loadedChunks = []

trueScroll = [0, 0]
scrollAmount = [0, 0]

slowMode = False
slowModeTimer = 0

backgroundColor = [200, 190, 255]

dt = 0

def main():
    run = True
    gameState = 'startScreen'
    global drawnChunks, trueScroll, timeElapsed, world, slowMode, slowModeTimer, dt, gameTitle

    pygame.mouse.set_visible(True)

    while run:

        dt = (clock.tick(TARGET_FPS) * .001 * TARGET_FPS)
        # dt = 1

        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        if gameState == 'startScreen':
            pygame.Surface.fill(display, (10, 10, 10))
            timeElapsed += 1
            if keys[pygame.K_q]:
                run = False
                break
            
            for event in events:
                if event.type == pygame.QUIT:
                    run = False

            if keys[pygame.K_s]:
                gameState = 'game'
                
                world = generate_world([math.floor(WORLD_TILES[0] / CHUNK_TILES[0]), math.floor(WORLD_TILES[1] / CHUNK_TILES[1])])

                # Find player's spawn

                player.truePos[1] = -1000

                newDrawnChunks = [
                    [player.chunk[0]-1, player.chunk[1]-1], [player.chunk[0], player.chunk[1]-1], [player.chunk[0]+1, player.chunk[1]-1],
                    [player.chunk[0]-1, player.chunk[1]], [player.chunk[0], player.chunk[1]], [player.chunk[0]+1, player.chunk[1]],
                    [player.chunk[0]-1, player.chunk[1]+1], [player.chunk[0], player.chunk[1]+1], [player.chunk[0]+1, player.chunk[1]+1],
                ]

                for chunk in newDrawnChunks:
                    load_chunk(chunk)

            display.blit(gameTitle['sprite'], (gameTitle['xPos'], 30))
            display.blit(startText['sprite'], (startText['xPos'], 90))

            if gameTitle['sprite'].get_rect().colliderect(mouse.rect):
                print("MOUSE")

        elif gameState == 'game':
            pygame.Surface.fill(display, backgroundColor)

            if keys[pygame.K_q]:
                run = False
                break

            # Change inventory
            if keys[pygame.K_1]:
                player.hotbar['selected'] = 0
            elif keys[pygame.K_2]:
                player.hotbar['selected'] = 1
            elif keys[pygame.K_3]:
                player.hotbar['selected'] = 2
            elif keys[pygame.K_4]:
                player.hotbar['selected'] = 3
            elif keys[pygame.K_5]:
                player.hotbar['selected'] = 4
            elif keys[pygame.K_6]:
                player.hotbar['selected'] = 5
            elif keys[pygame.K_7]:
                player.hotbar['selected'] = 6
            elif keys[pygame.K_8]:
                player.hotbar['selected'] = 7
            elif keys[pygame.K_9]:
                player.hotbar['selected'] = 8

            # Flying (for debug)
            if keys[pygame.K_w]:
                # player.velocity[1] -= 1 * dt
                player.velocity[1] -= 2 * dt

            if keys[pygame.K_a] and abs(player.velocity[0] - player.acceleration[0] * dt) <= player.maxVelocity[0]:
                player.velocity[0] -= player.acceleration[0] * dt

            if keys[pygame.K_d] and player.velocity[0] + player.acceleration[0] * dt <= player.maxVelocity[0]:
                player.velocity[0] += player.acceleration[0] * dt

            if keys[pygame.K_SPACE] and player.jumpTimer < 2:
                player.velocity[1] = -6
                player.jumpTimer = 2

            if not keys[pygame.K_a] and not keys[pygame.K_d] and abs(player.velocity[0]):
                player.velocity[0] = player.velocity[0] - player.acceleration[0] * dt if player.velocity[0] > 1 else player.velocity[0] + player.acceleration[0] * dt if player.velocity[0] < -1 else 0

            # Gravity
            player.velocity[1] += GRAVITY * dt

            # Player falling & flying constraints
            if player.velocity[1] > player.fallVelocity:
                player.velocity[1] -= GRAVITY * dt
            elif player.velocity[1] < player.flyVelocity:
                player.velocity[1] += 2 * dt

            previousChunk = player.chunk.copy()

            # Horizontal player movement and collision detection
            if abs(player.velocity[0]):
                player.chunk[0] = math.floor(player.worldPos[0] / CHUNK_SIZE[0])
                player.truePos[0] += player.velocity[0] * dt
                dp = player.truePos[0] - player.rect.x

                if abs(dp) > TILE_SIZE[0]:
                    collided = None

                    factor = int(dp / TILE_SIZE[0])
                    movements = [dp - factor*TILE_SIZE[0]]

                    for i in range(abs(factor)):
                        movements.append(TILE_SIZE[0] * -1 if factor < 0 else TILE_SIZE[0])

                    for move in movements:
                        player.rect.x += move
                        collided = pygame.sprite.spritecollideany(player, solidTiles)
                        if collided:
                            break

                else:
                    player.rect.x = math.floor(player.truePos[0])
                    collided = pygame.sprite.spritecollideany(player, solidTiles)

                if collided:
                    if player.rect.left < collided.rect.left:
                        player.truePos[0] = collided.rect.x - player.rect.width
                    elif player.rect.right > collided.rect.right:
                        player.truePos[0] = collided.rect.right

                    player.velocity[0] = 0
                    player.rect.x = player.truePos[0]

            # Vertical player movement and collision detection
            if abs(player.velocity[1]):
                player.chunk[1] = math.floor(player.worldPos[1] / CHUNK_SIZE[1])
                player.truePos[1] += int(player.velocity[1] * dt)
                dp = player.truePos[1] - player.rect.y

                if abs(dp) > TILE_SIZE[1]:
                    collided = None

                    factor = int(dp / TILE_SIZE[1])
                    movements = [dp - factor*TILE_SIZE[1]]

                    for i in range(abs(factor)):
                        movements.append(TILE_SIZE[1] * -1 if factor < 0 else TILE_SIZE[1])

                    for move in movements:
                        player.rect.y += move
                        collided = pygame.sprite.spritecollideany(player, solidTiles)
                        if collided:
                            break

                else:
                    player.rect.y = int(player.truePos[1])
                    collided = pygame.sprite.spritecollideany(player, solidTiles)

                if collided:
                    if player.rect.top < collided.rect.top:
                        player.truePos[1] = collided.rect.y - player.rect.height
                    elif player.rect.bottom > collided.rect.bottom:
                        player.truePos[1] = collided.rect.bottom

                    if player.jumpTimer <= 2 and not keys[pygame.K_SPACE]:
                        player.jumpTimer = 0
                    player.velocity[1] = 0
                    player.rect.y = player.truePos[1]
            
            if player.chunk != previousChunk:
                print(player.chunk)
                newDrawnChunks = [
                    [player.chunk[0]-1, player.chunk[1]-1], [player.chunk[0], player.chunk[1]-1], [player.chunk[0]+1, player.chunk[1]-1],
                    [player.chunk[0]-1, player.chunk[1]], [player.chunk[0], player.chunk[1]], [player.chunk[0]+1, player.chunk[1]],
                    [player.chunk[0]-1, player.chunk[1]+1], [player.chunk[0], player.chunk[1]+1], [player.chunk[0]+1, player.chunk[1]+1],
                ]

                # "Traverse" world
                # if player.chunk[0]+1 == math.floor(WORLD_CHUNKS[0]/2):
                #     for i in range(3):
                #         newDrawnChunks[i*3+2][0] = math.floor(WORLD_CHUNKS[0]/-2)

                # if player.chunk[0]-1 == math.floor(WORLD_CHUNKS[0]/-2):
                #     for i in range(3):
                #         newDrawnChunks[i*3][0] = math.floor(WORLD_CHUNKS[0]/-2)

                for chunk in newDrawnChunks:
                    if not chunk in drawnChunks:
                        load_chunk(chunk)

                for chunk in drawnChunks:
                    if not chunk in newDrawnChunks:
                        unload_chunk(chunk)

            player.action()

            # Move entire screen
            trueScroll = [
                (DISPLAY_CENTER[0] - player.rect.x - player.rect.width/2),
                (DISPLAY_CENTER[1] - player.rect.y - player.rect.height/2)
                ]

            scroll_screen(trueScroll)

            mouse.rect.x, mouse.rect.y = [pygame.mouse.get_pos()[0]*DISPLAY_TO_WIN[0], pygame.mouse.get_pos()[1]*DISPLAY_TO_WIN[1]]

            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                
                # Traverse hotbar
                if event.type == pygame.MOUSEWHEEL:
                    player.hotbar['selected'] -= event.y

                    if player.hotbar['selected'] < 0:
                        player.hotbar['selected'] = 8
                    elif player.hotbar['selected'] > 8:
                        player.hotbar['selected'] = 0

            for cloud in clouds:
                cloud.move()

            for cloud in enumerate(clouds):
                display.blit(cloud[1].image, (cloud[1].rect.x, cloud[1].rect.y))
                if cloud[0] == 6:
                    display.blit(mountains, (0, DISPLAY_CENTER[1]-100))

            walls.draw(display)
            solidTiles.draw(display)
            display.blit(player.image, (player.rect.x, player.rect.y))
            lightingTiles.draw(display)

            display.blit(textures['hotbar'], (5, 15))

            display.blit(textures['hotbar_selected'], (9+player.hotbar['selected']*29, 18))

            for item in enumerate(player.hotbar['items']):
                if item[1]['itemId']:
                    display.blit(textures[item[1]['image']], (item[1]['inventorySlot'][0]*29+15, 25))

            textToRender = hotbarText.render(player.hotbar['items'][player.hotbar['selected']]['displayName'], True, (0, 0, 0))
            display.blit(textToRender, (textures['hotbar'].get_width()/2 + 5 - textToRender.get_width()/2, 2))

            display.blit(mouse.image, (mouse.rect.x, mouse.rect.y))

        # print(clock.get_fps())
        display.blit(fpsDisplay.render(F'{clock.get_fps()}', True, (0, 0, 0)), (10, 370))
        win.blit(pygame.transform.scale(display, WIN_SIZE), (0, 0))
        pygame.display.flip()

    pygame.quit()

main()