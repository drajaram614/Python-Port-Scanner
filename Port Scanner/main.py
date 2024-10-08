import socket  # socket library to create network connections
from queue import Queue  # Queue for thread-safe communication
import threading  #threading to run multiple tasks at once
import logging  #logging to display messages
import random  #create random delays in stealth mode
import time  # handling time delays

# Set up logging to show info-level messages with timestamps and severity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

target = "127.0.0.1"  #target IP address, set by default to localhost (your own machine)
queue = Queue()  #queue hold ports that need to be scanned
open_ports = []  #A list to store any open ports found during the scan

# Function to check if a port is open, includes stealth mode 
def portscan(port, stealth_mode=False):
    try:
        #creating TCP socket to connect to a port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  #if the port doesn't respond in 1 second, move on
        sock.connect((target, port))  #try connecting to given port
        
        # If stealth mode is enabled, wait for a random time (between 0.5 to 1.5 seconds)
        if stealth_mode:
            time.sleep(random.uniform(0.5, 1.5))  # Adding random delays to avoid detection

        return True  #connection is successful, return True (port is open)
    except (socket.timeout, socket.error):  #error if (timeout or connection refused)
        return False  #port closed, return False
    finally:
        sock.close()  #close socket after scanning

#function to decide which ports to scan based on user selection
def get_ports(mode):
    if mode == 1:
        # mode 1: scan ports 1 to 1024 (well-known ports)
        for port in range(1, 1024):
            queue.put(port)#Add each port to the queue
    elif mode == 2:
        #mode 2: scan a large range of ports (up to 49152)
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        #mode 3: scan a small list of commonly used ports (like 80 for HTTP)
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        #mode 4: let the user manually enter the ports to scan
        ports = input("Enter your ports (separated by space): ")#user input
        try:
            #Split input into individual ports, convert to integers and add them to the queue
            ports = list(map(int, ports.split()))
            for port in ports:
                queue.put(port)
        except ValueError:
            logging.error("Invalid port input. Please enter valid port numbers.")

# Shuffle the order of the ports in the queue to avoid sequential scanning (useful for stealth mode)
def shuffle_queue():
    temp_list = list(queue.queue)  #Get the ports in the queue as a list
    random.shuffle(temp_list)  #randomly shuffle the list
    queue.queue.clear()  #clear the original queue
    for item in temp_list:
        queue.put(item)  #put the shuffled ports back into the queue

#function that runs the port scan on ports from the queue
def worker(stealth_mode=False):
    while not queue.empty():#scanning until the queue is empty
        port = queue.get() #get port from the queue
        if portscan(port, stealth_mode): #scan with stealth mode if enabled
            logging.info(f"Port {port} is open!")  #log open ports
            open_ports.append(port)  #add open ports to the list
        else:
            logging.info(f"Port {port} is closed!")  #log closed ports
        queue.task_done()  # mark the task as done for the queue

# function to run the scanner with multi-threading and user picked: stealth mode
def run_scanner(threads, mode, stealth_mode=False):
    get_ports(mode)  # get ports to scan based on the selected mode
    
    if stealth_mode:
        shuffle_queue()  #if stealth mode is enabled, randomize the scan order

    thread_list = []  #create a list to hold all threads

    for t in range(threads):  #start specified number of threads
        thread = threading.Thread(target=worker, args=(stealth_mode,))
        thread_list.append(thread)  #add thread to list

    for thread in thread_list:
        thread.start()  #start each thread

    queue.join()  #wait until all tasks in the queue are done

    for thread in thread_list:
        thread.join() #wait for all threads to finish

    logging.info(f"Open ports are: {open_ports}")  #log all open ports found


if __name__ == "__main__":
    try:
        # Ask user input for target IP/hostname, number of threads, and mode
        target = input("Enter the target IP (or hostname): ")
        target = socket.gethostbyname(target)  #convert hostname to IP address
        threads = int(input("Enter number of threads: "))
        mode = int(input("Select mode (1-4): "))
        
        # Asking if stealth mode should be enabled
        stealth_choice = input("Enable stealth mode? (y/n): ").lower()
        stealth_mode = True if stealth_choice == 'y' else False
        
        #run port scanner
        run_scanner(threads, mode, stealth_mode)
    #error logging
    except ValueError:
        logging.error("Invalid input. Please provide a valid number.")
    except socket.gaierror:
        logging.error("Hostname could not be resolved. Please check the target.")
