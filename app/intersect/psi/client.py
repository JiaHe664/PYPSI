from .pair import make_pair, Address
from .psi.client import Client
import logging

def start_client(local_address: str, peer_address: str, data_path: str):
    peer_host, peer_port_str = peer_address.split(":", 2)
    peer_port = int(peer_port_str)
    
    local_host, local_port_str = local_address.split(":", 2)
    local_port = int(local_port_str)

    local_address = Address(local_host, local_port)
    peer_address = Address(peer_host, peer_port)
 
    with open(data_path, mode="r", encoding="utf-8") as f:
        data = [line.rstrip().encode("utf-8") for line in f]

    with make_pair(local_address, peer_address) as pair:
        client = Client(pair, data, data_path)

        logging.info("start prepare")
        client.prepare()  # prepare stage
        logging.info("finish prepare")

        logging.info("start intersection")
        res = client.intersect()  # intersect stage, res is the intersection
        logging.info("finish intersection")

        res_strs = sorted([val.decode("utf-8") for val in res])

        pair.barrier()
        
        return res_strs
