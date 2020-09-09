#!/bin/bash -l


#for vcf in $(find -name "output.vcf" | grep DNA62222); 
#grep -e "NA12878_1d" -e "NA12877_robot") ;

extract_stats()
{
#statspath=/medstore/Development/WGS_validation/expansionhunter_results/extracted_stats
#filepath=$statspath/FMR1_stats
#sample=$(basename $(dirname $vcf) | cut -d"_" -f2)
#       filepath=$(echo "$statspath/$(basename $(dirname $vcf) | cut -d"_" -f2)")
#    if [ -f "$filepath" ];
#    then
#        continue
#    fi

while read row
do
    if [ ! -z "$(echo $row | grep ^#)" ];
    then
        continue
    fi
    if [ ! -z "$(echo $row | grep 'REPID=HTT')" ];
    then
        continue
    fi

    part1=$(echo "$row" | cut -f1,2,5)    
    part2=$(echo "$row" | cut -f8 | cut -d";" -f1,2,4,5 | sed 's/;/\t/g')
    part3=$(echo "$row" | cut -f10)
    stats=$(echo -e "$part1\t$part2\t$part3")
    #if [ ! -z "$(echo "$stats" | grep "REPID=FMR1_X")" ];
    #then
    echo -e "$stats" >> ${vcf}.tsv
# >> $filepath
    #fi
done<$vcf
}

vcf=$(echo "$1")
echo -e "Chrom\tStart\t# RepeatUnits\tEndPos\t# RepeatUnits in Ref\tRepeatUnit\tRepeatIdentifier\tStats" >> ${vcf}.tsv
extract_stats $vcf
echo "$(date)" >> ${vcf}.tsv
