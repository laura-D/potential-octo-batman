
from bson.objectid import ObjectId
from multiprocessing import Queue, Lock

wtopQueue = None
wtopLock = None

def writer(inWtopQueue, inWtopLock):
	wtopQueue = inWtopQueue
	wtopLock = inWtopLock
	


	while True:
		
		wtopLock.acquire()
	 	wtopQueue.put(downitem)
	        f=file("hello.txt","w+")
                li=wtopQueue.get()
                f.writelines(li)
                f.close()	
		wtopLock.release()
  


