# linkFastq

This script was made as a quick and dirty solution for copying fastq files to a place where Carola Oldfors could reach them.

The script looks in a samplesheet from a novaseq run, and finds samples belonging to 'PAT'. Then makes a symlink over to whatever destination. The destionation should be a webfolder belonging to pathology.

### Usage:
```
$ ./linkFastqs.py \
  --demultiplexdir /seqstore/instruments/novaseq_687_gc/Demultiplexdir/210122_A00687_0115_AHGVJYDSXY \
  --outdir /seqstore/webfolders/wgs/patologi_muskel/fastq
```
