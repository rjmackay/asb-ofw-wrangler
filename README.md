# OFX Wrangler

- Swaps memo and name fields when name is just DEBIT/CREDIT/EFTPOS
- Strip pointless memos like "CARD" or "FC" 

## Usage

```
uv run main.py input.ofx -o
```

Note: `-o` Updates the file in place
