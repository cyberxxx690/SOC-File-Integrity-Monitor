import os
import hashlib

def calculate_file_hash(filepath):
    """
    Calculates the SHA-256 hash of a file.
    We read the file in 64kb chunks to easily handle massive files without crashing the RAM.
    """
    hasher = hashlib.sha256()
    try:
        # 'rb' means read in binary mode, which is required for hashing
        with open(filepath, 'rb') as file:
            while chunk := file.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"[-] Error reading {filepath}: {e}")
        return None

def create_baseline(target_folder, baseline_file="baseline.txt"):
    """
    Walks through all files in a folder, calculates their hashes, 
    and saves them securely to a text file.
    """
    print(f"[*] Calculating baseline for folder: {target_folder}")
    
    # Erase the old baseline file if it exists so we start completely fresh
    if os.path.exists(baseline_file):
        os.remove(baseline_file)
        
    # Open the baseline file in write mode
    with open(baseline_file, 'w') as f:
        # os.walk automatically goes through all folders and subfolders
        for root, _, files in os.walk(target_folder):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_hash = calculate_file_hash(filepath)
                
                if file_hash:
                    # Save it in a simple structured format: "path|hash"
                    f.write(f"{filepath}|{file_hash}\n")
                    print(f"  [+] Hashed: {filename}")
                    
    print("\n[*] Baseline successfully created and saved to baseline.txt!")

if __name__ == "__main__":
    print("=== File Integrity Monitor ===")
    print("1. Create new baseline")
    print("2. Monitor for changes (Coming in Phase 3!)")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == '1':
        folder = input("Enter the folder path to monitor (e.g., ./test_folder): ")
        create_baseline(folder)
    else:
        print("Monitoring logic has not been built yet!")
