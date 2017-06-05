#!/usr/bin/env python
"""
Script for parsing the best hit reference from a mapping stage of multiple references.
"""

import csv
import sys

from Bio import SeqIO


class MissingFastaError(object):
    pass


def parse_best(mapping_results):
    """Parse a vcf for the best reference according to total read count."""
    with open(mapping_results) as inp:
        csv_info = csv.DictReader(inp, delimiter='\t')
        rows = [row for row in csv_info]

    best_mapped = max(rows, key=lambda x: int(x['Total read count']))
    return best_mapped


def fetch_best(best_mapped, fasta_path):
    """Fetch the SeqIO record for the best reference from references fasta file."""
    best_header = best_mapped['Name'].replace(' mapping', '')

    for record in SeqIO.parse(fasta_path, 'fasta'):
        if record.id == best_header:
            return record
    else:
        raise MissingFastaError('The sequence header was not found in the given fasta file.')


def write_output(best_record, output):
    """Write the SeqIO record for the best reference to file."""
    with open(output, 'w') as out:
        SeqIO.write(best_record, out, 'fasta')


def main():
    mapping_results, fasta_path, fasta_output = sys.argv[1]

    best_mapped = parse_best(mapping_results)
    best_record = fetch_best(best_mapped, fasta_path)
    write_output(best_record, fasta_output)


if __name__ == '__main__':
    main()
