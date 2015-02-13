# Blobtastical

import threading
import logging
import serial
import time

class Port(object):
    def __init__(self, dev, baud, parity):
        if parity == 'e':
            p = serial.PARITY_EVEN
        if parity == 'n':
            p = serial.PARITY_NONE
        if parity == 'o':
            p = serial.PARITY_ODD
        self.baud = baud
        self.ser = serial.Serial(dev, baud, parity=p, timeout=0)


class ReaderPort(Port):
    def __init__(self, dev, baud, parity):
        super(ReaderPort, self).__init__(dev, baud, parity)
        self.expected = None

    def expect(self, data):
        """
        start a waiting thread that will expect to receive 'data' in a timely fashion
        :param data: the exact data that will be sent from the writer side.
        :return:
        """
        self.expected = data
        logging.info("attempting to start a listening thread")
        self.t = threading.Thread(target=self.run)
        self.t.start()

    def run(self):
        rtt = len(self.expected) / self.baud
        if rtt < 1:
            rtt = 1
        logging.info("going to wait for %f secs", rtt)
        start = time.time()
        while time.time() - start < rtt:
            x = self.ser.read()
            logging.info("so far: %s", x)
            time.sleep(0.1)

    def join(self):
        self.t.join()

class WriterPort(Port):
    def write(self, data):
        self.ser.write(data)
        logging.info("finished writing data to writerport")






