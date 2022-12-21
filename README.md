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

# query the help documentation
python3.9 annotate.py -h
usage: annotate.py [-h] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input VCF file
  -o OUTPUT, --output OUTPUT
                        Name of the output CSV file

# run the program with a small input dataset
python3.9 annotate.py -i ./data/small_test_vcf_data.txt -o small_output.csv

# run the program with the large dataset that was provided
python3.9 annotate.py -i ./data/test_vcf_data.txt -o output.csv

# deactivate the virtualenv
deactivate
```

# Improvements we could make

1. There is probably a way to reduce the number of API calls we are making (maybe 
by querying the API with a larger genomic range?). This would likely speed up
the application because API calls can be slow.
2. We could add tests that will make our application more robust.
3. We could ship the application in a docker container, thus ensuring a 
more reproducible environment.





