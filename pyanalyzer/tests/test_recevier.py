from os import environ
from unittest.mock import patch

from src.recevier import NetworkReceiver
from dotenv import load_dotenv

load_dotenv()

IFACE_NAME = environ.get("IFACE_NAME")

packet_ip_mock = {
    "version": "4",
    "hdr_len": "20",
    "dsfield": "0x00",
    "dsfield_dscp": "0",
    "dsfield_ecn": "0",
    "len": "199",
    "id": "0x0000",
    "flags": "0x02",
    "flags_rb": "0",
    "flags_df": "1",
    "flags_mf": "0",
    "frag_offset": "0",
    "ttl": "64",
    "proto": "6",
    "checksum": "0xb5da",
    "checksum_status": "2",
    "src": "192.168.1.141",
    "addr": "192.168.1.141",
    "src_host": "192.168.1.141",
    "host": "192.168.1.141",
    "dst": "192.168.1.121",
    "dst_host": "192.168.1.121"
}


def test_start_sniff_successfully():
    network_receiver = NetworkReceiver(IFACE_NAME)
    capture = network_receiver.start_sniff()
    assert len(capture) > 0


@patch('src.recevier.NetworkReceiver.start_sniff')
def test_start_sniff_unsuccessfully(start_sniff_mock):
    start_sniff_mock.return_value = []
    network_receiver = NetworkReceiver(IFACE_NAME)
    capture = network_receiver.start_sniff()
    assert len(capture) == 0
