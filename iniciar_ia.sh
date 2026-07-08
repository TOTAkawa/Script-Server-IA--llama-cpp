#!/bin/bash

# 1. Alerta visual de controle no prompt
echo -e "\e[1;32m[+] Inicializando Central de Engenharia Reversa Offline...\e[0m"
echo -e "\e[1;34m[+] Carregando DeepSeek-Coder-V2 nos 12 Núcleos do Xeon...\e[0m"

# 2. Expurgar resíduos e fragmentações antigas da memória RAM de 32GB
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

# 3. Entrar na pasta do motor que compilamos hoje via CMake
cd $HOME/fortaleza_ia/llama.cpp

# 4. Boot do servidor com 2048 tokens de contexto travados na memória
./build/bin/llama-server \
  -m $HOME/fortaleza_ia/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf \
  -c 8192 \
  -t 12 \
  --mlock
