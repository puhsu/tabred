import os

os.environ['PROJECT_DIR'] = '/home/irubachev/repos/big'

import lib
import pandas as pd

import plotnine as p9

from typing import cast

datasets = [
    f'homesite-insurance-sliding-window-{i}'
    for i in range(3)
] + [
    f'homesite-insurance-random-{i}'
    for i in range(3)
]

data = cast(pd.DataFrame, pd.json_normalize(
    [lib.load_json(f) | {'name': 'mlp-plr', 'split': ' '.join(d.split('-')[-2:])} for d in datasets for f in lib.EXP_DIR.glob(f'mlp-plr/{d}/**/report.json')] + 
    [lib.load_json(f) | {'name': 'xgboost', 'split': ' '.join(d.split('-')[-2:])} for d in datasets for f in lib.EXP_DIR.glob(f'xgboost_/{d}/**/report.json')]
)[['name', 'config.data.path', 'metrics.test.score', 'split', 'config.seed']])
# .groupby(['config.data.path', 'split', 'name']).agg(['mean', 'std', 'count']))
# data = data.reset_index()

data.columns = ["model", "dataset", "score", "split", "seed"]
data.dataset = data.dataset.str.removeprefix(':data/')
data.split = data.split.replace({"homecredit-v0.1": "t"})

data

import plotnine as p9

fig = (
    p9.ggplot(data)
    + p9.geom_boxplot(
        p9.aes(x="split", y="score", fill="model", color="model"),
        position="dodge",
        outlier_shape=".",
    )
    + p9.theme(axis_text_x=p9.element_text(rotation=45, hjust=1))
    + p9.ggtitle("Homesite Example Run")
)

fig
