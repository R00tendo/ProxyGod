import threading
from termcolor import colored as c
import time
import requests
import argparse
import os
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxies', help='File containing all the proxies in this format: proto://ip:port', required=True)
    parser.add_argument('-t', '--threads', help='Amount of threads.', required=False, default=40)
    parser.add_argument('-f', '--format', help='Format of output. Options: 0: proto://ip:port 1:proto ip port', required=True, type=int)
    parser.add_argument('-q', '--quiet', help='Only displays the final results.', required=False, default=False, action="store_true")

    args = parser.parse_args()
    return args

def thread(proxy):
    try:
        r = requests.get("https://www.whatismyip.net/", proxies=dict(http=proxy, https=proxy), timeout=2)
        if r.status_code == 200 and "What Is My IP | Whats My IP Address | GeoIP Location | Check IP Information | IP Tools" in r.text:
             variables.working.append(proxy)
             if not args.quiet:
                 print(c(f"📡 {proxy}{' ' * (40 - len(proxy) + len(str(variables.overall) + '/' + str(variables.overall)))}{''}", 'green'))
    except KeyboardInterrupt:
        sys.exit()
    except:
        if not args.quiet:
            print(c(f"🌹🪦🌹 {proxy} {' ' * (40 - (len(proxy) + 4) )} {variables.current}/{variables.overall}{' ' * 20}", 'red'), end='\r')
        pass

    variables.cur_running -= 1

def main(args):

    variables.overall = len(open(args.proxies).read().split("\n"))
    for proxy in open(args.proxies).read().split("\n"):
        variables.current += 1
        while variables.cur_running >= variables.threads:
            try:
                time.sleep(0.2)
            except KeyboardInterrupt:
                sys.exit()

        threading.Thread(target=thread, args=(proxy,)).start()
        
        variables.cur_running += 1    

    while variables.cur_running != 0:
      try:
          time.sleep(0.2)
      except KeyboardInterrupt:
          sys.exit()
      
    os.system("clear")    

    if args.format == 1:
        for proxy in variables.working:
            print(proxy.replace('://', ' ').replace(':', ' '))    

    if args.format == 0:
        for proxy in variables.working:
            print(proxy)


if __name__ == "__main__":
   args = get_args()

   class variables:
    working = []
    cur_running = 0
    overall = 0
    current = 0
    threads = int(args.threads)

   main(args)
