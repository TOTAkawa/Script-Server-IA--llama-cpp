# 🚀 terminal_IA_automatic

A high-performance Bash orchestration suite designed to deploy and interact with the **DeepSeek-Coder-V2-Lite** Large Language Model (LLM) completely offline on Arch Linux. 

This project bridges infrastructure engineering, low-level OS optimization, and local AI orchestration to serve as a fast reverse-engineering assistant.

## 🛠️ Tech Stack & Infrastructure

- **Host OS:** Arch Linux (Rolling Release)
- **CPU Engine:** Native `llama.cpp` server compiled via CMake
- **Hardware Profile:** 12-Core Intel Xeon CPU / 32GB RAM
- **Model Architecture:** DeepSeek-Coder-V2-Lite-Instruct (Q4_K_M GGUF format)
- **Automation:** POSIX Bash Scripts

## ⚡ Linux Kernel & Performance Optimizations

To extract maximum performance from the Intel Xeon architecture and eliminate latency during inference, the automation scripts apply critical low-level kernel tweaks:

1. **RAM Defragmentation (`drop_caches`):** Prior to loading the model, the script forces the Linux kernel to clear clean caches, dentries, and inodes (`sync && echo 3 | sudo tee /proc/sys/vm/drop_caches`). This ensures a completely clean 32GB memory block layout.
2. **Memory Locking (`--mlock`):** The engine locks the entire GGUF binary directly into physical RAM. This strictly prohibits the Linux kernel from swapping model pages to Disk/Swap, maintaining ultra-low token generation latency.
3. **Core Pinning:** Allocates execution threads precisely across all 12 physical CPU cores (`-t 12`) preventing thread context-switching overhead.

## 📦 Directory Structure

```text
fortaleza_ia/
├── .gitignore             # Excludes heavy GGUF binaries and log files
├── LICENSE                # MIT License terms
├── README.md              # Project documentation
├── iniciar_ia.sh          # Linux memory prep and Server deployment script
└── iniciar_conversa.sh    # Local API communication client
```

## 🚀 Installation & Setup

-Git
-CMake
-gcc/g++
-curl

Ensure your system has the required build tools and packages:
```bash
sudo pacman -S git cmake base-devel curl
```

### 1. Clone and Build the Engine
```bash
mkdir -p \(HOME/fortaleza_ia && cd\)HOME/fortaleza_ia
git clone 
cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

### 2. Download the Model weights (Manual Step)
*Do not commit this file to Git. Download the weights into `$HOME/fortaleza_ia/`:*
- Model: `DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf`

### 3. Deploying the Environment
Clone this automation repository from Codeberg:
```bash
git clone 
cd fortaleza_ia
chmod +x iniciar_ia.sh iniciar_conversa.sh
```

## 🎮 How to Run

### Step 1: Boot the LLM Server Engine
Run the main orchestrator. It will request `sudo` privileges to clear kernel caches, optimize the 32GB RAM layout, and boot the server on local port `8080`:
```bash
./iniciar_ia.sh
```

### Step 2: Interact with the AI
Open a secondary terminal split or window on your Arch Linux environment and run the client:
```bash
./inversa_conversa.sh
```

## 🧠 Engineering Insights

- **Zero Cloud Footprint:** The environment operates completely offline, ensuring absolute privacy for secure reverse engineering analysis.
- **Fail-Safe Mechanism:** Scripts include automated directory verification to ensure clean execution and avoid silent failures or broken runtime paths.

> [!WARNING]
> **Do not run multiple instances simultaneously!**
> Running two or more AI instances at the same time will cause network port conflicts (port 8080), high CPU core contention on your Xeon processor, and may completely exhaust your 32GB of RAM. Always stop the current server before launching a new session.


## 📄 License

This orchestration suite is released under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

