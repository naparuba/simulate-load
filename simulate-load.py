import os
import sys
import subprocess
import multiprocessing
import requests as rq
import random
import time
import shlex
import io



def f():
    l = []
    for i in xrange(random.randint(1, 1000000)):
        l.append(i)
    time.sleep(1)


if __name__ == '__main__':
    print 'Launching vairous loads'

    ddproc = None
    while True:
        # simulate various memory size, in a sub process so the memory is not leak
        p = multiprocessing.Process(target=f)
        p.start()
        p.join()


        # Massive sys use
        if random.random() < 0.3:
            print "Massive forking"
            for ii in xrange(random.randint(1, 1000)):
                p = subprocess.Popen(shlex.split('/bin/true'), stdout=None, stderr=None)
                p.communicate()
                try:
                    p.terminate()
                except: 
                    pass

        # Massive ios
        if random.random() < 0.3:
            print "Launching dd proc"
            p = os.path.expanduser('~/load.dat')
            count = random.randint(1, 20)
            ddcmd = 'dd if=/dev/urandom of=%s bs=1M count=%d' % (p, count)
            ddproc = subprocess.Popen(shlex.split(ddcmd), stdout=None, stderr=None)#subprocess.PIPE)
            ddproc.communicate()
            try:
                ddproc.terminate()
            except:
                pass


        # network usage, quite 
        if random.random() < 0.3:
            print "Launching web"
            for i in xrange(random.randint(1, 3)):
                for u in ['http://fr.msn.com', 'https://github.com/', 'http://news.google.fr']:
                    try:
                        r = rq.get(u)
                        v = r.text
                        print len(v)
                    except Exception, exp:
                        print 'HTTP exception', exp

        time.sleep(random.randint(1, 3))
