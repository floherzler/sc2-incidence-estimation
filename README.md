# SARS-CoV-2 Incidence Estimation
## Project 4 by Nora Wild and Florian Herzler

[Our Google Presentation](https://docs.google.com/presentation/d/15XBvj9IJd0EobPAPHM653WX2qZeGP24DdKORgymw1Sw/edit?usp=sharing)

![Workflow Diagram](results/plots/workFlo.svg)

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

mamba activate base # assume matplotlib, pandas, altair installed
cd scripts
python convert_tables.py
python histogram.py

# Get FASTA seq files with sonar --restore; ~30min for me
mamba activate covsonar
cd scripts
python get_fastas.py ../data/sonar_out_fr.csv france
python get_fastas.py ../data/sonar_out_sp.csv spain
cd ..

# Clone + activate pangolin env
cd pipelines
git clone git@github.com:cov-lineages/pangolin.git
mamba env create -n pangolin -f pangolin/environment.yml
mamba activate pangolin
cd pangolin
pip install .
cd ../scripts
python get_lineages.py france pangolin_fr.csv
python get_lineages.py spain pangolin_sp.csv
cd ..

# update Database + get csv
mamba activate covsonar
pipelines/covsonar/sonar.py update --db data/given/france/project4.db --csv results/pangolin_fr.csv --fields accession=accession lineage=lineage

pipelines/covsonar/sonar.py match --db data/given/france/project4.db --collection FRANCE --date 2022-01-01:2022-07-01 > results/lng_sonar_out_fr.csv


pipelines/covsonar/sonar.py update --db data/given/france/project4.db --csv results/pangolin_sp.csv --fields accession=accession lineage=lineage

pipelines/covsonar/sonar.py match --db data/given/france/project4.db --collection SPAIN --date 2022-01-01:2022-07-01 > results/lng_sonar_out_sp.csv

# plot lineages
mamba activate base
cd scripts
python plot_lineages.py ../results/lng_sonar_out_fr.csv lineages_fr.html
python plot_lineages.py ../results/lng_sonar_out_sp.csv lineages_sp.html

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
