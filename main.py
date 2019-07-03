import tkinter as tk
from window import *
from player import *
from numpy import random

def main():
    root = tk.Tk()
    window = Window(master=root)
    window.mainloop()
    win = False
    pupulation_size = 100
    population = []
    generation = 1
    window.update_gen(generation)
    for i in range(population_size):
        chrom = Player.create_genome()
        population.append(Player(chrom))

    while not win:
        population = sorted(population, lambda x: x.fitness)
        if population[0].game_state == 'win':
            win = True
            break
        new_generation = []
        sample = int((10*population_size)/100)
        new_generation.extend(population[:sample])
        for i in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)
        population = new_generation
        window.update_matrix(population[0].game)
        window.update_labels()
        output_string = 'Generation: %-4s Fitness: %-8s' % (generation, population[0].fitness)
        print(output_string)
        generation += 1
        window.update_gen(generation)

if __name__ == '__main__':
    main()
