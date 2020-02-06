cat git*.csv gitsearch.*.out links.txt >mergelink.txt

sort mergelink.txt | uniq -u >links.txt

