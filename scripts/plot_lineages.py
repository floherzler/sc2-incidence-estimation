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
    df = pd.read_csv(args.in_file)
    df['lineage_simplified'] = df['lineage'].str.split('.').str[:1].str.join('.').str.lower()

    print(df.head())
    # use altair
    plot = alt.Chart(df).mark_area().encode(
        x='date:T',
        #y='count()',
        y=alt.Y('count()', stack='normalize', axis=alt.Axis(format='%')), 
        color='lineage_simplified:N',
        tooltip=['date:T', 'count()', 'lineage_simplified:N']
    ).properties(
        title='Lineages over time'
    )
    plot.save(f'../results/{args.out_file}')
