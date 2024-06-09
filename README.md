# OFX Wrangler

- Swaps memo and name fields when name is just DEBIT/CREDIT/EFTPOS
- Strip pointless memos like "CARD" or "FC" 

## Usage

```
pipenv install
pipenv run python ofxwrangler/main.py input.ofx -o
```

Note: `-o` Updates the file in place
