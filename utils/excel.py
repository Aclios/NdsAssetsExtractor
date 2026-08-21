from typing import Any
import pandas as pd

def write_excel(out_path: str, data: list[list[Any]], columns: list[str]):
    df = pd.DataFrame(data=data, columns=columns)
    df.to_excel(out_path, index=False)