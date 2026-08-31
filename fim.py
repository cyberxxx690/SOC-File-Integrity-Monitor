import os
import hashlib
import time
import logging

# Configure the logging artifact
logging.basicConfig(
    filename='fim_alerts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def calculate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def create_baseline(target_folder, baseline_file="baseline.txt"):
    """Creates a baseline of file hashes and saves to a text file."""
    print(f"[*] Calculating baseline for folder: {target_folder}")
    if os.path.exists(baseline_file):
        os.remove(baseline_file)
        
    with open(baseline_file, 'w') as f:
        for root, _, files in os.walk(target_folder):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    f.write(f"{filepath}|{file_hash}\n")
                    print(f"  [+] Hashed: {filename}")
    print("\n[*] Baseline successfully created and saved to baseline.txt!")

def load_baseline(baseline_file="baseline.txt"):
    """Loads the baseline file into a Python dictionary for fast lookups."""
    baseline_dict = {}
    if not os.path.exists(baseline_file):
        print("[-] Baseline file not found. Please create one first.")
        return None
        
    with open(baseline_file, 'r') as f:
        for line in f:
            filepath, file_hash = line.strip().split('|')
            baseline_dict[filepath] = file_hash
    return baseline_dict

def monitor_environment(target_folder, baseline_file="baseline.txt"):
    """Continuously monitors the target folder for changes."""
    print(f"\n[*] Loading baseline into memory...")
    baseline_dict = load_baseline(baseline_file)
    if not baseline_dict:
        return

    print(f"[*] Started monitoring: {target_folder}")
    print("[*] Press Ctrl+C to stop monitoring.\n")
    
    try:
        while True:
            time.sleep(1) # Rest for 1 second to prevent maxing out the CPU
            
            # Step 1: Check for modified or newly created files
            current_files = []
            for root, _, files in os.walk(target_folder):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    current_files.append(filepath)
                    
                    live_hash = calculate_file_hash(filepath)
                    
                    # If it's a new file
                    if filepath not in baseline_dict:
                        alert = f"NEW FILE DETECTED: {filepath}"
                        print(f"  [!] {alert}")
                        logging.warning(alert)
                        baseline_dict[filepath] = live_hash # Update dictionary to suppress duplicate alerts
                        
                    # If the file exists but the hash changed
                    elif baseline_dict[filepath] != live_hash:
                        alert = f"FILE MODIFIED: {filepath}"
                        print(f"  [!] {alert}")
                        logging.warning(alert)
                        baseline_dict[filepath] = live_hash
                        
            # Step 2: Check for deleted files
            deleted_files = []
            for filepath in baseline_dict:
                if filepath not in current_files:
                    alert = f"FILE DELETED: {filepath}"
                    print(f"  [!] {alert}")
                    logging.warning(alert)
                    deleted_files.append(filepath)
                    
            # Remove deleted files from dictionary so we don't alert twice
            for filepath in deleted_files:
                del baseline_dict[filepath]

    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped by user.")

if __name__ == "__main__":
    print("=== File Integrity Monitor ===")
    print("1. Create new baseline")
    print("2. Monitor for changes")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == '1':
        folder = input("Enter the folder path to monitor: ")
        create_baseline(folder)
    elif choice == '2':
        folder = input("Enter the folder path to monitor: ")
        monitor_environment(folder)
    else:
        print("Invalid choice.")
