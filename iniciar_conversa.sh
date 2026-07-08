#!/bin/bash
echo -e "\e[1;35m[+] Inicializando Central de Conversação Neutra Offline...\e[0m"
echo -e "\e[1;34m[+] Carregando Josiefied Qwen2.5 Abliterated nos 12 Núcleos...\e[0m"

# 1. Purga de resíduos da memória RAM para garantir clocks limpos
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

# 2. Entrar na pasta do motor compilado hoje via CMake
cd $HOME/fortaleza_ia/llama.cpp

# 3. Boot do servidor travando os 5.1G na RAM de 32GB com 4096 de contexto
./build/bin/llama-server \
  -m $HOME/fortaleza_ia/Josiefied-Qwen2.5-7B-Instruct-abliterated.i1-Q5_K_M.gguf \
  -c 8192 \
  -t 12 \
  --mlock
