scores.join(
    scores.filter(pl.col('model').eq('mlp')).drop('moedel'),
    on=['data', 'split', 'split-idx', 'seed'],
    suffix='_mlp',
).with_columns(
    pl.when(pl.col('data').is_in([':data/homecredit-default', ':data/homesite-insurance', ':data/ecom-offers'])).then(
        (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
    ).otherwise(
        -1 * (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
    ).alias('tr-score')
).filter(
    pl.col('split-idx').ne(2),
).group_by(
    'model', 'split',
).agg(
    pl.col('tr-score').median().alias('tr-score-median'),
    pl.col('tr-score').std().alias('tr-score-std'),
).sort('split', -pl.col('tr-score-median'))



tr_scores = scores.join(
    scores.filter(pl.col('model').eq('mlp')).drop('moedel'),
    on=['data', 'split', 'split-idx', 'seed'],
    suffix='_mlp',
).with_columns(
    pl.when(pl.col('data').is_in([':data/homecredit-default', ':data/homesite-insurance', ':data/ecom-offers'])).then(
        (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
    ).otherwise(
        -1 * (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
    ).alias('tr-score')
).filter(
    pl.col('split-idx').ne(2),
)

plot = (
    pn.ggplot(tr_scores, pn.aes(x='model', y='tr-score', color='model'))
    + pn.geom_boxplot(outlier_shape='', width=0.6)
    # + pn.geom_jitter(size=0.5, alpha=0.3)
    # + pn.facet_grid('data', 'split', scales='free', space='free')
    + pn.coord_cartesian(ylim=(-2, 5))
    + pn.stat_summary(fun_y=np.mean, geom='point', color='black', shape='*')
    + pn.facet_wrap('split')
    + pn.scale_x_discrete(limits=['mlp', 'mlp-plr', 'xgboost_', 'tabr'])
)
plot.show()



for d in datasets:
    print(d)
    print(
        mean_scores.join(
            mean_scores.filter(pl.col('model').eq('mlp')).drop('moedel'), on=['data', 'split', 'split-idx'], suffix='_mlp',
        ).with_columns(
            pl.when(pl.col('data').is_in(['homecredit-default', 'homesite-insurance', 'ecom-offers'])).then(
                (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
            ).otherwise(
                -1 * (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
            ).alias('tr-score')
        ).filter(
            pl.col('split-idx').eq(0),
            pl.col('data').eq(d),
        ).sort('data', 'split', -pl.col('score'))[['model', 'split', 'score', 'score_std', 'score_mlp', 'tr-score']]
    )


# Temporal Shift plots
data = pl.DataFrame(cast(pd.DataFrame, pd.json_normalize(
    [
        lib.load_json(f) | {
            'model': m, 'split': s, 'split-idx': si, 'data': d,
            'task': 'regression' if d not in ['homesite-insurance', 'homecredit-default', 'ecom-offers'] else 'binclass'
        }
        for m in ["mlp", "mlp-plr", "xgboost_", "tabr"]
        for d in datasets
        for s in ["random", "sliding-window"]
        for si in range(3)
        for f in lib.EXP_DIR.glob(f'temporal-shift-analysis/{m}/{d}-{s}-{si}/evaluation/**/report.json')
    ]
)))

scores = data.select(
    pl.col('model'),
    pl.col('data'),
    pl.col('split'),
    pl.col('split-idx'),
    pl.col('task'),
    pl.col('metrics.test.score').alias('score'),
    pl.col('config.seed').alias('seed'),
)

# for cmd in [
#  f'python bin/xgboost_.py {f.parent.relative_to(lib.PROJECT_DIR)}.toml --force'
#  for m in ["mlp", "mlp-plr", "xgboost_", "tabr"]
#  for d in datasets
#  for s in ["random", "sliding-window"]
#  for seed in range(15)
#  for si in range(3)
#  if not (f := lib.EXP_DIR/f'temporal-shift-analysis/{m}/{d}-{s}-{si}/evaluation/{seed}/report.json').exists() and d != 'cooking-time'
# ]:
#     print(cmd)


import matplotlib.pyplot as plt


datasets = [
    'sberbank-housing',
    'cooking-time',
    'delivery-eta',
    'maps-routing',
    'weather',
    'homesite-insurance',
    'ecom-offers',
    'homecredit-default',
]


# This for absolutes

# This is averaging seeds in each split for plotting splits then
s = scores.group_by('model', 'data', 'split', 'split-idx').agg(
    pl.col('score').abs().mean()
).group_by(
    'model', 'data', 'split'
).agg(
    pl.col('score')
)


# This is averaging scores on different splits 

# s = scores.group_by('model', 'data', 'split', 'split-idx').agg(
#     pl.col('score').abs().mean()
# ).group_by(
#     'model', 'data', 'split',
# ).agg(
#     pl.col('score')
# )


# This is for deltas
# s = scores.join(
#     scores.filter(pl.col('model').eq('mlp')).drop('moedel'),
#     on=['data', 'split', 'split-idx', 'seed'],
#     suffix='_mlp',
# ).with_columns(
#     pl.when(pl.col('data').is_in(['homecredit-default', 'homesite-insurance', 'ecom-offers'])).then(
#         (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
#     ).otherwise(
#         -1 * (pl.col('score') - pl.col('score_mlp')) / pl.col('score_mlp') * 100
#     ).alias('tr-score')
# ).group_by('model', 'data', 'split').agg(
#     pl.col('tr-score').alias('score')
# )

import matplotlib
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "font.serif": ["Times"],
    "text.usetex": True,
})

fig = plt.figure(figsize=(20, 9))
c1, c2, c3, c4 = '#4DAF4A', '#377EB8', '#E41A1C', '#838383'

for i, d in enumerate(datasets):

    plot_data = []
    for split in ["sliding-window", "random"]:
        for m in ["mlp", "mlp-plr", "xgboost_", "tabr"]:
            plot_data.append(list(s.filter(
                pl.col('data').eq(d),
                pl.col('model').eq(m),
                pl.col('split').eq(split),
            )['score'].item()))

    ax = plt.subplot(2, 5, i+1)
    bplot = ax.boxplot(plot_data, False, '', patch_artist=True)

    for i in range(8):
        bplot['medians'][i].set_color('#000000')
        bplot['medians'][i].set_linewidth(0.5)

    ax.axvspan(4.5, 8.5, color='#e41a1c', alpha=0.04)

    bplot['boxes'][0].set_color(c1)
    bplot['boxes'][0].set_label('MLP')
    bplot['boxes'][1].set_color(c2)
    bplot['boxes'][1].set_label('MLP-PLR')
    bplot['boxes'][2].set_color(c3)
    bplot['boxes'][2].set_label('XGBoost')
    bplot['boxes'][3].set_color(c4)
    bplot['boxes'][3].set_label('TabR')
    bplot['boxes'][4].set_color(c1)
    bplot['boxes'][5].set_color(c2)
    bplot['boxes'][6].set_color(c3)
    bplot['boxes'][7].set_color(c4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.xticks([2.5, 6.5], ['Time Split', 'Random Split'])
    plt.tick_params(labelsize=16)
    ax.set_title(dataset_name[d], fontsize=18)
    if d not in ['homesite-insurance', 'ecom-offers', 'homecredit-default']:
        ax.set_ylabel(r'RMSE $\downarrow$', fontsize=18)
    else:
        ax.set_ylabel(r'AUC-ROC $\uparrow$', fontsize=18)

    if d == 'weather':
        plt.legend(loc='upper right', bbox_to_anchor=(2, 1.0), fontsize=16, edgecolor='#ffffff')


fig.subplots_adjust(wspace=0.3, hspace=0.3)
# .set_position()
shift = 0.2
p = fig.axes[-2].get_position()
p.x0 += shift
p.x1 += shift
fig.axes[-2].set_position(p)

shift = 0.26
p = fig.axes[-1].get_position()
p.x0 += shift
p.x1 += shift
fig.axes[-1].set_position(p)

plt.savefig('figure-id-ood.pdf', bbox_inches='tight')
plt.show()



