import numpy as np
import genetic_algorithm
#genetic_algorithm.main()
pop_list = np.load("encoded_solution.npy")

genetic_algorithm.rank(pop_list)
opt_solution = pop_list[0]
opt_value = genetic_algorithm.fitness_cal(opt_solution)
print("genetic_alg opt value :", opt_value)

with open("att48.opt.tour") as f:
    lines = f.readlines()
    start = lines.index("TOUR_SECTION\n")
    lines2 = [int(i) -1 for i in lines[start+1:start+1+genetic_algorithm.PROBLEM_SIZE]]

true_opt = np.array(lines2)
#print(true_opt)
true_opt_value = genetic_algorithm.fitness_cal(true_opt)
print("true opt value : ", true_opt_value)