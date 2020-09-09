#!/bin/bash -l
#$ -cwd
#$ -S /bin/bash
#$ -pe mpi 16
#$ -q production.q

export LD_PRELOAD="/usr/lib/petalink.so"
export PETASUITE_REFPATH="/seqstore/software/petagene/corpus:/opt/petagene/petasuite/species"

# A bamfile as input
INPUT=$1
# The directory where the expansionhunter output directory expansionhunt_${SAMPLE}_$DATESEC will be placed
OUTPUT=$2
# The WGS average coverage of the sample (can be found in the PDF-report or WGScoverage.tsv file)
GENCOV=$3
# The gender of the sample male/female (can be found in PDF-report too)
GENDER=$4
# The samplename, this will be included in the output directory 
SAMPLE=$5

export LC_ALL=C; unset LANGUAGE

run_exp()
{
REF=/medstore/External_References/hs37d5/hs37d5.fa
DATESEC=$(date +%s)
tmp=/tmp/expansionhunt_${SAMPLE}_$DATESEC
mkdir $tmp
mkdir $tmp/ref
cp ${REF}* $tmp/ref
REF=$tmp/ref/$(basename $REF)
#VARCAT=/apps/bio/software/ExpansionHunter/ExpansionHunter-v3.0.0-rc1-linux_x86_64/variant_catalog/variant_catalog_hg19.json
VARCAT=/apps/bio/software/ExpansionHunter/ExpansionHunter-v3.0.0-rc1-linux_x86_64/variant_catalog/variant_catalog_grch37.json
cp $VARCAT $tmp/ref
VARCAT=$tmp/ref/$(basename $VARCAT)
mkdir $tmp/bam
cp ${INPUT}* $tmp/bam/
cp $INPUT $tmp/bam/
BAM=$tmp/bam/$(basename $INPUT)
EXPH=/apps/bio/software/ExpansionHunter/ExpansionHunter-v3.0.0-rc1-linux_x86_64/bin/ExpansionHunter
$EXPH --reference $REF --read-length 151 --variant-catalog $VARCAT --verbose-logging --reads $BAM --genome-coverage $GENCOV --output-prefix $tmp/output --sex $GENDER
mv $tmp $OUTPUT
}
run_exp

