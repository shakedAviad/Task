import time
from threading import Thread, Lock
import threading
from fuzzywuzzy import fuzz


class ClusteringName:
    def __init__(self, file_name: str = None):
        self.EOF = False
        self.befor_procesing = list()

        self.after_procesing = list()
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

    def processing(self, lock_befoer,lock_after):

        print("function processing  ,{0}".format(threading.currentThread().getName()))
        while True:
            # print("function algorithm ,{0}".format(threading.currentThread().getName()))
            if self.EOF and len(self.befor_procesing) == 0: break
            if len(self.befor_procesing) == 0:continue
            else:
                with lock_befoer:
                    n = self.befor_procesing.pop()
                
                n = n.lower().replace(" ", "").replace("\n", "")
                with lock_after:
                    self.after_procesing.append(n)


    def algorithm(self,lock):

        print("function algorithm ,{0}".format(threading.currentThread().getName()))
        grs=list()
        while True:
            # print("function algorithm ,{0}".format(threading.currentThread().getName()))
            if self.EOF and len(self.after_procesing) == 0 and len(self.befor_procesing) == 0: break
            if len(self.after_procesing) == 0:continue
            else:
                with lock:
                    n = self.after_procesing.pop()
                for group in self.groups:
                    if all(fuzz.ratio(n,w)>80 for w in group):
                        group.append(n)
                        break
                else:
                    self.groups.append([n, ])


    def start(self):
        mutex_befor_procesing = Lock()
        reader = threading.Thread(target=self.input_file, args=[mutex_befor_procesing])
        #reader = threading.Thread(target=self.input_file(mutex_befor_procesing), args=[mutex_befor_procesing])


        mutex_after_procesing= Lock()
        handler = threading.Thread(target=self.processing, args=[mutex_befor_procesing,mutex_after_procesing])


        grouping =threading.Thread(target=self.algorithm, args=[mutex_after_procesing])

        #handler = threading.Thread(target=self.processing(mutex_befor_procesing, mutex_after_procesing), args=[mutex_befor_procesing, mutex_after_procesing])

        reader.start()
        handler.start()
        grouping.start()



        reader.join()
        handler.join()
        grouping.join()
        print("before :\n{0}\n num:{1}".format(self.befor_procesing, len(self.befor_procesing)))
        print("after :\n{0}\n num:{1}".format(self.after_procesing, len(self.after_procesing)))
        c=0
        for i in self.groups:
            c+=len(i)
        print("algorithm :\n{0}\nnum:{1}".format(self.groups,c))


if __name__ == '__main__':
    file_name1 = "../data/Task_15_names.txt"
    file_name2 = "../data/02 Task_clustering_1000names.txt"
    start = time.perf_counter()
    t = ClusteringName(file_name2)
    t.start()
    end = time.perf_counter()
    print(f"Program time {end - start}")
