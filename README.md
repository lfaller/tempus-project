# Tempus Project

# Description

The program extracts the following fields from the VCF file:

1. `TC` which is the `Total coverage at this locus`
2. `TR` which is the `Total number of reads containing this variant`

Based on the chromosome number and the variant position, it will also query 
the Ensembl Rest API for the consequence terms and the gene names.

The output will be saved to a CSV file called `output.csv`.


# Running the program

Clone this git repo. Then...

```bash
# create a virtual env
python3.9 -m venv my_env

# activate it
source my_env/bin/activate

# install the packages
pip install -r requirements_dev.txt

python3.9 annotate.py
```






