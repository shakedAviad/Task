import time
from threading import Thread, Lock
import threading
from fuzzywuzzy import fuzz
from multiprocessing import Process


class ClusteringName:
    def __init__(self, file_name: str = None):
        self.EOF = False
        self.befor_procesing = list()

        self.groups = list()
        self.file_name = file_name

    def input_file(self, lock):

        print("function input file ,{0}".format(threading.currentThread().getName()))
        with open(self.file_name, "r") as file:
            for name in file:
                # print("function input file ,{0}".format(threading.currentThread().getName()))
                with lock:
                    self.befor_procesing.append(name)

        self.EOF = True

    def processing(self, lock):

        print("function processing  ,{0}".format(threading.currentThread().getName()))
        while True:
            # print("function algorithm ,{0}".format(threading.currentThread().getName()))
            if self.EOF and len(self.befor_procesing) == 0: break
            if len(self.befor_procesing) == 0:continue
            else:
                with lock:
                    n = self.befor_procesing.pop()

                self.algorithm(n)

    def algorithm(self, n):
        n = n.lower().replace(" ", "").replace("\n", "")
        for group in self.groups:
            if all(fuzz.ratio(n, w) > 80 for w in group):
                group.append(n)
                break
        else:
            self.groups.append([n, ])

    def start(self):
        mutex = Lock()
        reader = threading.Thread(target=self.input_file, args=[mutex])
        # reader = threading.Thread(target=self.input_file(mutex_befor_procesing), args=[mutex_befor_procesing])
        # handler= Process(target=self.processing, args=[mutex])
        handler = threading.Thread(target=self.processing, args=[mutex])
        # handler1 = threading.Thread(target=self.processing, args=[mutex_befor_procesing,mutex_after_procesing])
        # handler = threading.Thread(target=self.processing(mutex_befor_procesing, mutex_after_procesing),
        #                            args=[mutex_befor_procesing, mutex_after_procesing])

        reader.start()

        handler.start()
        # handler1.start()

        reader.join()

        handler.join()
        # handler1.join()
        print("before :\n{0}\n num:{1}".format(self.befor_procesing, len(self.befor_procesing)))
        c = 0
        for i in self.groups:
            c += len(i)
        print("algorithm :\n{0}\nnum:{1}".format(self.groups, c))


if __name__ == '__main__':
    file_name1 = "../data/Task_15_names.txt"
    file_name2 = "../data/02 Task_clustering_1000names.txt"
    start = time.perf_counter()
    t = ClusteringName(file_name2)
    t.start()
    end = time.perf_counter()
    print(f"Program time {end - start}")
