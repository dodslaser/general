# Move researchdata
This script takes a demultiplex directory as input and looks for any
samples belonging to reseaarch projects in the samplesheet.

If any are found, it copies the fastq and fastqc (if they exists) to the remote outbox.
One has to run this script as root since the sFTP chroot jails on /seqstore/remote/outbox needs 
to have root permissions set. 

The script uses the python libraries sample-sheet and click, and needs an environment with
these two. A simple environment with only these exists called 'move_research'.

### Usage, stand-alone
```
$ sudo su
$ module load miniconda/4.8.3
$ source activate move_research
$ python3 move_researchdata/move_researchdata.py -d /path/to/demultiplexdir/of/run
```

There is also a wrapper script for finding new demultiplex dirs of sequencing runs,a nd moving any research data in it.
This currently looks in the 2 novaseq folders as well as the nextseq folder.

## Usage, wrapper
```
$ sudo su
$ module load miniconda/4.8.3
$ source activate move_research
$ python3 move_researchdata/wrapper.py
```