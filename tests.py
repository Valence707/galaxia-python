import pygame, math, time, noise

def game_test():
    pygame.init()

    CLOCK = pygame.time.Clock()
    TARGET_FPS = 60
    WINDOW_SIZE = (1200, 800)
    DISPLAY_SIZE = (600, 400)
    WINDOW = pygame.display.set_mode(WINDOW_SIZE)
    DISPLAY = pygame.Surface(DISPLAY_SIZE)
    CENTER_OF_DISPLAY = (math.floor(DISPLAY_SIZE[0]/2), math.floor(DISPLAY_SIZE[1]/2))
    DISPLAY_TO_WIN = (DISPLAY_SIZE[0]/WINDOW_SIZE[0], DISPLAY_SIZE[1]/WINDOW_SIZE[1])

    class Rectangle(pygame.sprite.Sprite):
        def __init__(self, pos=[0, 0], size=[10, 10], color=(0, 0, 0)):
            super().__init__()
            self.image = pygame.Surface(size)
            self.rect = self.image.get_rect()
            self.truePos = pos
            self.rect.x, self.rect.y = pos
            self.worldPos = [0, 0]
            self.velocity = [0, 0]
            self.acceleration = [0.5, 0.25]
            self.maxVelocity = [5, 5]
            self.fallVelocity = 12
            self.flyVelocity = -8
            self.jumpTimer = 0

            pygame.Surface.fill(self.image, color)

    player = Rectangle(color=(255, 0, 255), size=[30,30])

    solids = pygame.sprite.Group()

    for i in range(50):
        solids.add(Rectangle(pos=[21*i, 50], size=[20, 20], color=(0, 155, 0)))

    prev_time = time.time()

    slowMode = False
    slowModeTimer = 0

    run = True

    while run:

            # now = time.time()
            # dt = (now - prev_time) * TARGET_FPS
            # prev_time = now

            dt = (CLOCK.tick(60) * .001 * TARGET_FPS)

            keys = pygame.key.get_pressed()
            pygame.Surface.fill(DISPLAY, (220, 210, 255))

            if keys[pygame.K_q]:
                run = False
                break

            if keys[pygame.K_e] and slowModeTimer == 0:
                slowMode = True if slowMode == False else False
                slowModeTimer = 100

            if slowModeTimer > 0:
                slowModeTimer -= 1

            if slowMode:
                for i in range(500):
                    print(CLOCK.get_fps(), dt)
            else:
                print(CLOCK.get_fps(), dt)

            # Flying (for debug)
            if keys[pygame.K_w]:
                player.velocity[1] -= 1 * dt

            if keys[pygame.K_a]:
                player.velocity[0] -= 1 * dt

            if keys[pygame.K_d]:
                player.velocity[0] += 1 * dt

            if keys[pygame.K_SPACE] and player.jumpTimer < 2:
                player.velocity[1] -= 12
                player.jumpTimer = 2

            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                if player.velocity[0] > 1:
                    player.velocity[0] -= player.acceleration[0] * dt
                elif player.velocity[0] < -1:
                    player.velocity[0] += player.acceleration[0] * dt
                else:
                    player.velocity[0] = 0
            
            if abs(player.velocity[0]):
                player.velocity[0] = player.maxVelocity[0] if player.velocity[0] > player.maxVelocity[0] else -1*player.maxVelocity[0] if player.velocity[0] < -1*player.maxVelocity[0] else player.velocity[0]

            player.velocity[1] += 0.5 * dt

            # Player falling and flying velocity constraints
            player.velocity[1] = player.fallVelocity if player.velocity[1] > player.fallVelocity else player.flyVelocity if player.velocity[1] < player.flyVelocity else player.velocity[1]

            # Horizontal player movement and collision detection
            if abs(player.velocity[0]):
                player.truePos[0] += math.floor(player.velocity[0]*dt)
                player.rect.x = math.floor(player.truePos[0])
                collided = pygame.sprite.spritecollideany(player, solids)
                if collided:
                    if player.rect.left < collided.rect.left:
                        player.truePos[0] = collided.rect.x - player.rect.width
                    elif player.rect.right > collided.rect.right:
                        player.truePos[0] = collided.rect.right

                    player.velocity[0] = 0
                    player.rect.x = player.truePos[0]

            # Vertical player movement and collision detection
            if abs(player.velocity[1]):
                player.truePos[1] += math.floor(player.velocity[1]*dt)
                differenceInPos = player.rect.x - player.truePos[1]
                print(differenceInPos)
                player.rect.y = math.floor(player.truePos[1])
                collided = pygame.sprite.spritecollideany(player, solids)
                if collided:
                    if player.rect.top < collided.rect.top:
                        player.truePos[1] = collided.rect.y - player.rect.height
                    elif player.rect.bottom > collided.rect.bottom:
                        player.truePos[1] = collided.rect.bottom

                    if player.jumpTimer == 2 and not keys[pygame.K_SPACE]:
                        player.jumpTimer = 0
                    player.velocity[1] = 0
                    player.rect.y = player.truePos[1]

            # Move entire screen
            trueScroll = [
                (CENTER_OF_DISPLAY[0] - player.rect.x - player.rect.width/2),
                (CENTER_OF_DISPLAY[1] - player.rect.y - player.rect.height/2)
                ]
                
            scrollAmount = trueScroll.copy()
            scrollAmount = [math.floor(scrollAmount[0]), math.floor(scrollAmount[1])]
                    
            player.truePos = [player.truePos[0]+scrollAmount[0], player.truePos[1]+scrollAmount[1]]
            player.rect.x, player.rect.y = player.truePos
            player.worldPos = [player.worldPos[0]-scrollAmount[0], player.worldPos[1]-scrollAmount[1]]

            for sprite in solids:
                sprite.rect = sprite.rect.move(scrollAmount)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            solids.draw(DISPLAY)
            DISPLAY.blit(player.image, (player.rect.x, player.rect.y))

            # print(CLOCK.get_fps())
            WINDOW.blit(pygame.transform.scale(DISPLAY, WINDOW_SIZE), (0, 0))
            pygame.display.flip()

def one_d_noise_test():
    noiseTest = []
    noiseWidth = 66

    # Height of noisemap
    noiseHeight = 40

    # Greater values zoom in, smaller values zoom out
    noiseScale = 350

    octaves = 5
    lacunarity = 3
    persistence = 0.5
    xOffset = 400
    height = 50

    for j in range(noiseHeight):
        noiseTest.append([])
        for i in range(noiseWidth):
            noiseResult = abs(int(noise.pnoise1((i+xOffset)/noiseScale, octaves=octaves, lacunarity=lacunarity, persistence=persistence)*height))+j

            if noiseResult > noiseHeight-2:
                noiseTest[j].append('O')
            else:
                noiseTest[j].append('.')
        
    for i in noiseTest:
        print(i)

# one_d_noise_test()

def two_d_noise_test():
    noiseTest = []
    noiseWidth = 300

    # Height of noisemap
    noiseHeight = 66

    # Smaller values zoom in, greater values zoom out
    noiseScale = 7

    octaves = 3
    lacunarity = 4
    persistence = 0.25
    xOffset = 66*4
    yOffset = 66*5
    depth = 1000

    for row in range(noiseHeight):
        noiseTest.append([])
        for col in range(noiseWidth):
            noiseResult = int(noise.pnoise2((col/noiseWidth*noiseScale)+xOffset, (row/noiseHeight*noiseScale)+yOffset, octaves=octaves, lacunarity=lacunarity, persistence=persistence)*depth)+350

            if noiseResult < 0:
                noiseTest[row].append('#')

            else:
                noiseTest[row].append('`')
        
    with open('noise_output.txt', 'w') as file:
        for row in noiseTest:
            for col in row:
                file.write(col)
            
            file.write('\n')

two_d_noise_test()