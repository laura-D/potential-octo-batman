
from multiprocessing import Process, Queue, Lock

import json


ptopQueue = None
ptopLock = None

def printer(inPtopQueue, inPtopLock):
	ptopQueue = inPtopQueue
	ptopLock = inPtopLock
	

	while True:
		ptopLock.acquire()
	 	ptopQueue.put(downitem)
                print(ptopQueue.get())
		ptopLock.release()


 
