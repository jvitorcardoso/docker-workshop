import sys
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

print(df['B'])

arg = sys.argv[1] if len(sys.argv) > 1 else "default"
print(f"Pipeline argument: {arg}")