#!/usr/bin/env python

"""
A script that looks in a specified location and
finds directories older than a specified number
of days, and removes the directory.
Will also first send out an email to the owner to warn
"""

#Import libraries
import os
import click

# Get arguments from the commandline
@click.command()
def main ():



if __name__ == '__main__':
    main()