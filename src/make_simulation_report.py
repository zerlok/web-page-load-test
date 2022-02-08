import functools as ft
import sys
import typing as t
from datetime import datetime

import numpy as np
import pandas as pd


def perc(q):
    return ft.partial(np.percentile, q=q)


def ratio(values):
    return np.count_nonzero(values) / np.size(values)


def load_csv(path: str) -> pd.DataFrame:
    data = pd.read_csv(
        path,
        dtype={"link": str, "errors": str, "duration": float},
        parse_dates=["ts"],
        date_parser=datetime.fromisoformat,
    )

    return data


def main(argv: t.Sequence[str]) -> int:
    data = load_csv(argv[1])

    result = data \
        .assign(mean=data["duration"], std=data["duration"], perc50=data["duration"], perc90=data["duration"],
                fails=data["error"].notnull()) \
        .groupby("link") \
        .agg({"mean": np.mean, "std": np.std, "perc50": perc(0.50), "perc90": perc(0.90), "fails": ratio}) \
        .sort_values("mean")

    result.to_csv(sys.stdout, header=("mean", "duration", "perc50", "perc90", "fails"))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
