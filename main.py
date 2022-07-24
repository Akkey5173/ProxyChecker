import requests
import threading
from pick import pick
from colorama import init
init(convert=True)
from colorama import Fore
from console.utils import set_title

protocol_prefix = "http"
global_ip = "0.0.0.0"
working_proxies = []
timeout = 1
threads = []

def check(proxy):
    global protocol_prefix
    global working_proxies
    global global_ip
    global timeout
    global threads
    proxies = {
        "http": f"{protocol_prefix}://{proxy}",
        "https": f"{protocol_prefix}://{proxy}"
    }
    try:
        response = requests.get("https://api.ipify.org", proxies=proxies, timeout=timeout)
        if response.text == global_ip:
            print(f"{Fore.RED}Not Working: {proxy}{Fore.RESET}")
        elif response.text != global_ip:
            working_proxies.append(proxy)
            print(f"{Fore.GREEN}Working: {proxy}{Fore.RESET}")
    except:
        print(f"{Fore.RED}Not Working: {proxy}{Fore.RESET}")
    threads.remove(threading.current_thread())

def set_ip():
    global global_ip
    response = requests.get("https://api.ipify.org")
    global_ip = response.text

def update_title():
    while True:
        total_threads = str(len(threads))
        total_work_proxies = str(len(working_proxies))
        set_title(f"Proxy Checker | Working: {total_work_proxies} | Threads: {total_threads}")

def main():
    global protocol_prefix
    global working_proxies
    global timeout
    global threads
    print(f"{Fore.YELLOW}Loading{Fore.RESET}")
    set_ip()
    threading.Thread(target=update_title).start()
    with open("proxies.txt", "r", encoding="utf-8") as file:
        proxies = file.read().split("\n")
    selected = pick(["HTTP", "Socks5"], "Protocol:", indicator=">")
    if selected[0][0] == "HTTP":
        protocol_prefix = "http"
    elif selected[0][0] == "Socks5":
        protocol_prefix = "socks5h"
    timeout_input = input("Timeout: ")
    try:
        int(timeout_input)
    except:
        print(f"{Fore.RED}Invalid value{Fore.RESET}")
        return
    timeout = timeout_input
    for proxy in proxies:
        thread = threading.Thread(target=check, args=(proxy,))
        threads.append(thread)
    print(f"{Fore.GREEN}Starting{Fore.RESET}")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"{Fore.GREEN}Saving{Fore.RESET}")
    with open("checked.txt", "w", encoding="utf-8") as file:
        file.write("{}".format("\n".join(working_proxies)))
        file.close()

if __name__ == "__main__":
    main()