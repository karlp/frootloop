#!/usr/bin/env python
#
# Copyright (c) 2015, Karl Palsson <karlp@tweak.net.au>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Serial port back to back testing
"""

import argparse
import logging
import os
import sys
import threading
import time

import frootloop.froot

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def actual_file(arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError("The file %s does not exist!" % arg)
    else:
        return arg

def get_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-1", "--primary", help="Device under test",
                        type=actual_file, default="/dev/ttyUSB0", metavar="DEV")
    parser.add_argument("-2", "--secondary", help="Reliable 'remote' loop device",
                        type=actual_file, default="/dev/ttyUSB1", metavar="DEV")
    parser.add_argument("-b", "--baud", help="Baud rate to request", default=19200, type=int)
    parser.add_argument("-y", "--parity", help="parity to request", default='n', choices=['n','e','o'])

    # Here we add subparsers for each of the test modules...
    # but for now, just run the one we've got...
    return parser


def t1(options):
    """
    Our only test so far
    :param p1: port 1
    :param p2: port 2
    :return:
    """

    # need to start a thread listening on p2
    # then write to p1
    # wait for a while, but timeout after 50% over expected time for baud...
    testdata = "hello karl from the primary side"
    p1 = frootloop.froot.WriterPort(options.primary, options.baud, options.parity)
#    p2 = frootloop.froot.ReaderPort(options.secondary, options.baud, options.parity)
#    p2.expect(testdata)
    x = p1.ser.write(testdata)
    logging.info("write %d bytes to primary", x)
    p1.ser.flush()
#    p2.join()
    logging.info("well?")


def main():
    options = get_parser().parse_args()
    logging.info("we're running")
    t1(options)


if __name__ == "__main__":
    main()