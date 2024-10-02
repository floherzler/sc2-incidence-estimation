import argparse
import pandas as pd
import altair as alt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', type=str, help='The name of the file to read')
    parser.add_argument('out_file', type=str, help='The name of the file to write')
    
    # use altair to plot columns 'lineage' versus 'date'
    # group by 'lineage' and display stacked bars for each day

    args = parser.parse_args()
    top_n = 5
    df = pd.read_csv(args.in_file)
    df['lin_simple'] = df['lineage'].str.split('.').str[:2].str.join('.').str.lower()
    # only keep top 5 lineages
    top_lineages = df['lin_simple'].value_counts().head(top_n).index
    df = df[df['lin_simple'].isin(top_lineages)]

    # use altair
    plot_total = alt.Chart(df).mark_area().encode(
        x='date:T',
        #y='count()',
        y=alt.Y('count()'), 
        color='lin_simple:N',
        tooltip=['date:T', 'count()', 'lin_simple:N']
    ).properties(
        title=f'Top {top_n} Lineages over time'
    )
    plot_total.save(f'../results/total_{args.out_file}')

    plot_perc = alt.Chart(df).mark_area().encode(
        x='date:T',
        y=alt.Y('count()', stack='normalize'),
        color='lin_simple:N',
        tooltip=['date:T', 'count()', 'lin_simple:N']
    ).properties(
        title=f'Top {top_n} Lineages over time (perc)'
    )
    plot_perc.save(f'../results/perc_{args.out_file}')
