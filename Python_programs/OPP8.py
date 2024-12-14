from multiprocessing import Process

def task():
    print("task is running")

thread = Process(target=task)
thread.start()
thread.join()