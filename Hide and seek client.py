import turtle
import socket
import threading
import time
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
CONNECTION = ('192.168.1.53',5000)
SOCK.sendto('0,0,0'.encode(),CONNECTION)
class Player:
  def __init__(s,x,y,d):
    s.d = d
    s.x = x
    s.y = y
    s.turtle = turtle.Turtle()
    s.turtle.pu()
    
  def forward(s,*kwargs):
    s.turtle.fd(5)
    s.x,s.y = s.turtle.pos()
    s.x,s.y = s.turtle.pos()    
    s.x = round(s.x)
    s.y = round(s.y)
    
  def left(s):
    s.d+=10
  def right(s):
    s.d-=10
  def show(s):
    s.turtle.goto(s.x,s.y)
    s.turtle.seth(s.d)
  def update(s,x,y,d):
    s.x = x
    s.y = y
    s.d = d


def send(player):
    global SOCK
    msg = ''.join([str(player.x),',',str(player.y),',',str(player.d)])
    SOCK.sendto(msg.encode(),CONNECTION)

def recieve():
    global SOCK
    global infFromServ
    while True:
      d = SOCK.recv(1024)
      data = d.decode()
      ip,inf = data.split(' ')
      infFromServ[ip]=inf
      print(infFromServ)

def serverUpdate(player):
  global TIME
  if time.time()-TIME > .1:
    send(player)
    TIME = time.time()
class RemotePlayer:
  addressList = []
  def __init__(s,IP,vals):
    s.vals = vals.split(',')
    s.x = int(s.vals[0])
    s.y = int(s.vals[1])
    s.d = int(s.vals[2])
    s.address = IP
    s.turtle = turtle.Turtle()
    s.turtle.pu()
    s.turtle.goto(s.x,s.y)
    RemotePlayer.addressList.append(IP)
  def update(s,vals):
    s.vals = vals.split(',')
    s.x = int(s.vals[0])
    s.y = int(s.vals[1])
    s.d = int(s.vals[2])
    s.show()
  def show(s):
    s.turtle.goto(s.x,s.y)
    s.turtle.seth(s.d)
def findNewPlayers():
  MYIP = socket.gethostbyname(socket.gethostname())
  for i in infFromServ:
    if i == MYIP:
      pass
    elif i not in RemotePlayer.addressList:
      Remoteplayers.append(RemotePlayer(i,infFromServ[i]))
    else:
      print('Updating')
      Remoteplayers[RemotePlayer.addressList.index(i)].update(infFromServ[i])
    

#infFromServ = {ip: 'x,y,d'}
infFromServ = {}
Remoteplayers = []
TIME = 0
player = Player(0,0,0)
recievingThread = threading.Thread(target = recieve)
recievingThread.start()
import random

window = turtle.Screen()
window.listen()
window.onkeypress(player.forward,'w')
window.onkeypress(player.left,"a")
window.onkeypress(player.right,"d")
while True:
  player.show()
  serverUpdate(player)
  findNewPlayers()
  
