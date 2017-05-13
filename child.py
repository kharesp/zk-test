from kazoo.client import KazooClient
from kazoo.recipe.barrier import Barrier
import logging, uuid, socket, time, datetime

def connection_state_listener(state):
	print("connection state:%s"%state)

def main():
	name="child_"+socket.getfqdn()+"_"+uuid.uuid4().hex
	logging.basicConfig()
	zk=KazooClient(hosts='129.59.107.59:2181')
	zk.add_listener(connection_state_listener)
	zk.start()

	zk.ensure_path("/test/group-membership")
	zk.ensure_path("/test/barriers/barrier")
	barrier=Barrier(client=zk,path="/test/barriers/barrier")
	zk.create("/test/group-membership/"+name,ephemeral=True)
	while True:
		print("Waiting on Barrier")
		barrier.wait()	
		print("Barrier was opened")
		print("child:%s \t ts:%s"%(name,
			datetime.datetime.now().time()))
		time.sleep(1)		

if __name__=='__main__':
	main()
