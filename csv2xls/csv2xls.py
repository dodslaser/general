#!/usr/bin/env python

import xlsxwriter
import click
from pathlib import Path

@click.command()
@click.option('-i', '--infile', required=True,
              help='Comma separated list of input files')
@click.option('-o', '--outfile', required=True,
              help='Path to output xlsx file')
@click.option('-s', '--sheetnames',
              help='Comma separated list of names for worksheets, must be in same order as the files provided. '
                   'Default: Use filenames')
@click.option('-d', '--delimiter', default=',',
              help='Delimiter to use, default:,')
@click.option('--strings2num', is_flag=True,
              help='Convert strings to numbers using float()?, default:False')
@click.option('--strings2form', is_flag=True,
              help='Convert strings to formulas?, default:False')
def main(infile, outfile, sheetnames, delimiter, strings2num, strings2form):
    #Set parameters for the workbook
    params = get_params(strings2num, strings2form)

    #Name the sheets to be used
    if sheetnames:
        infile = infile.split(',')
        sheetnames = sheetnames.split(',')
        if len(sheetnames) != len(infile):
            print("** ERROR: Sheetname and filename lists are not of same length")
            exit(1)
    else:
        sheetnames = [Path(infile).stem]

    #print(sheetnames)

    #Initialize the workbook
    workbook = xlsxwriter.Workbook(outfile, params)

    #Create worksheets for each input file
    for ws in sheetnames:
        worksheet = workbook.add_worksheet(ws)
        worksheet.write('A2', 'Hello World')
        worksheet.write('A3', '15.5')

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