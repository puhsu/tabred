import polars as pl

data = pl.read_csv(
    '/Users/irubachev/academic_datasets_summary.csv',
    separator=';',
    n_rows=150,
)
data = data.drop_nulls(subset=' ').sort(' ')

data.columns[5] = 'Timesplit Needed'

for row in data.iter_rows():
    print(
        r'\subsection*{\href{' +
        row[3].replace('_', r'\_').replace('#', r'\#').strip() + '}' +
        '{' + row[0].replace('_', r'\_').replace('#', r'\#').strip() + '}}\n'
    )

    print(
        r'\textbf{Tags}: ',
        ', '.join(
            (['Leak'] if row[25] else []) +
            [data.columns[i] for i in range(8,13) if row[i]] +
            (['Timesplit Needed'] if row[5] else []) +
            (['Timesplit Possible'] if row[7] else [])
        ),
        '\n',
        sep='',
    )

    print(
        r'\textbf{\#Samples}:', row[1],
        r'\textbf{\#Features}:', row[2],
        r'\textbf{Year}:', row[13],
        '\n',
    )

    print(
        r'\textbf{Comments}:',
        row[4].replace('_', r'\_').replace('#', r'\#'),
        '\n',
    )
