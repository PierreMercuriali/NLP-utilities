"""
    Language evolution via a genetic algorithm
    
    
"""
import random 
import matplotlib.pyplot as plt
def mutateWord(w):
    res = list(w)
    res[random.randint(0,len(w)-1)] = random.choice("qwertyuioplkjhgfdsazxcvbnm")
    return "".join(res)

def normalize(scores):
    m = min(scores)
    s = [score+m for score in scores]
    S = sum(s)
    return [float(score)/(S) for score in s]

def biggest(w1, w2):
    if len(w1) > len(w2):
        return w1
    else:
        return w2

def reproduce(w1, w2):
    res = []
    b = biggest(w1, w2)
    for i in range(min(len(w1), len(w2))):
        res.append(random.choice([w1[i], w2[i]]))
    for i in b[min(len(w1), len(w2)):]:
        res.append(random.choice([i,""]))
    return "".join(res)

def fitness(w):
    consonants = "qwrtplkjhgfdszxcvbnm"
    vowels = "eyuioa"
    pause = " "
    score = 0
    for i in range(len(w)-1):
        if w[i] in consonants and w[i+1] in vowels:
            score+=10
        if w[i] in consonants and w[i+1] in consonants:
            score+=1
        if w[i] in vowels and w[i+1] in consonants:
            score+=10
        if w[i] in vowels and w[i+1] in vowels:
            score+=2
        if w[i] in vowels and w[i+1] in pause:
            score+=3
    return float(score)/len(w)

def init(n, mi, ma):
    res = []
    for i in range(n):
        res.append("".join([random.choice("qwertyuioplkjhgfdsazxcvbnm") for i in range(random.randint(mi,ma))]))
    return res

def order(pop):
    return sorted(pop, key=fitness, reverse=True)

def selection(pop):
    res = []
    for p in pop[:int(len(pop)/2)]:
        res.append(p)
        res.append(p)
        res.append(p)
    return res[:len(pop)]
#    return random.choices(pop, weights=[fitness(e) for e in pop], k=len(pop))

def crossover(pop):
    res = []   
    for i in range(len(pop)-1):
        res.append(reproduce(pop[i], pop[i+1]))
    res.append(reproduce(pop[0], pop[-1]))
    return res

def mutate(pop, amount):
    res = []
    for e in pop:
        r = e
        for i in range(amount):
            r = mutateWord(r)
        res.append(r)
    return res
    
NUMBER = 20
GENERATIONS = 200
population = init(NUMBER, 3, 10)
mean_fitness = [[] for i in range(NUMBER)]
mean_overall_fitness = []
for i in range(GENERATIONS):
    population = order(population)
    for i in range(NUMBER):
        mean_fitness[i].append(fitness(population[i]))
    mean_overall_fitness.append(sum([fitness(e) for e in population])/NUMBER)
    population = selection(population)
    population = order(population)
    population = crossover(population)
    population = mutate(population, 1)
    #print(population)
print(population)
for i in range(NUMBER):
    plt.plot(mean_fitness[i], color = (float(i)/NUMBER, 0,0), linewidth = .2)
plt.plot(mean_overall_fitness, color = (0,0,1), linewidth = .5)
plt.title("Mean fitness over generations")
plt.show()

