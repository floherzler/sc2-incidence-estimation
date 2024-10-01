import os
import subprocess
import pandas as pd
import tqdm
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(in_dir, out_name, file):
    if file.endswith('.fasta'):
        id = file.split('.')[0]
        pangolin_cmd = ["pangolin", "-t", "8", "--analysis-mode", "fast", f"../data/fastas/{in_dir}/{file}"]
        try:
            result = subprocess.run(pangolin_cmd, capture_output=True, text=True, check=True)
            data = pd.read_csv('lineage_report.csv')
            lineage = data['lineage'][0]
            name = data['scorpio_call'][0]
            with open(f'../results/{out_name}', 'a') as f:
                f.write(f"{id},{lineage},{name}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error running Pangolin: {e}")

def main():
    # arg parser for filename and out_dir
    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir', type=str, help='The name of the dir to read fastas')
    parser.add_argument('out_file', type=str, help='The name of the output file')
    in_dir = parser.parse_args().in_dir
    out_file = parser.parse_args().out_file

    if not os.path.exists(f'../results/{out_file}'):
        with open(f'../results/{out_file}', 'w') as f:
            f.write('accession,lineage,scorpio_name\n')
    files = [file for file in os.listdir(f'../data/fastas/{in_dir}') if file.endswith('.fasta')]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_file, in_dir, out_file, file) for file in files]
        for future in tqdm.tqdm(as_completed(futures), total=len(futures)):
            future.result()

if __name__ == "__main__":
    main()