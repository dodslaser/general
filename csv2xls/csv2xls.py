#!/usr/bin/env python

import xlsxwriter
import click
from pathlib import Path
import csv

@click.command()
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--outfile', required=True,
              help='Path to output xlsx file')
@click.option('-s', '--sheetnames',
              help='Comma separated list of names for worksheets, must be in same order as the files provided. '
                   'Default: Use filenames')
@click.option('--tsv', is_flag=True,
              help='Input is a tab separated file')
@click.option('--strings2num', is_flag=True,
              help='Convert strings to numbers using float()?, default:False')
@click.option('--strings2form', is_flag=True,
              help='Convert strings to formulas?, default:False')
def main(files, outfile, sheetnames, strings2num, strings2form, tsv):
    #Set parameters for the workbook
    params = get_params(strings2num, strings2form)

    #Name the sheets to be used
    infile = list(files)
    sheets = []
    if sheetnames:
        sheets = sheetnames.split(',')
        if len(sheets) != len(infile):
            print("Error: Sheetname and filename lists are not of same length")
            exit(1)
    else:
        for file in infile:
            sheets.append(Path(file).stem)

    #Initialize the workbook
    workbook = xlsxwriter.Workbook(outfile, params)

    #Create worksheets for each input file
    for ws, file in enumerate(infile):
        worksheet = workbook.add_worksheet(sheets[ws])
        #Write each file to new worksheet
        with open(file, 'r', encoding='utf8') as f:
            if tsv:
                reader = csv.reader(f, delimiter='\t')
            else:
                reader = csv.reader(f, delimiter=',')
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)

    #Close the workbook
    workbook.close()

def get_params(strings2num, strings2form):
    params = {'constant_memory': True}
    if strings2num:
        params['strings_to_numbers'] = True
    if strings2form:
        params['strings_to_formulas'] = True

    return params

if __name__ == '__main__':
    main()
