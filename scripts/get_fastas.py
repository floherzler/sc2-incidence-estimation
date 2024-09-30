import pandas as pd
import subprocess
import os
import tqdm
ids = pd.read_csv('../data/sonar_out_fr.csv', header=1)
# keep only first column
ids = ids.iloc[:,0]
for id in tqdm.tqdm(ids):
    # Ensure the directory exists
    os.makedirs('../data/fastas', exist_ok=True)
    with open(f'../data/fastas/{id}.fasta', 'x') as output_file:
        subprocess.run(['../pipelines/covsonar/sonar.py', 'restore', '--acc', id, '--db', '../data/given/france/project4.db'], stdout=output_file)
