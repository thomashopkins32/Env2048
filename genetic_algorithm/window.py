import tkinter as tk
from player import *
from constants import *
import logic

class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_window()

        self.score_raw = 0
        self.matrix = logic.new_game()
        self.update_labels()
        self.simulate()

    def init_window(self):
        self.master.geometry(GEOMETRY)
        self.master.title('2048')
        #self.master.bind('<Key>', self.key_pressed)
        self.header = tk.Frame(self.master, bg='#92877d')
        self.create_header_widgets(self.header)

        self.content = tk.Frame(self.master, bg='#92877d')
        self.create_content_grid(self.content)

        layout = [[self.header], [self.content]]
        col_weights = [1]
        row_weights = [1, 99]
        self.create_grid(self.master, layout=layout, r_weights=row_weights, c_weights=col_weights)

    def create_grid(self, container, layout=[], r_weights=[], c_weights=[]):
        if layout == [] or r_weights == [] or c_weights == []:
            print('Error creating grid with empty layout...')
            quit()
        for i in range(len(layout[0])):
            container.columnconfigure(i, weight=c_weights[i])
        for i in range(len(layout)):
            container.rowconfigure(i, weight=r_weights[i])
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                layout[i][j].grid(row=i, column=j, sticky='nsew')

    def simulate(self):
        win = False
        population = []
        generation = 1
        self.update_gen(generation)
        for i in range(POPULATION_SIZE):
            chrom = Player.create_genome()
            population.append(Player(chrom))
        while not win:
            extend = False
            population = sorted(population, key=lambda x: x.fitness, reverse=True)
            self.update_matrix(population[0].game)
            self.score_raw = population[0].fitness
            self.update_labels()
            output_string = 'Generation: %-4s Fitness: %-8s' % (generation, population[0].fitness)
            print(output_string)
            if population[0].outcome == 'win':
                win = True
                break
            if generation % GEN_OFFSET == 0:
                extend = True
                print('Extending moveset by 50...')
            new_generation = []
            sample = int((ELITE*POPULATION_SIZE)/100)
            for i in population[:sample+1]:
                if extend:
                    i.extend()
                new_generation.append(i)
            sample = int(((100-ELITE)*POPULATION_SIZE)/100)
            for i in range(sample):
                parent1 = R_GLOBAL.choice(population[:int(POPULATION_SIZE/2)])
                parent2 = R_GLOBAL.choice(population[:int(POPULATION_SIZE/2)])
                child = parent1.mate(parent2)
                if extend:
                    child.extend()
                new_generation.append(child)
            population = new_generation
            generation += 1
            self.update_gen(generation)

    def create_header_widgets(self, header):
        self.score = tk.Label(header, text='Score: ', anchor='w', font=('Helvetica', 18), bg='#92877d')
        self.gen = tk.Label(header, text='Generation: ', anchor='w', font=('Helvetica', 18), bg='#92877d')
        self.score.pack()
        self.gen.pack()

    def create_content_grid(self, content):
        self.labels = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(tk.Label(content, bg='#92877d', text='', font=('Helvetica', 24), borderwidth=2, relief='raised' ))
            self.labels.append(tmp)
        col_weights = [25, 25, 25, 25]
        row_weights = [25, 25, 25 ,25]
        self.create_grid(content, layout=self.labels, r_weights=row_weights, c_weights=col_weights)

    def update_labels(self):
        for i in range(4):
            for j in range(4):
                new_value = self.matrix[i][j]
                if new_value == 0:
                    self.labels[i][j].configure(text='', bg='#9e948a')
                else:
                    self.labels[i][j].configure(text=str(new_value), bg=COLORS[new_value])
        score_text = 'Score: ' + str(self.score_raw)
        self.score.configure(text=score_text)
        self.update_idletasks()

    def update_gen(self, gen):
        gen_text = 'Generation: ' + str(gen)
        self.gen.configure(text=gen_text)
        self.update_idletasks()

    def update_matrix(self, new_matrix):
        self.matrix = new_matrix
