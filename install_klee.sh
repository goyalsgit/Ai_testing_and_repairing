#!/bin/bash
# Install KLEE dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake python3 python3-pip
sudo apt-get install -y llvm-11 llvm-11-dev clang-11 libclang-11-dev
sudo apt-get install -y libz3-dev

# Clone and build KLEE
git clone https://github.com/klee/klee.git
cd klee
mkdir build && cd build
cmake -DLLVM_CONFIG_BINARY=/usr/bin/llvm-config-11 ..
make -j$(nproc)
sudo make install
cd ../..
