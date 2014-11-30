#!/usr/bin/env python
import socket              
import time
import threading

            

def session(conn, addr):
  print 'Session:request goted'
  while True:
    print 'Got connection from', addr
    conn.send('Please wait...')

    while True:
      print 'w'
      msg = conn.recv(1024)
      if not msg:
        s.close()
        print "No message"
        break
      elif msg == "close":
        print ("Connection with %s was closed by the client." % (addr[0]))
      else:
        print "%s: %s" % (addr[0], msg)
        conn.send("1")

if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  host = socket.gethostname()
  s.bind(('localhost', 50999))       
  s.listen(5)
  adress = []

  while True:
    event = threading.Event()
    print 'Panding'
    conn, addr = s.accept()
    print 'Accepted'
    if addr not in adress:
      adress.append(addr)
      print addr
      server_thread = threading.Thread(target=session, args=(conn,addr))
      server_thread.start()
      print 'thread started'

      #event.set()

      #server_thread.join()
      print 'joined'

  s.close()