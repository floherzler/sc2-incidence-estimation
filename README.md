# SARS-CoV-2 Incidence Estimation
## Project 4 by Nora Wild and Florian Herzler

- covsonar database
- get sequences in timeframe for france
- TODO plot histogram of cases
    - TODO get lineages w/ pangolin 
- transform reported cases for each day

```bash
# Download project4.db
# https://osf.io/uchtg -> data/project4.db
# Download reported cases for France
# https://osf.io/jptkw -> data/france_new_cases_2022_owid.csv

python scripts/convert_tables.py

# Clone + activate covsonar env
cd pipelines
git clone https://github.com/rki-mf1/covsonar.git
mamba env create -n sonar -f covsonar/sonar.env.yml
mamba activate sonar
cd ..
# Query covSonar database -> csv
pipelines/covsonar/sonar.py match --db data/project4.db --collection FRANCE --date 2022-01-01:2022-07-01 > data/sonar_out_fr.csv
pipelines/covsonar/sonar.py match --db data/project4.db --collection SPAIN --date 2022-01-01:2022-07-01 > data/sonar_out_sp.csv
# Get FASTA seq files with sonar --restore; ~30min for me
python scripts/get_fastas.py

# Clone + activate pangolin env
cd pipelines
git clone git@github.com:cov-lineages/pangolin.git
mamba env create -n pangolin -f pangolin/environment.yml
mamba activate pangolin
cd pangolin
pip install .
cd ..
# Get all lineages
python scripts/get_lineages.py

# update Database
pipelines/covsonar/sonar.py update --db data/project4.db --csv results/pangolin.csv --fields acession=accesion lineage=lineage

# Clone + activate GInPipe env
cd pipelines
git clone git@github.com:KleistLab/GInPipe.git
mamba env create -f GInPipe/env/env.yml
mamba activate GInPipe3

# Run GInPipe for France, Germany, Spain
snakemake --snakefile pipelines/GInPipe/GInPipe --configfile pipelines/gin_config_fr.yaml -d ../results/gin_out_fr --cores all

snakemake --snakefile pipelines/GInPipe/GInPipe --configfile pipelines/gin_config_de.yaml -d ../results/gin_out_de --cores all

snakemake --snakefile pipelines/GInPipe/GInPipe --configfile pipelines/gin_config_sp.yaml -d ../results/gin_out_sp --cores all
cd ..
```
