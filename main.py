import threading
from termcolor import colored as c
import time
import requests
import argparse
import os
import sys

def info(msg):
    if not args.quiet:
        print(c(msg, "blue"))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxies', help='File containing all the proxies in this format: proto://ip:port', required=True)
    parser.add_argument('-t', '--threads', help='Amount of threads.', required=False, default=40)
    parser.add_argument('-f', '--format', help='Format of output. Options: 0: proto://ip:port 1:proto ip port', required=True, type=int)
    parser.add_argument('-q', '--quiet', help='Only displays the final results.', required=False, default=False, action="store_true")
    parser.add_argument('-c', '--cycles', help='How many times proxygod will check the proxies (helps to discovery stable proxies)', type=int, default=1)

    args = parser.parse_args()
    return args

def thread(proxy):
    if len(proxy) > 2:
        try:
            formatt = c(f"🌹🪦🌹 {proxy} {' ' * (40 - (len(proxy) + 4) )} {variables.current}/{variables.overall}{' ' * 20}", 'red')

            r = requests.get("https://www.whatismyip.net/", proxies=dict(http=proxy, https=proxy), timeout=2)
            if r.status_code == 200 and "What Is My IP | Whats My IP Address | GeoIP Location | Check IP Information | IP Tools" in r.text:
                 variables.working.append(proxy)
                 if not args.quiet:
                     print(c(f"📡 {proxy} {' ' * 50}", 'green'))
            r = ""
        except KeyboardInterrupt:
            sys.exit()

        except requests.exceptions.ConnectionError:
            if not args.quiet:
                print(formatt)
            pass

        except requests.exceptions.ReadTimeout:
            if not args.quiet:
                print(formatt)
            pass

        except Exception as e:
            print(e)
            
    variables.cur_running -= 1
    exit()

def main(args):
    info("🔄Cycle 1🔄")
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


#    os.system("clear")    




    for cycle in range(2,args.cycles):

        working_temp = variables.working
        variables.working = []

        info(f"🔄Cycle {cycle}🔄")

        variables.current = 0
        variables.overall = len(working_temp)

        for proxy in working_temp:
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


#        os.system("clear")

    if args.format == 1:
        for proxy in variables.working:
            formatted = proxy.replace('://', ' ').replace(':', ' ')
            if len(formatted) > 1:
                print(formatted.strip())

    elif args.format == 0:
        for proxy in variables.working:
            if len(proxy) > 1:
                print(proxy.strip())
    
    else:
        print("Invalid format...")
        sys.exit(1)
    
if __name__ == "__main__":
   args = get_args()

   class variables:
    working = []
    cur_running = 0
    overall = 0
    current = 0
    threads = int(args.threads)
   
   main(args)
