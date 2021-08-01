import time
from fuzzywuzzy import fuzz

target_group = list()
real_groups = dict()


def grouping_names(file_name: str = None, number_of_groups: int = 0):
    global real_groups, target_group
    with open(file_name, "r")as file:
        for name in file:
            target = simplify(name)
            algorithm(target)
            real_groups[target] = name
    print_groups(number_of_groups)


def simplify(name: str = None):
    return name.lower().replace(".", "").replace(",", "").replace("\n", "")


def algorithm(target):
    global target_group
    for group in target_group:
        if condition(group, target):
            group.append(target)
            break
    else:
        target_group.append([target, ])


def condition(group, target) -> bool:
    if all(ratio(target, full_name) or ratio(target, full_name.split(" ")[0]) for full_name in group):
        return True
    return False


def ratio(target, name):
    # return (fuzz.ratio(target, new) > c or
    #         fuzz.partial_ratio(target, new) > c or
    #         fuzz.token_sort_ratio(target, new) > c or
    #         fuzz.token_set_ratio(target, new) > c)
    return fuzz.ratio(target,name)>75 or fuzz.partial_ratio(target, name) >90

def print_groups(number_of_groups: int = 0):
    global target_group, real_groups

    solution = list()
    target_group.sort(key=lambda n: -len(n))

    for group in target_group:
        li = list()
        for target in group:
            li.append(real_groups.get(target))
        solution.append(li)
        number_of_groups -= 1
        if number_of_groups == 0: break
    st=str()
    for i,s in enumerate(solution):
        st+=f"group {i+1} :\n * number : {len(s)} \n * list:{s}\n"
    print(st)
if __name__ == '__main__':
    file_name1 = "../data/Task_15_names.txt"
    file_name2 = "../data/02 Task_clustering_1000names.txt"
    start = time.perf_counter()
    grouping_names(file_name1, 3)
    end = time.perf_counter()
    print(f"Program time with straight  {end - start}")
