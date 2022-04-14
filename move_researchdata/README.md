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

There is also a wrapper script for finding new demultiplex dirs of sequencing runs,and moving any research data in it.
This currently looks in the 2 novaseq folders as well as the nextseq folder.
If there were any samples transferred, an e-mail is sent to the lab with information that data has been moved (cc to cgg-logs).
The recipients of both error and success e-mails can be configured in the wrapper_config.yaml file.

The wrapper is executed via root users crontab on medair and is set to run once per day at 16:00.

## Usage, wrapper
```
$ sudo su
$ module load miniconda/4.8.3
$ source activate move_research
$ python3 move_researchdata/wrapper.py
```