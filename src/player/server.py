from stupidArtnet import StupidArtnetServer
from player import VlcPlayer
import os,time

from dotenv import load_dotenv
config = load_dotenv(".env") 

UDP_IP=os.environ['UDP_IP']
UDP_PORT=os.environ['UDP_PORT']
UNIVERSE=int(os.environ['UNIVERSE'])
SUBNET=int(os.environ['SUBNET'])
NET=int(os.environ['NET'])-1

DEBUG=True

server = StupidArtnetServer()

universe_id = server.register_listener(
    UNIVERSE, SUBNET, NET, False)

print(server)
old_state = {}
player = VlcPlayer()

while True:
    buffer = bytes(server.get_buffer(universe_id))
    if len(buffer) == 512:
        new_state = { 'media_id': ((buffer[NET] << 8) & 0xff00) + buffer[NET+1], 'command': buffer[NET+2], 'extra': ((buffer[NET+3] << 8) & 0xff00) + buffer[NET+5] }
        print(new_state)
        if (not old_state == new_state):
            player.update(**new_state)
            old_state = new_state
    time.sleep(0.5)
