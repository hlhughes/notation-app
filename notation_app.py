from multiprocessing import Process

import record
import realTime

if __name__ == '__main__':

    p1 = Process(target=record.record_loop)
    p1.start()
    print("p1, record started")
    
    p2 = Process(target=realTime.realTimeABC)
    p2.start()
    print("p2, realTime started")

    p1.join()
    p2.join()
    print("processes done")