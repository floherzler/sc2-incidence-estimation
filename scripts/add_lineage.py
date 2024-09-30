import csv
import subprocess
from tqdm import tqdm

# Paths to your files
csv_file = "../data/france_sonar_output.csv"
db_path = "../data/project4.db"
output_fasta = "temp.fasta"  # Temporary FASTA file to hold restored sequence
num_rows = 1  # Number of rows to process

# Function to run CovSonar restore command for a given accession
def run_covsonar_restore(accession, db_path, output_fasta):
    restore_cmd = [
        "python", "../pipelines/covsonar/sonar.py",
        "restore", "--acc", accession,
        "--db", db_path
    ]

    # Open a file to write the restored FASTA sequence
    with open(output_fasta, "w") as fasta_file:
        try:
            subprocess.run(restore_cmd, stdout=fasta_file, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error restoring sequence for {accession}: {e}")

def run_covsonar_update(db_path, lineage_csv):
    update_cmd = [
        "python", "../pipelines/covsonar/sonar.py",
        "update", "--pangolin", lineage_csv,
        "--db", db_path,
    ]

    try:
        subprocess.run(update_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating lineage for {accession}: {e}")

# Function to run Pangolin on the given FASTA file
def run_pangolin(fasta_file):
    pangolin_cmd = ["pangolin", "-t", "8", fasta_file]
    try:
        result = subprocess.run(pangolin_cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running Pangolin: {e}")
        return None

# Process the first N rows of the CSV
with open(csv_file, mode="r") as csvfile:
    reader = csv.DictReader(csvfile)
    input_csv = "lineage_report.csv"
    output_csv = "pangolin.csv"
    # Loop through the first `num_rows` rows
    for row in tqdm(list(reader)[:num_rows]):
        accession = row["accession"]  # Adjust this field name if it's different in your CSV

        # Run CovSonar restore to get the FASTA sequence
        run_covsonar_restore(accession, db_path, output_fasta)

        # Run Pangolin on the restored FASTA sequence
        pangolin_output = run_pangolin(output_fasta)
        if pangolin_output:
            #print(f"Pangolin output for {accession}:\n{pangolin_output}")
            

            # Read the second row from the input CSV
            with open(input_csv, mode='r', newline='') as infile:
                reader = csv.reader(infile)
                header = next(reader)  # Skip the header row
                second_row = next(reader, None)  # Read the second row (if it exists)

            # If second row exists, append it to the output CSV
            if second_row:
                with open(output_csv, mode='a', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(second_row)
            run_covsonar_update(db_path, "lineage_report.csv")


# Optionally: Clean up the temporary FASTA file
# os.remove(output_fasta)
