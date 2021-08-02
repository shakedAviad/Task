import time
from fuzzywuzzy import fuzz

target_group = list()
real_groups = dict()


def grouping_names(file_name: str = None, number_of_groups: int = 0) -> list:
    """
    This is the primary function,goes through every name in the file
    and sends the name  to the  algorithm function(explanation below)
    finally prints the names that are repeated the most times on request

    Issues:If you want a very high level of accuracy it may take time

    :param file_name:
    :param number_of_groups:
    :return:
    """
    global real_groups, target_group
    with open(file_name, "r")as file:
        for name in file:
            target = simplify(name)
            algorithm(target)
            real_groups[target] = name
    print_groups(number_of_groups)


def simplify(name: str = None) -> str:
    """
    Simplifies a name so that there is a high match but without damaging the name's standards
    :param name:
    :return:
    """
    return name.lower().replace(".", "").replace(",", "").replace("\n", "")


def algorithm(target: str = None) -> None:
    """
    This function uses an external directory
    see:https://www.datacamp.com/community/tutorials/fuzzy-string-python
    each name(target) is matched to the other existing groups
    if a relatively high match is found then added to the appropriate list
    else a new group with the current name opens
    :param target:
    :return:
    """
    global target_group
    for group in target_group:
        if condition(group, target):
            group.append(target)
            break
    else:
        target_group.append([target, ])


def condition(group, target) -> bool:
    """
    For each group and target name
    check whether the destination belongs approximately to each member of the group
    :param group:
    :param target:
    :return:
    """
    if all(ratio(target, full_name) or ratio(target, full_name.split(" ")[0]) for full_name in group):
        return True
    return False


def ratio(target, name) -> bool:
    """
    Match check for a name from the group to a target name
    :param target:
    :param name:
    :return:
    """
    # return (fuzz.ratio(target, new) > c or
    #         fuzz.partial_ratio(target, new) > c or
    #         fuzz.token_sort_ratio(target, new) > c or
    #         fuzz.token_set_ratio(target, new) > c)
    return fuzz.ratio(target, name) > 75 or fuzz.partial_ratio(target, name) > 90


def print_groups(number_of_groups: int = 0) -> None:
    """
    This function pretty prints the names that have been repeated the most times
    by required quantity
    :param number_of_groups:
    :return:
    """
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

    st = str()
    for i, s in enumerate(solution):
        st += f"group {i + 1} :\n * number : {len(s)} \n * list:{s}\n"
    print(st)


if __name__ == '__main__':
    file_name1 = "../data/Task_15_names.txt"
    file_name2 = "../data/02 Task_clustering_1000names.txt"

    print(f"Short File 15 names ")
    start = time.perf_counter()
    grouping_names(file_name1, 3)
    end = time.perf_counter()
    print(f"Time of 15 names  {end - start}")

    print(f"Long File 1000 names ")
    start = time.perf_counter()
    grouping_names(file_name2, 3)
    end = time.perf_counter()
    print(f"Time of Long file 1000 names  {end - start}")