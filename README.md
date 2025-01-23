# Steps to run

## Visualize

```bash
# inside poetry shell in directory redalyze/redalyze
poetry run python index.py
```

## Unit test(manual)

- Make sure `main.py` has correct URLs for both online and offline
- All the visualization units are inside `visualizations/`
- `analyze_data.py` is the one to edit for testing which gets called inside `main.py`

`poetry run python main.py`