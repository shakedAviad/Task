import time
import threading
from threading import Lock
from fuzzywuzzy import fuzz


class ClusteringName:
    def __init__(self, file_name: str = None,num_of_group:int =3):
        self.EOF = False
        self.before_processing = list()
        self.groups = list()
        self.file_name = file_name
        self.num_of_group = num_of_group

    def grouping(self):
        with open(self.file_name, "r") as file:
            for name in file:
                self.algorithm(name)
        self.groups.sort(key=lambda n:-len(n))
        return self.get_biggest_groups()
    def get_biggest_groups(self):
        li=list()
        di=dict()
        for i in range(self.num_of_group):
            li.append(self.groups[i])
            di[f"group  {i+1}"]=(len(li[i]),li[i])
        return di
    def input_file(self, lock):
        with open(self.file_name, "r") as file:
            for name in file:
                with lock:
                    self.before_processing.append(name)

        self.EOF = True

    def processing(self, lock):
        while True:
            if self.EOF and len(self.before_processing) == 0: break
            if len(self.before_processing) == 0:
                continue
            else:
                with lock:
                    n = self.before_processing.pop()
                self.algorithm(n)

    def algorithm(self, n):
        n = n.lower().replace(" ", "").replace("\n", "").replace(".", "")
        for group in self.groups:
            if all(fuzz.ratio(n, w) > 80 for w in group):
                group.append(n)
                break
        else:
            self.groups.append([n, ])

    def start(self):
        mutex = Lock()

        reader = threading.Thread(target=self.input_file, args=[mutex])
        handler = threading.Thread(target=self.processing, args=[mutex])

        reader.start()
        handler.start()

        reader.join()
        handler.join()


if __name__ == '__main__':
    file_name1 = "../data/Task_15_names.txt"
    file_name2 = "../data/02 Task_clustering_1000names.txt"
    file_name3 = "../data/myTest.txt"
    t = ClusteringName(file_name3)

    start = time.perf_counter()
    # t.start()
    end = time.perf_counter()

    print(f"Program time with parallel {end - start}")
    t = ClusteringName(file_name1)
    start = time.perf_counter()
    print(t.grouping())

    end = time.perf_counter()
    print(f"Program time with straight  {end - start}")
