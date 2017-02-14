#!/usr/bin/env python2

#
# MIT License
#
# Copyright (c) 2017 Sean Nowlan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import socket
import requests
import sys

DISCOVERY_IP = '192.168.1.255'
DISCOVERY_SENDPORT = 4950
DISCOVERY_RECVPORT = 4951
DISCOVERY_MSG = 'MCLDAT?'

GET_SN_MSG = '/:SN?'        # get serial number
GET_MN_MSG = '/:MN?'        # get model number
GET_FW_MSG = '/Firmware?'   # get current firmware version
GET_ATT_MSG = '/ATT?'       # get current attenuation in dB
GET_ADD_MSG = '/ADD?'       # unknown handshaking, reproduced from packet capture
SET_ATT_MSG = '/SETATT='    # set attenuation: concatenate value after '=' sign

if __name__ == '__main__':

    if len(sys.argv) == 1:
        try:
            print 'Starting device discovery...\n'
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock1.sendto(DISCOVERY_MSG, (DISCOVERY_IP, DISCOVERY_SENDPORT))

            sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock2.settimeout(1.0)
            sock2.bind(('0.0.0.0', DISCOVERY_RECVPORT))
            data, addr = sock2.recvfrom(4096)

            print 'Found device:\n'
            print data

            http_url = 'http://' + addr[0]  # addr: (ip, port)
        except:
            print 'UDP communication error.'
            exit(-1)
    elif len(sys.argv) == 2:
        http_url = 'http://' + sys.argv[1]
    else:
        print 'Usage: %s [IP_ADDR]' % sys.argv[0]
        exit(-1)

    print 'Using URL: %s\n' % http_url

    try:
        r = requests.get(http_url + GET_SN_MSG, params={'':''})
        print 'Serial number: %s' % r.text

        r = requests.get(http_url + GET_MN_MSG, params={'':''})
        print 'Model number: %s' % r.text

        r = requests.get(http_url + GET_FW_MSG, params={'':''})
        print 'Firmware version: %s' % r.text

        r = requests.get(http_url + GET_ADD_MSG, params={'':''})
        print 'ADD command reply (expected: 255): %s' % r.text

        r = requests.get(http_url + GET_ATT_MSG, params={'':''})
        print 'Current attenuation: %s' % r.text
    except requests.exceptions.Timeout:
        print 'HTTP request timed out.'
        exit(-1)
    except requests.exceptions.RequestException as e:
        print 'HTTP error: %s' % e
        exit(-1)

    quit = False
    while not quit:
        s = raw_input('\nEnter attenuation in dB (min: 0, max: 125, step: 0.25) or "q" to quit: ')
        try:
            if len(s) == 0:
                r = requests.get(http_url + GET_ATT_MSG, params={'':''})
                print '\nCurrent attenuation: %s' % r.text
            elif s == 'q':
                print '\nExiting.'
                quit = True
            else:
                atten = float(s)
                r = requests.get(http_url + SET_ATT_MSG + s)
                response_code = r.text
                if response_code != '1':
                    print '\nInvalid value entered.'
                r = requests.get(http_url + GET_ATT_MSG, params={'':''})
                if response_code == '1' and float(r.text) != float(s):
                    print '\nRequested and actual values do not match.'
                print '\nCurrent attenuation: %s' % r.text
        except ValueError:
            print 'Invalid value entered.'
        except:
            print 'HTTP request failed.'
