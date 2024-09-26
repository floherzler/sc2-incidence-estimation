# mamba create env if not present
# mamba activate covsonar
# query the covsonar database

../pipelines/covsonar/sonar.py match --db ../data/project4.db --date 2022-01-01:2022-07-01 > ../data/sonar_output.csv

# mamba deactivate