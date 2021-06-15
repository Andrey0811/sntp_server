import socket
import struct
from multiprocessing.pool import ThreadPool

from sntp_server.const import *


class Server:
    def __init__(self, delta, host='127.0.0.1', port=123):
        self._port = port
        self._host = host
        self._delta = delta
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((host, self._port))

    def start_answer(self, input_packet, addr):
        answer = self.get_packet(input_packet, self.get_bytes_fake_time())
        self._sock.sendto(answer + self.get_bytes_fake_time(), addr)

    def work(self):
        while True:
            data, addr = self._sock.recvfrom(CHUNK)
            print(f'{addr} accept to {self._host}:{self._port}')
            ThreadPool(COUNT_THREAD).apply_async(self.start_answer, args=(data, addr))

    def get_bytes_fake_time(self):
        time = (datetime.datetime.utcnow() - EPOCH_TIME).total_seconds() + self._delta
        sec, mil_sec = [int(x) for x in str(time).split('.')]
        return struct.pack('!II', sec, mil_sec)

    def get_packet(self, input_packet, come_time):
        return struct.pack('!B', (0 << 6 | 3 << 3 | 4)) + struct.pack('!B', 1) \
               + struct.pack('!b', 0) + struct.pack('!b', -20) + struct.pack('!i', 0) \
               + struct.pack('!i', 0) + struct.pack('!i', 0) \
               + self.get_bytes_fake_time() + input_packet[40:48] + come_time
        # first_byte + stratum
        # + poll + precision + delay
        # + dispersion + serv_id +
        # + fake_begin_time + input_time + come_time
