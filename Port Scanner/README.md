# Python Port Scanner

## Project Summary
This project is a multithreaded Python-based port scanner that can scan a target machine for open ports. It supports various scanning modes, including a stealth mode that adds random delays to avoid detection. The project was built using Python's `socket`, `threading`, and `queue` libraries, and includes features like user-defined port ranges, common port scanning, and error handling. 

### What I Learned
Working on this project enhanced my understanding of:
- **Network security**: Understanding how open ports can be exploited and how to identify them efficiently.
- **Cybersecurity fundamentals**: Recognizing how port scanners function in real-world scenarios and how to implement security features such as stealth mode.
- **Python skills**: Gained experience in multithreading, socket programming, and error handling in Python.

### Skills Gained
- **Networking**: Deepened knowledge of TCP/IP protocols, port scanning techniques, and how to interact with open/closed ports.
- **Cybersecurity**: Implemented stealth scanning techniques to evade network detection.
- **Python Programming**: Worked with sockets, queues, and threads, learned to handle network timeouts, and used random delays for obfuscation.

## Code Breakdown

### 1. `portscan(port, stealth_mode=False)`
- **Purpose**: This function checks if a specific port is open on the target machine. It attempts to connect using a TCP socket, and if successful, it logs that the port is open.
- **Stealth Mode**: When enabled, this function adds random delays between port scans (ranging from 0.5 to 1.5 seconds), helping the scan avoid detection by intrusion detection systems (IDS).
- **Why**: It is essential to have a mechanism for checking port availability, especially for vulnerability assessments or network testing.

### 2. `get_ports(mode)`
- **Purpose**: Determines which ports to scan based on the user’s selection. It has four modes:
  - **Mode 1**: Scans well-known ports (1-1024).
  - **Mode 2**: Scans a wide range of ports (1-49152).
  - **Mode 3**: Scans commonly used ports (HTTP, FTP, etc.).
  - **Mode 4**: Allows the user to manually specify ports to scan.
- **Why**: Giving users flexibility in how many ports to scan makes the tool versatile for different scenarios.

### 3. `shuffle_queue()`
- **Purpose**: Randomizes the order in which ports are scanned, especially useful in stealth mode to avoid sequential scanning patterns that might trigger alarms in security systems.
- **Why**: Sequential scanning can easily be detected by monitoring systems, so adding randomness helps make the scan less detectable.

### 4. `worker(stealth_mode=False)`
- **Purpose**: A worker thread function that pulls ports from the queue and scans them using the `portscan` function. It handles both open and closed port responses and logs the results.
- **Why**: Multithreading allows the program to scan multiple ports concurrently, speeding up the overall process significantly.

### 5. `run_scanner(threads, mode, stealth_mode=False)`
- **Purpose**: The main function to orchestrate the scanning process. It sets up the ports to scan, creates the worker threads, and monitors their progress. It also supports stealth mode.
- **Why**: This function handles user input, creates threads, and starts the scanning process, managing everything from start to finish. It ensures all ports in the queue are processed and logs open ports once scanning is complete.

### Key Features
- **Multithreading**: Enables scanning across multiple ports simultaneously for faster results.
- **Stealth Mode**: Introduces random delays and shuffling to avoid detection by IDS systems.
- **Error Handling**: Handles invalid user inputs and hostname resolution issues with appropriate logging and error messages.

## Example Output
Below is an example screenshot of the port scanner output:

![Port Scanner Output](screenshot.png)

---
