import neat
import pygame
import math
from Car import Car
from Parkingline import Parkingline
from Prize import Prize
from Border import Border
from Obstacle import Obstacle

WIN_WIDTH = 1900
WIN_HEIGHT = 1000
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Self learning car")
generation = 0

#rysujemy auta itp
def draw_window(win, cars, obstacles):


    for car in cars:
        car.draw(win)


    for obstacle in obstacles:
        win.blit(obstacle.obstacle_image, (obstacle.x, obstacle.y))


def eval_genomes(genomes, config):
    global generation

    distance = math.sqrt((160 - 856) ** 2 + (560 - 774) ** 2)

    cars = []
    ge = []
    nets = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car())
        ge.append(genome)

    for car in cars:
        car.distance_b = distance


    parked_car_placement = [[390, 145],
                            [535, 145],
                            [675, 145],
                            [820, 145],
                            [965, 145],
                            [1110, 145],
                            [1250, 145],
                            [1390, 145],
                            [1540, 145],
                            [390, 695],
                            [535, 695],
                            [675, 695],
                            [965, 695],
                            [1110, 695],
                            [1250, 695],
                            [1390, 695],
                            [1540, 695]]

    border_sprites = [['assets/Border1.png'],
                      ['assets/Border2.png'],
                      ['assets/Border3.png'],
                      ['assets/Border4.png'],
                      ['assets/Border5.png'],
                      ['assets/Border6.png']]

    border_placement = [[0, 0],
                        [0, 0],
                        [0, 0],
                        [1804, 0],
                        [0, 868],
                        [0, 706]]

    parking_lines_sprites = [['assets/parking_line.png'],
                             ['assets/parking_line2.png'],
                             ['assets/parking_line3.png']]

    parking_lines_cords = [[766, 671],
                           [914, 671],
                           [762, 653]]

    parking_lines = []
    for n, x in enumerate(parking_lines_cords):
        parking_lines.append(Parkingline(parking_lines_sprites[n][0], x[0], x[1]))

    obstacles = []
    for x in parked_car_placement:
        obstacles.append(Obstacle(x[0], x[1]))

    for n, x in enumerate(border_placement):
        obstacles.append(Border(border_sprites[n][0], x[0], x[1]))

    parking = Prize(800, 675)

    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    screen.blit(parking.parking_image, (parking.x, parking.y))
    map = pygame.image.load('assets/Map.png')
    act_time = 0
    generation += 1

    clock = pygame.time.Clock()
    run = True
    while run and len(cars) > 0:
        clock.tick(60)

        act_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        if act_time == 3:
            act_time = 0
            for x, car in enumerate(cars):
                prize = car.distance_b - car.distance(856,774)
                ge[x].fitness += prize * 3
                car.distance_b = car.distance(856,774)
                car.numver_of_moves += 1

                output = nets[cars.index(car)].activate((car.speed,car.angle,car.pozycja[0],car.pozycja[1],
                                                         car.distance(856,774),car.distance(710,774),
                                                         car.distance(1000,774),car.distance(856,150),car.distance(710,150),
                                                         car.distance(1000,150),car.distance(856,850,),car.is_parked))

                i = output.index(max(output))


                if i == 0:
                    car.forward()
                elif i == 1:
                    car.backward()
                elif i == 2:
                    car.left()
                elif i ==3 :
                    car.right()
                elif i == 4:
                    car.stop()

                for parking_line in parking_lines:
                    screen.blit(parking_line.parkline_image, (parking_line.x, parking_line.y))
                    offset = (int(car.pozycja[0]- parking_line.x), int(car.pozycja[1] - parking_line.y))
                    result = parking_line.parkline_mask.overlap(car.body_mask, offset)
                    if result:
                        car.na_lini = True
                    else:
                        car.na_lini = False

                offset = (int(car.pozycja[0] - parking.x), int(car.pozycja[1] - parking.y))
                result = parking.parking_mask.overlap(car.body_mask, offset)
                if result:
                    car.na_parkingu = True
                else:
                    car.na_parkingu= False


                for obs in obstacles:
                    offset = (int(car.pozycja[0] - obs.x),int(car.pozycja[1] - obs.y))
                    result = obs.obstacle_mask.overlap(car.body_mask, offset)
                    if result:
                        car.to_delete = True
                        ge[x].fitness -= 300

                if car.na_parkingu and not car.na_lini:
                    ge[x].fitness += 100
                    car.is_parked = 1


                if car.numver_of_moves > 100:
                    car.to_delete = True
                    if car.is_parked == 0:
                        ge[x].fitness -= 500

                if car.to_delete:
                    nets.pop(cars.index(car))
                    ge.pop(cars.index(car))
                    cars.pop(cars.index(car))


        for car in cars:
            car.update()
        screen.blit(map, (0, 0))
        draw_window(screen, cars, obstacles)
        pygame.display.flip()
        clock.tick(0)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 10000)

    print('\nBest genome:\n{!s}'.format(winner))
