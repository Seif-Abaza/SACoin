# 📦 SACoin --- Full Repository Scan & Explanation

*A micro-blockchain for learning: Blocks, Mining (Proof of Work), Transactions, Rewards, NFTs (mint/transfer), Coin burning, and simple smart contracts. Requires Python 3.9+ and the ecdsa package. All demo/experiment files live in the Demo folder.*

## 🔍 Overview

**SACoin** is a lightweight, educational blockchain written in Python.\
It implements the fundamental components of a cryptocurrency system:

-   Blocks & Blockchain\
-   Transactions, Signatures & Wallets\
-   Proof-of-Work Mining\
-   Rewards & Coin Burning\
-   NFT Minting & Transfers\
-   Basic Smart-Contract Support\
-   Network Modules\
-   Demonstration Scripts (in the `Demo/` folder)

## 📁 Repository Structure

    SACoin/
    │
    ├── .vscode/               → Editor configuration files
    ├── Blockchain/            → Core blockchain logic
    ├── Network/               → Peer-to-peer or RPC networking logic
    ├── SmartContract/         → Basic contract interpreter / contract examples
    ├── Demo/                  → All runnable scripts and demonstrations
    ├── __pycache__/           → Auto-generated Python bytecode (ignore)
    └── README.md              → Main project description

## 🧠 Detailed Explanation of Each Major Component

### 1. Blockchain/

This folder contains the heart of the system.

### Expected Modules Inside

-   Block\
-   Blockchain Manager\
-   Transactions\
-   Proof-of-Work Miner

### 2. Network/

Handles communication between nodes.

### 3. SmartContract/

A simplified smart-contract engine.

### 4. Demo/

Contains runnable examples showing how SACoin works.

## 🧪 Audit Checklist

-   Blockchain integrity\
-   Transaction security\
-   Smart contract safety\
-   Network validation\
-   Mining correctness\
-   Code quality

## Requirements

- Python 3.9+
- ecdsa

```bash
pip install ecdsa
```

