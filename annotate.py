# python3 annotate.py test_vcf_data.txt

import csv
import logging
import requests
import vcfpy


ENSEMBL_SERVER = "https://rest.ensembl.org"


def get_consequence_terms(query_input: str):
    """Returns a list of consequence terms.

    Note: modified in part from code found here:
    https://rest.ensembl.org/documentation/info/vep_region_get

    """
    logging.info("Consequence terms query: ", query_input)
    ext = f"/vep/human/region/{query_input}?"

    r = requests.get(ENSEMBL_SERVER + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        logging.error("Status for query was: ", r.status_code[0])
        r.raise_for_status()

    # the results are a list of dicts that we can parse
    results = r.json()

    if not results:
        logging.warning("No consequence terms identified for query: %s", query_input)
        return None

    return results[0]['most_severe_consequence']


def get_gene_name(query_input: str):
    """Returns a gene name given an input query.

    Note: modified in part from code found here:
    https://rest.ensembl.org/documentation/info/overlap_region
    """
    logging.info("Gene name query: ", query_input)
    ext = f"/overlap/region/human/{query_input}?feature=gene;feature=transcript;feature=cds;feature=exon"

    r = requests.get(ENSEMBL_SERVER + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        logging.error("Status for query was: ", r.status_code[0])
        r.raise_for_status()

    # the results are a list of dicts that we can parse
    results = r.json()

    if not results:
        logging.warning("No gene names identified for query: %s", query_input)
        return None

    return results[0]['external_name']


# Open file, this will read in the header
reader = vcfpy.Reader.from_path('./data/small_test_vcf_data.txt')
line_count = 0

# The output will be a list of lines
# Build header and save to the output variable
header = ['#CHROM', 'POS', 'TC', 'TR', 'Most_Severe_Consequence', 'Gene_Name']
output = [header]

# read through the VCF file and print out info that we want
for record in reader:

    api_query_string_for_consequences = f"{record.CHROM}:{record.POS}-{record.POS}/{record.ALT[0].value}"

    most_severe_consequence = 'none_found'

    try:
        most_severe_consequence = get_consequence_terms(api_query_string_for_consequences)
    except Exception:
        # endpoint did not return a most severe consequence
        pass

    api_query_string_for_gene = f"{record.CHROM}:{record.POS}-{record.POS}"
    gene_name = 'none_found'

    try:
        gene_name = get_gene_name(api_query_string_for_gene)
    except Exception as err:
        # endpoint did not return a gene name
        pass

    line = [record.CHROM, record.POS, record.INFO['TC'], record.INFO['TR'], most_severe_consequence, gene_name]
    output = output + [line]

    line_count += 1

logging.info("Processed %i lines.", line_count)

# print(output)

# now we are done parsing the file, let's print the output to a CSV
with open('output.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(output)
