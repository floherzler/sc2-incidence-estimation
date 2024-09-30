import os
import subprocess
import pandas as pd
import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(file):
    if file.endswith('.fasta'):
        name = file.split('.')[0]
        pangolin_cmd = ["pangolin", "-t", "8", "--analysis-mode", "fast", f"../data/fastas/{file}"]
        try:
            result = subprocess.run(pangolin_cmd, capture_output=True, text=True, check=True)
            data = pd.read_csv('lineage_report.csv')
            lineage = data['lineage'][0]
            with open('../results/pangolin.csv', 'a') as f:
                f.write(f"{name},{lineage}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error running Pangolin: {e}")

def main():
    # create ../data/pangolin.csv if it does not exist already
    if not os.path.exists('../results/pangolin.csv'):
        with open('../results/pangolin.csv', 'w') as f:
            f.write('accession,lineage\n')
    files = [file for file in os.listdir('../data/fastas') if file.endswith('.fasta')]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_file, file) for file in files]
        for future in tqdm.tqdm(as_completed(futures), total=len(futures)):
            future.result()

if __name__ == "__main__":
    main()