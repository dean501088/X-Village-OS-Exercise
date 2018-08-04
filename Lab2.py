import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0
path="/Users/deanchu/Documents/X-Village/OS_LAB/testdata"

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue
 
    #for subpath in os.listdir(path):
     #   if os.path.isdir(os.path.join(path, subpath)):
      #      queue.put(os.path.join(path, subpath))
    queue.put(top_dir)
    files = os.listdir(top_dir)
    for f in files:
        filepath = os.path.join(top_dir, f)
        if os.path.isdir(filepath):
            producer(filepath, queue_buffer)

     
            
        


def consumer(queue_buffer):
    global file_count
    # search file in directory
    a = queue.get()
    for i in os.listdir(a):
        b = os.path.join(a, i)
        if os.path.isfile(b):
            lock.acquire()
            file_count +=1
            print(file_count)
            lock.release()
        


def main():
    producer_thread = threading.Thread(target = producer, args = (path, queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()