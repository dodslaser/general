#!/usr/bin/env python

import xlsxwriter
import click
from pathlib import Path
import csv

@click.command()
@click.option('-i', '--infile', required=True,
              help='Comma separated list of input files')
@click.option('-o', '--outfile', required=True,
              help='Path to output xlsx file')
@click.option('-s', '--sheetnames',
              help='Comma separated list of names for worksheets, must be in same order as the files provided. '
                   'Default: Use filenames')
@click.option('-d', '--delimiter', 'delim', default=',',
              help='Delimiter to use, default:,')
@click.option('--strings2num', is_flag=True,
              help='Convert strings to numbers using float()?, default:False')
@click.option('--strings2form', is_flag=True,
              help='Convert strings to formulas?, default:False')
def main(infile, outfile, sheetnames, strings2num, strings2form, delim):
    #Set parameters for the workbook
    params = get_params(strings2num, strings2form)

    #Name the sheets to be used
    sheets = []
    if sheetnames:
        infile = infile.split(',')
        sheets = sheetnames.split(',')
        if len(sheets) != len(infile):
            print("** ERROR: Sheetname and filename lists are not of same length")
            exit(1)
    else:
        infile = infile.split(',')
        for file in infile:
            sheets.append(Path(file).stem)

    #Initialize the workbook
    workbook = xlsxwriter.Workbook(outfile, params)

    #Create worksheets for each input file
    for ws, file in enumerate(infile):
        worksheet = workbook.add_worksheet(sheets[ws])
        #Write each file to new worksheet
        with open(file, 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter=delim)
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