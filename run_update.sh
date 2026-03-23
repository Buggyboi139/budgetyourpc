#!/bin/bash

echo "========================================"
echo "Starting PCBudget Auto-Update Script"
echo "Time: $(date)"
echo "========================================"

echo "[+] Running update_prices.py..."
/home/dsmason321/venv/bin/python3 update_prices.py

if [[ `git status --porcelain products.json` ]]; then
    echo "[+] Price or availability changes detected. Committing to repository..."
    
    git add products.json
    
    git commit -m "chore: automated PC parts price update $(date +'%Y-%m-%d %H:%M')"
    
    git push origin main
    
    echo "[+] Successfully pushed new prices to the live site!"
else
    echo "[-] No changes detected in products.json. Prices are up to date."
fi

echo "========================================"
echo "Update Finished."
echo "========================================"
