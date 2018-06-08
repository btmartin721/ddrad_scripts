# ddrad_scripts  

**Random scripts for dealing with ddRAD data, including output from pyRAD**  

## snps2phylip.py - converts a .snps file from pyRAD to Phylip format  

Usage:  
`snps2phylip -f [input.snps] -o [output.phy; optional, default="out.phy"]`  

## getbadpyrad.py - Writes samples with high missing data from pyRAD .stats file to CSV so they can be input into
 a pyRAD params file

Usage:  
`getbadpyrad.py -f [input.stats] -o [output_filename] -p [minimum proportion of loci for inclusion; float]`  

I.e., -p 0.15 excludes samples with more than 85% missing data  


