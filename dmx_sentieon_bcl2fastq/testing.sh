#!/bin/bash -l
#$ -cwd
#$ -S /bin/bash
#$ -pe mpi 40
#$ -q wgs.q
#$ -l excl=1

export SENTIEON_LICENSE=medair1.medair.lcl:8990
export SENTIEON_INSTALL_DIR=/apps/bio/software/Senteion/sentieon-genomics-201808.05

BCL_DIR=/seqstore/instruments/nextseq_500175_gc/190628_NB501037_0423_AHVHT7BGXB

OUTPUT_DIR=/seqstore/instruments/Testing/testing_sentieon_dmx/201808.03/190628_NB501037_0423_AHVHT7BGX_sentieon_v05

/apps/bio/software/bcl2fastq/2.20.0.422_source/bin/bcl2fastq --runfolder-dir $BCL_DIR -o $OUTPUT_DIR --fastq-compression-level 1 -r40 -p40 -w40 --barcode-mismatches 1 --min-log-level TRACE &>> $OUTPUT_DIR/logfile

#OUTPUT_DIR=/seqstore/instruments/Testing/testing_sentieon_dmx/201808.03/190628_NB501037_0423_AHVHT7BGX_bcl2fastq_2.20 
#/apps/bio/software/bcl2fastq/2.20/bin/bcl2fastq --runfolder-dir $BCL_DIR -o $OUTPUT_DIR --fastq-compression-level 1 -r40 -p40 -w40 --barcode-mismatches 1 --min-log-level TRACE &>> $OUTPUT_DIR/logfile

#OUTPUT_DIR=/seqstore/instruments/Testing/testing_sentieon_dmx/201808.03/190627_NB501037_0422_AHNCKFAFXY_bcl2fastq_2.20
