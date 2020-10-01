import numpy as np
#problem : saleman att48


POPULATION = 14
MUTATION_PROBABILITY = 0.05
SELECTED_PARENT_SIZE = 5
#np.random.seed(14)



#encoding solution: permutation
with open("att48.tsp") as input_file:
    all_things = input_file.readlines()
    start = all_things.index("NODE_COORD_SECTION\n")
    all_things= all_things[start+1:]
    location = list() # decoding look-up list
    PROBLEM_SIZE = len(all_things)
    for i in range(len(all_things)):
        loc = (all_things[i].split(' '))
        location.append((int(loc[1]), int(loc[2])))

distance = np.array(list()) # distance matrix
for i in range(len(location)):
    dis = list()
    for j in range(len(location)):
        dis.append(np.sqrt(pow(location[i][0] - location[j][0],2) + pow(location[i][1] - location[j][1],2)  ))
    dis = np.array(dis)
    distance = np.append(distance,dis)

distance.resize(PROBLEM_SIZE,PROBLEM_SIZE)


#ranking
def rank(pop_list):
    lis = list()
    for i in range(pop_list.shape[0]):
        term = list()
        term.append(i)
        term.append(fitness_cal(pop_list[i]))
        lis.append(term)

    lis.sort(key = lambda x:x[1])

    return lis
#pop fitness
def fitness_pop(pop_list):
    sum = 0
    for i in range(POPULATION):
        sum += fitness_cal(pop_list[i])
    return sum

#indivitual fitness cal
def fitness_cal(x):

    sum = 0
    for i in range(len(x[1:])):

        sum = sum+ distance[int(x[i])][int(x[i-1])]
    sum = sum + distance[int(x[len(x) - 1]) ][int(x[0])]
    return sum


#initialize func
def ini(population):
    list_pop = np.array(list())
    for i in range(population):
        list_pop = np.append(list_pop,np.random.permutation(PROBLEM_SIZE))
    list_pop.resize(population,PROBLEM_SIZE)
    return list_pop


#parent_selection : roulette wheel:
def parent_select(pop_list):
    prob = np.array(list())
    sum = 0
    for i in range(POPULATION):
        sum += fitness_cal(pop_list[i])
    for i in range(POPULATION):
        fitness =  fitness_cal(pop_list[i] )/sum
        prob = np.append(prob,fitness)
    par1 = np.random.choice(POPULATION,p = prob)
    par1 = pop_list[par1]
    par2 = np.random.choice(POPULATION, p =prob)
    par2 = pop_list[par2]
    parents = np.append(par1, par2)
    parents.resize(2,PROBLEM_SIZE)
    return parents
#mutation :
def mutation(offspring):
    for i in range(offspring.shape[0]):
        out = np.random.choice(a= [1,0], p=[ MUTATION_PROBABILITY, 1-MUTATION_PROBABILITY])
        if(out == 1):
            out = np.random.choice(a= offspring.shape[0])

            term = offspring[i]
            offspring[i] = offspring[out]
            offspring[out] = term
    return offspring

#cross over
def crossover(parents):
    shared = np.array(list())
    par1 = parents[0]
    par2 = parents[1]
    offspring = np.array(list())
    leng = parents.shape[1]

    start = np.random.choice(leng)
    end = np.random.choice(leng)
    if(start> end):
        t = end
        end = start
        start= end

    shared = par1[start:end+1]

    term = list()
    total = [i for i in par2 if i not in shared]
    offspring = np.append(offspring, total[0:start])
    offspring = np.append(offspring,shared)
    offspring = np.append(offspring, total[start:])

    return offspring

#main
def main():
    STOP_CONDITION = 15000

    end = 0
    pop_list = ini(POPULATION)
    while(end <= STOP_CONDITION):
        total_fitness= fitness_pop(pop_list)

        list_offsprint = np.array(list())
        print(total_fitness)
        for i in range(SELECTED_PARENT_SIZE):
            parents = parent_select(pop_list)
            offspring = crossover(parents)
            offspring = mutation(offspring)


            list_offsprint = np.append(list_offsprint, offspring)

        list_offsprint.resize(SELECTED_PARENT_SIZE, PROBLEM_SIZE)

        pop_list = np.append(pop_list,list_offsprint,axis = 0)
        pop_list.resize()
        ranking_lis = rank(pop_list)
        pop_list2 = np.array(list())
        for i in range(POPULATION):
            pop_list2 = np.append(pop_list2, pop_list[ranking_lis[i][0] ])
        pop_list2.resize(POPULATION,PROBLEM_SIZE)
        pop_list = pop_list2
        end+=1

    print(pop_list[0])
    print(fitness_pop(pop_list))
    np.save("encoded_solution.npy",pop_list)

