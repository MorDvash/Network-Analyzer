import datetime
import json
from typing import Dict
import logging
import pyshark

logger = logging.getLogger(__name__)


class NetworkReceiver:

    def __init__(self, iface_name: str, filter_bpf: str = None, timeout: int = 10):
        """
        :param iface_name: Name of the interface to sniff on. If not given, takes the first available.
        :param filter_bpf: BPF filter to use on packets example - port 443.
        :param timeout: timeout in seconds to sniff the network.
        """
        self.iface_name = iface_name
        self.filter_bpf = filter_bpf
        self.timeout = timeout

    def start_sniff(self):
        """
        start sniffing network on the given interface
        :return: list of ip layers
        """
        # capture = pyshark.LiveCapture(interface=self.iface_name, bpf_filter=self.filter_bpf)
        capture = pyshark.LiveCapture()
        capture.sniff(timeout=self.timeout)
        return capture

    @staticmethod
    def process_packet(packet) -> Dict:
        """
        :param packet: packet network data.
        :return: dictionary of IP data.
        """
        current_date = datetime.datetime.now()
        return {
            "version": packet.ip.version,
            "hdr_len": packet.ip.hdr_len,
            "dsfield": packet.ip.dsfield,
            "dsfield_dscp": packet.ip.dsfield_dscp,
            "dsfield_ecn": packet.ip.dsfield_ecn,
            "len": packet.ip.len,
            "id": packet.ip.id,
            "flags": packet.ip.flags,
            "flags_rb": packet.ip.flags_rb,
            "flags_df": packet.ip.flags_df,
            "flags_mf": packet.ip.flags_mf,
            "frag_offset": packet.ip.frag_offset,
            "ttl": packet.ip.ttl,
            "proto": packet.ip.proto,
            "checksum": packet.ip.checksum,
            "checksum_status": packet.ip.checksum_status,
            "src": packet.ip.src,
            "addr": packet.ip.addr,
            "src_host": packet.ip.src_host,
            "host": packet.ip.host,
            "dst": packet.ip.dst,
            "dst_host": packet.ip.dst_host,
            "created_at": json.dumps(current_date, default=str)
        }
