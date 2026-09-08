import pygame
import math

#Inizializzazione di Pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulazione Sistema Gioviano")

#Costanti e Colori
WHITE = (255, 255, 255)
JUPITER_COLOR = (210, 180, 140)
IO_COLOR = (255, 255, 0)
EUROPA_COLOR = (200, 200, 255)
GANYMEDE_COLOR = (180, 180, 180)
CALLISTO_COLOR = (100, 100, 100)

class CorpoCeleste:
    G = 6.67428e-11
    #Scala: 300 pixel corrispondono a circa 2 milioni di km (l'orbita di Callisto)
    SCALE = 300 / 2e9
    # Ogni "tick" del programma fa avanzare il tempo di 6 ore
    TIMESTEP = 3600 * 6

    def __init__ (self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.x_vel = 0
        self.y_vel = 0
        self.orbit = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        #Disegna la traccia dell'orbita
        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                px, py = point
                scaled_points.append((px * self.SCALE + WIDTH / 2, py * self.SCALE + HEIGHT / 2))
            pygame.draw.lines(win, self.color, False, scaled_points, 1)

        #Disegna il corpo celeste
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def update_position(self, bodies):
        total_fx = total_fy = 0
        for body in bodies:
            if self == body:
                continue

            dx = body.x - self.x
            dy = body.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance == 0:
               continue

            force = self.G * self.mass * body.mass / distance**2
            theta = math.atan2(dy, dx)

            total_fx += math.cos(theta) * force
            total_fy += math.sin(theta) * force

        # a = F/m, v = v + a*dt
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        #p = p + v*dt
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))
        #Limito la lunghezza della traccia per non intasare la memoria
        if len(self.orbit) > 300:
            self.orbit.pop(0)

def main():
    run = True
    clock = pygame.time.Clock()

    #Creazione dei corpi celesti (Distanze dal centro in metri, Masse in Kg)
    giove = CorpoCeleste(0, 0, 30, JUPITER_COLOR, 1.898e27, "Giove")

    io = CorpoCeleste(421.7e6, 0, 4, IO_COLOR, 8.93e22, "Io")
    io.y_vel = 17334 # m/s (Velocità orbitale iniziale perpendicolare)

    europa = CorpoCeleste(671e6, 0, 4, EUROPA_COLOR, 4.8e22, "Europa")
    europa.y_vel = 13740

    ganimede = CorpoCeleste(1.07e9, 0, 6, GANYMEDE_COLOR, 1.48e23, "Ganimede")
    ganimede.y_vel = 10880

    callisto = CorpoCeleste(1.88e9, 0, 5, CALLISTO_COLOR, 1.08e23, "Callisto")
    callisto.y_vel = 8200

    corpi = [giove, io, europa, ganimede, callisto]

    #Il Game Loop
    while run:
        clock.tick(60) #60 frame per secondo
        WIN.fill((10, 10, 15)) #Sfondo a simulare lo spazio scuro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Aggiorna e disegna
        for corpo in corpi:
            corpo.update_position(corpi)
            corpo.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()