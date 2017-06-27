#!/usr/bin/env python

import sys
import glob
import csv
import os
import subprocess
from tabulate import tabulate


class AbnormalInputError(object):
    pass


class Context():
    def __init__(self, txt_output, csv_output, svg_output):
        self.txt_output = txt_output
        self.csv_output = csv_output
        self.svg_output = svg_output

        self.exported_path = '/medstore/CLC_Import_Export/Jens_Werling/temporary_files/dist_matrix'

        self.dummy_txt = f'{self.exported_path}/dummy.txt'
        self.dummy_csv = f'{self.exported_path}/dummy.cesv'
        self.dummy_svg = f'{self.exported_path}/dummy.svg'
        self.exported_files = self.get_exported_files()
        #self.exported_files_pretty = [f.split(' ')[0]+'.csv' for f in self.exported_files]

    def get_exported_files(self):
        """Read and clean file names."""
        raw = glob.glob(f'{self.exported_path}/*.csv')
        return raw

    def paths_for_clc(self):
        subprocess.run(['mv', self.dummy_txt, self.txt_output])
        subprocess.run(['mv', self.dummy_csv, self.csv_output])
        subprocess.run(['mv', self.dummy_svg, self.svg_output])

    def cleanup(self):
        """Remove temporary files and dirs"""
        for f in os.listdir(self.exported_path):
            print(os.path.join(self.exported_path, f))
            #os.remove(os.path.join(self.exported_path, f))


def collect_csv_info(ctx):
    """Read variant call vcf and structure info."""
    csv_info = []

    for f in ctx.exported_files:
        #name = os.path.basename(f).replace('.csv', '')
        name = os.path.basename(f).split(' ')[0]
        rows = []
        with open(f, 'r') as csv_file:
            csv_rd = csv.DictReader(csv_file, delimiter=',')
            for row in csv_rd:
                if row['Reference allele'] == 'No' and row['Zygosity'] == 'Homozygous':
                    rows.append((row['Chromosome'], row['Region'], row['Allele']))
        csv_info.append((name, rows))

    return tuple(csv_info)


def pairwise_compare(csv_info):
    final_distances = []

    for ref_pair in csv_info:
        ref_name, ref_info = ref_pair
        pair_distances = [ref_name]

        for comp_pair in csv_info:
            comp_name, comp_info = comp_pair
            set_intersect = set(ref_info) ^ set(comp_info)

            pair_distances.append(len(set_intersect))
        final_distances.append(pair_distances)
    return final_distances


def make_table(ctx, distances):
    headers = [os.path.basename(f).split(' ')[0] for f in ctx.exported_files]

    with open(ctx.dummy_txt, 'w') as out:
        print(distances)
        print(tabulate(distances, headers=headers, tablefmt='fancy_grid'), file=out)


def make_dummy(ctx):
    with open(ctx.dummy_csv, 'w') as bla, open(ctx.dummy_svg, 'w') as ble:
        print('hello', file=bla)
        print('there', file=ble)


def main(arguments):
    _, txt_output, csv_output, svg_output = arguments
    ctx = Context(txt_output, csv_output, svg_output)

    csv_info = collect_csv_info(ctx)
    distances = pairwise_compare(csv_info)
    make_dummy(ctx)
    make_table(ctx, distances)

    ctx.paths_for_clc()
    ctx.cleanup()


print(sys.argv[1:])
main(sys.argv[1:])
#main(*sys.argv[1:])
