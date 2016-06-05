from __future__ import division
from random import randint, random, uniform
import sys


def run_random_forest(train, test, parameter_list={"n_estimators":10, "min_samples_split":2, "min_samples_leaf":1, "max_leaf_nodes":None, "max_features":1}):

    train_indep = [t[:-1] for t in train]
    train_dep = [t[-1] for t in train]

    test_indep = [t[:-1] for t in test]
    test_dep = [t[-1] for t in test]

    # Import the random forest package
    from sklearn.ensemble import RandomForestClassifier

    # Create the random forest object which will include all the parameters
    # for the fit
    forest = RandomForestClassifier(n_estimators = parameter_list[0],
                                    min_samples_split = parameter_list[1],
                                    min_samples_leaf = parameter_list[2],
                                    max_leaf_nodes = parameter_list[3],
                                    max_features = parameter_list[4]
                                    )

    # print parameter_list
    # Fit the training data to the Survived labels and create the decision trees
    forest = forest.fit(train_indep, train_dep)

    # Take the same decision trees and run it on the test data
    output = forest.predict(test_indep)

    # performance scores
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(test_dep, output)

    from sklearn.metrics import precision_score
    precision = precision_score(test_dep, output)

    from sklearn.metrics import f1_score
    f_score = f1_score(test_dep, output)

    return f_score

def generate_population(population_size, parameter_ranges):
    population = []
    for _ in xrange(population_size):
        temp = []
        temp.append(randint(parameter_ranges["n_estimators"][0], parameter_ranges["n_estimators"][1]))
        temp.append(randint(parameter_ranges["min_samples_split"][0], parameter_ranges["min_samples_split"][1]))
        temp.append(randint(parameter_ranges["min_samples_leaf"][0], parameter_ranges["min_samples_leaf"][1]))
        temp.append(randint(parameter_ranges["max_leaf_nodes"][0], parameter_ranges["max_leaf_nodes"][1]))
        temp.append(uniform(parameter_ranges["max_feature"][0], parameter_ranges["max_feature"][1]))
        population.append(temp)
    assert(len(population) == population_size), "Something wrong in the loop"
    return population

def three_others(individuals, one):
    seen = [one]
    def other():
        while True:
            random_selection = randint(0, len(individuals) - 1)
            if individuals[random_selection] not in seen:
                seen.append(individuals[random_selection])
                break
        return individuals[random_selection]
    return other(), other(), other()

def trim(mutated, low, up):
    return max(low, min(mutated, up))

def extrapolate(parameter_ranges, population, one, f, cf):
    ranges = []
    keys = ["n_estimators", "min_samples_split", "min_samples_leaf","max_leaf_nodes", "max_feature"]
    for key in keys:
        ranges.append([parameter_ranges[key][0], parameter_ranges[key][1]])

    from random import randint
    two, three, four = three_others(population, one)
    solution = []
    for d, range in enumerate(ranges):
        x, y, z = two[d], three[d], four[d]
        if random() < cf or randint(0, len(population[0])) == d:
            mut = trim(x + f * (y - z), range[0], range[1])
            if keys[d] == "max_feature":
                solution.append(mut)
            else: solution.append(int(mut))
        else:
            solution.append(one[d])

    return solution

def evaluate_population(population, train, validation):
    scores = []
    for pop in population:
        scores.append(run_random_forest(train, validation, pop))
    assert(len(scores) == len(population)), "Something is wrong"
    return scores

def acceptance(pop_score, mutant_score):
    if pop_score > mutant_score: return False
    else: return True

def stopping_criteria(change_in_population, lives):
    if change_in_population is False:
        lives -= 1
        print "Lost life"
        if lives == 0: return True, lives
        else: return False, lives
    else: return False, lives




def run_de_4_rf(train, validation, de_parameters):

    # print "> ", de_parameters
    lives = de_parameters["lives"]




    parameter_ranges = {"n_estimators":[50,150],
                        "min_samples_split":[2,20],
                        "min_samples_leaf":[2,20],
                        "max_leaf_nodes":[2,50],
                        "max_feature":[0.02,1]}


    to_stop = False
    gen = 0

    population = generate_population(de_parameters["pop_size"], parameter_ranges)
    scores = evaluate_population(population, train, validation)

    while gen < de_parameters["max_generations"] and to_stop is False:
        # print [round(s, 3) for s in scores]

        print "# ",
        sys.stdout.flush()
        change_in_population = False
        for pop_no, pop in enumerate(population):
            mutant = extrapolate(parameter_ranges, population, pop, de_parameters["F"], de_parameters["CF"])
            mutant_score = run_random_forest(train, validation, mutant)
            mutant_accept = acceptance(scores[pop_no], mutant_score)
            if mutant_accept is True:
                scores[pop_no] = mutant_score
                population[pop_no] = mutant
                change_in_population = True

        to_stop, lives = stopping_criteria(change_in_population, lives)
        gen += 1

    # find index with highest score
    max_index = scores.index(max(scores))
    parameter = population[max_index]
    print
    return parameter

