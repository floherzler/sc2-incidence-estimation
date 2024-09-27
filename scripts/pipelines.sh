# mamba create env if not present
# mamba activate ~/envs/sonar
# query the covsonar database

# ../pipelines/covsonar/sonar.py match --db ../data/project4.db --date 2022-01-01:2022-07-01 > ../data/sonar_output.csv

# mamba deactivate
# mamba create env ginpipe
# use dev version of skdfa
# mamba activate GInPipe3

#france
#snakemake --snakefile ../pipelines/GInPipe/GInPipe --configfile ../pipelines/gin_config.yaml -d ../pipelines/gin_output --cores all
#germany
snakemake --snakefile ../pipelines/GInPipe/GInPipe --configfile ../pipelines/gin_config-germany.yaml -d ../pipelines/gin_output --cores all