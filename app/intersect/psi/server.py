import logging

from psi.pair import Address, make_pair
from .psi.server import Server


def start_server(local_address: str, peer_address: str, data_path: str):
    peer_host, peer_port_str = peer_address.split(":", 2)
    peer_port = int(peer_port_str)
    
    local_host, local_port_str = local_address.split(":", 2)
    local_port = int(local_port_str)

    local_address = Address(local_host, local_port)
    peer_address = Address(peer_host, peer_port)

    max_lines = 10000
    count = 0
    with open(data_path, mode="r", encoding="utf-8") as f:
        data = []
        for line in f:
            if count >= max_lines:
                break
            data.append(line.rstrip().encode("utf-8"))
            count += 1

    with make_pair(local_address, peer_address) as pair:
        server = Server(pair, data)  # psi server
        logging.info("start prepare")
        server.prepare()  # prepare stage
        logging.info("finish prepare")

        logging.info("start intersection")
        server.intersect()  # intersect stage, res is the intersection
        logging.info("finish intersection")

        pair.barrier()
        
