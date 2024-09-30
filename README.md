# SARS-CoV-2 Incidence Estimation
## Project 4 by Nora Wild and Florian Herzler

```bash
# Download project4.db
# https://osf.io/uchtg -> data/given/france/project4.db
# Download reported cases for France
# https://osf.io/jptkw -> data//given/france/france_new_cases_2022_owid.csv

# Clone + activate covsonar env
cd pipelines
git clone https://github.com/rki-mf1/covsonar.git
mamba env create -n covsonar -f covsonar/sonar.env.yml
mamba activate covsonar
cd ..
# Query covSonar database -> csv
pipelines/covsonar/sonar.py match --db data/given/france/project4.db --collection FRANCE --date 2022-01-01:2022-07-01 > data/sonar_out_fr.csv
pipelines/covsonar/sonar.py match --db data/given/france/project4.db --collection SPAIN --date 2022-01-01:2022-07-01 > data/sonar_out_sp.csv
# got reported cases for spain from https://ourworldindata.org/coronavirus/country/spain

mamba activate base # assume matplotlib and pandas installed
python scripts/convert_tables.py
# TODO plot in new script
# TODO plot lineages + line chart reported cases
# TODO plot also for spain and germany

# Get FASTA seq files with sonar --restore; ~30min for me
mamba activate covsonar
cd scripts
python get_fastas.py
cd ..

# Clone + activate pangolin env
cd pipelines
git clone git@github.com:cov-lineages/pangolin.git
mamba env create -n pangolin -f pangolin/environment.yml
mamba activate pangolin
cd pangolin
pip install .
cd ../scripts
python get_lineages.py # Get all lineages
# TODO modify for all countries
cd ..

# update Database
mamba activate covsonar
pipelines/covsonar/sonar.py update --db data/given/france/project4.db --csv results/pangolin.csv --fields accession=accession lineage=lineage

# Clone + activate GInPipe env
cd pipelines
git clone git@github.com:KleistLab/GInPipe.git
mamba env create -f GInPipe/env/env.yml
mamba activate GInPipe3
cd GInPipe

# Run GInPipe for France, Germany, Spain
snakemake --snakefile GInPipe --configfile ../../gin_config_fr.yaml -d ../../results/gin_out_fr --cores all

snakemake --snakefile GInPipe --configfile ../../gin_config_de.yaml -d ../../results/gin_out_de --cores all

snakemake --snakefile GInPipe --configfile ../../gin_config_sp.yaml -d ../../results/gin_out_sp --cores all
```
