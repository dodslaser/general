#!/bin/bash
## Small script that generates some folders to test 
## the delete by age script

## DEPENDENCIES (These should be found in $PATH)
## openssl

if  [ "$#" == 0 ]; then
    echo >&2 -e "Usage: genTestData.sh \n\t-n <num of months to generate> \n\t-s <start month: default:1> \n\t-t <samplesheet template file> \nt-d <num data folders> \n"
    exit 0
fi

#Default parameters
j=1
num_folds=3
start_month=1
template='/Users/anli/cgg/general/deleteOldSeqRuns/genTestData/sampleSheetTemplate.txt'
numdata=4

#An array with values to pull from randomly
PILIST=( \
    "SL" \
    "ES" \
    "CGG" \
    "JW" \
)

#Read in all flags
while getopts ":n:s:t:d:" opt; do
    case $opt in
        n)
            num_folds=$OPTARG
            ;;
        s)
            start_month=$OPTARG
            ;;
		t)
            template=$OPTARG
            ;;
		d)
            numdata=$OPTARG
            ;;
        \?)
            echo >&2 "Invalid option: -$OPTARG" >&2
			exit 1
            ;;
        :)
            echo >&2 "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

#Make a Demultiplex dir
mkdir Demultiplexdir

for ((i=1;i<=num_folds;i++)); do
	for day in 01 20 28; do
		#Make a run folder
		idnum=$(openssl rand -hex 5 | tr '[:lower:]' '[:upper:]')
		newdir="200${start_month}${day}_A00687_005${j}_$idnum"
		j=$(($j+1))
		mkdir $newdir
		if [ ! -f "${newdir}/SampleSheet.csv" ]; then
			cat $template > ${newdir}/SampleSheet.csv
		fi

		#Make a copy of the folder in a Demultiplex subdir
		mkdir Demultiplexdir/$newdir

		#Make some various folders in the run folder
		for f in Config Data InterOp Logs Recipe Thumbnail_Images; do
			mkdir ${newdir}/$f
		done

		#Make some files in the run folder
		for f in CopyComplete.txt RTA3.cfg RunINfo.xml RunParameters.xml SequenceComplete.txt; do
			touch ${newdir}/$f
		done

		#Generate a SampleSheet.csv file with samples
		for ((x=1;x<=numdata;x++)); do 
			ID=$(shuf -i 1000-9999 -n 1)
			#Get a random PI owner
			PI=${PILIST[ $(( RANDOM % ${#PILIST[@]} )) ] }
			#This line could be more dynamic
			line="DNA${ID},DNA${ID},,,A12,UDI0089,TATGCC,UDI0089,CTTAGTGT,XXX,${PI}_F_03_t_$ID"
			echo $line >> ${newdir}/SampleSheet.csv
		done

	#Set the newly made folders/files mtime to correct value
		find $newdir -exec touch -t 200${start_month}011200 {} +		
	done
	start_month=$(($start_month+1))
done
