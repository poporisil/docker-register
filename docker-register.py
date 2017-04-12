#!/usr/bin/env python

import os
import sys
import argparse
import threading
import subprocess
import time
from urlparse import urlparse
import docker
import etcd
import json
import logging
import logging.handlers


parser = argparse.ArgumentParser(description='Docker Register')
parser.add_argument('-e','--etcd-url', default='http://localhost:4001',
                    help='etcd url (default: http://localhost:4001)')
parser.add_argument('-d','--docker-url', default='unix://var/run/docker.sock',
                    help='docker url (default: unix://var/run/docker.sock)')
parser.add_argument('--docker-api-ver', default='1.23',
                    help='docker api version (default: 1.23)')
parser.add_argument('-t','--ttl', type=int, default=15,
                    help='register ttl (default: 15)')
parser.add_argument('-l','--log-path', default='.',
                    help='log path (default: .)')

args = parser.parse_args()

etcdUrl = args.etcd_url
dockerUrl = args.docker_url
dockerApiVer = args.docker_api_ver
ttl = args.ttl
logPath = args.log_path


logger = logging.getLogger('DockerRegister')
handler = logging.handlers.RotatingFileHandler(logPath + '/docker-register.log', backupCount=10)
formatter = logging.Formatter(fmt='%(asctime)s] (%(levelname)s) %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info('-- Parameters --------------------------')
logger.info('etcdUrl = %s' % etcdUrl)
logger.info('dockerUrl = %s' % dockerUrl)
logger.info('dockerApiVer = %s' % dockerApiVer)
logger.info('ttl = %d' % ttl)
logger.info('logPath = %s' % logPath)
logger.info('-----------------------------------------')
 
class DockerRegister(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.dc = docker.Client(base_url=dockerUrl, version=dockerApiVer)
        self.ec = etcd.Client(host=urlparse(etcdUrl).hostname, port=urlparse(etcdUrl).port, protocol=urlparse(etcdUrl).scheme)
        self.internalIp = subprocess.check_output("ip route get 8.8.8.8 | awk '{print $NF; exit}'", shell=True).strip()

    def getContainers(self):
        logger.debug('get container list...')
        bindedContainers = {}
        try:
            for container in self.dc.containers():
                binded = []
                for port in container['Ports']:
                    if 'PublicPort' in port:
                        binded.append('%s:%d-%d/%s'%(self.internalIp, port['PublicPort'], port['PrivatePort'], port['Type']))
                if binded:
                    key = container['Image'].split(':')[0] + '/' + container['Id']
                    bindedContainers[key] = ','.join(binded)
        except Exception:
            logger.exception('get containers fail')
            return None
        return bindedContainers

    def registerContainers(self, containers):
        logger.debug('register containers...')
        for key, value in containers.iteritems():
            logger.debug('register %s' % key)
            try:
                self.ec.write('/containers/' + key, value, ttl=ttl)
            except etcd.EtcdConnectionFailed:
                logger.exception('etcd connection fail')
        pass

    def run(self):
        logger.info('start agent!')
        while True:
            containers = self.getContainers()
            if containers:
                self.registerContainers(containers)
            time.sleep(10)
        pass


if __name__ == '__main__':
    t = DockerRegister()
    t.start()
    t.join()