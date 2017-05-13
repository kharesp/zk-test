from kazoo.client import KazooClient 
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.recipe.barrier import Barrier
from kazoo.protocol.states import EventType
import logging,time

def connection_state_listener(state):
  print("connection state:%s"%state)

def membership_watch(children,event):
  if event and event.type==EventType.CHILD:
    print("Number of members under /test/group-membership has changed to:%s\nCurrent members:%s\n"%(len(children),children))
    if(len(children)==3):
      global barrier
      barrier.remove()

def main():
  logging.basicConfig()
  zk=KazooClient(hosts='129.59.107.59:2181')
  zk.add_listener(connection_state_listener)
  zk.start()
  zk.ensure_path("/test/group-membership")
  zk.ensure_path("/test/barriers/barrier")
  global barrier
  barrier=Barrier(client=zk,path="/test/barriers/barrier")
  ChildrenWatch(client=zk,path="/test/group-membership",func=membership_watch,send_event=True)
  while True:
    time.sleep(20)

if __name__=='__main__':
  main()
