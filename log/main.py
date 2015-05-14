from multiprocessing import Process, Queue, Lock
from receiver import receiver
from printer import printer
from writer import writer

def run_loop():
        wtopQueue = Queue()
	wtopLock = Lock()	
	ptopQueue = Queue()
	ptopLock = Lock()

	receiverPs = Process(target = receiver, args = ())
        writerPs = Process(target = writer, args = (wtopQueue, wtopLock))
	printerPs = Process(target = printer, args = (ptopQueue, ptopLock))
	
	

	writerPs.start()
	printerPs.start()
	receiverPs.start()
	

	receiverPs.join()
	printerPs.join()
	writerPs.join()
	

if __name__ == '__main__':
        global downitem
	run_loop()
