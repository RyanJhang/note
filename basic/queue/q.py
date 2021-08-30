
import queue


q = queue.Queue(1)
q.put('a')
if q.full():
    q.get()
q.put('b')
print(q.qsize())

# --------------------------------------------
while True:
    frame = "get"
    if not q.empty():
        try:
            q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
            pass
        q.put(frame)