# File Integrity Monitor (FIM) 

Welcome to my custom File Integrity Monitor!

I built this tool to explore how endpoint security agents detect unauthorized changes to critical files. Instead of relying on timestamps (which can be easily spoofed by malware), this script uses strict cryptographic hashing (SHA-256) to prove whether a file has been tampered with.

Basically, you point the script at a critical folder. It calculates the hash of every file and creates a trusted baseline. Then, it runs in a continuous loop, rehashing the live files and checking them against the baseline in memory. If a file is modified, deleted, or created, it instantly triggers an alert and writes it to an audit log.

## What it actually does

- **Cryptographic Baselining:** Uses the SHA-256 algorithm to calculate the unique fingerprint of every file in a target directory and saves it securely to `baseline.txt`.
- **In-Memory Dictionary Lookups:** Loads the baseline into a Python dictionary (Hash Map) for O(1) constant-time lookups, making the continuous monitoring loop incredibly fast and efficient.
- **Real-Time Detection:** Instantly detects and alerts on modified, deleted, or newly dropped files.
- **SIEM-Ready Audit Logging:** Automatically generates a timestamped `fim_alerts.log` file, making it easy to ingest these alerts into a centralized logging server or SIEM.

## The Tech Stack

- **Python 3.9+**
- `hashlib` (For SHA-256 cryptographic hashing)
- `logging` (For secure audit trails)
- `os` & `time` (For file system traversal and background loop management)
- *Zero external dependencies (Built entirely with Python standard libraries!)*

## How to run it on your machine

1. **Clone it down:**

   ```bash
   git clone https://github.com/cyberxxx690/SOC-File-Integrity-Monitor.git
   cd SOC-File-Integrity-Monitor
   ```

2. **Run the script:**

   Since this uses only built-in libraries, no virtual environment or `pip install` is required!

   ```bash
   python3 fim.py
   ```

3. **Follow the on-screen menu:**
   - Select **Option 1** first to create a baseline for a target folder (e.g., `./test_folder`).
   - Select **Option 2** to begin actively monitoring that folder.