# ddrad_scripts  

**Random scripts for dealing with ddRAD data, including output from pyRAD**  

## snps2phylip.py - converts a .snps file from pyRAD to Phylip format  

Usage:  
`snps2phylip -f [input.snps] -o [output.phy; optional, default="out.phy"]`  

## getbadpyrad.py - Writes samples with high missing data from pyRAD .stats file to CSV so they can be input into a pyRAD params file

Usage:  
`getbadpyrad.py -f [input.stats] -o [output_filename] -p [minimum proportion of loci for inclusion; float]`  

I.e., -p 0.15 excludes samples with more than 85% missing data  

## filterUninformative.py - Uses .log file from IQ-TREE to blacklist uninformative loci from a directory of loci files.  

Usage:  
`filterUninformative -l [input.log (must be in working directory)] -d [path/to/directoryWithLociFiles/ (must be subdirectory)]`  

Optional arguments: 
-b [/path/to/blacklistDIR]  
-h Displays help menu

The log file must be in the current working directory, and the loci directory must be a subdirectory within the working directory.  

## popmap2exDFOIL.py  

### Dependencies  
Python3  
pandas  
numpy  

### General Instructions  
Takes two-column tab-separated map files to make the mysampleinfo.txt file used in the [ExDFOIL pipeline](https://github.com/SheaML/ExDFOIL.git)  

Each map file must have two columns: One with individual IDs, and another with either popIDs, batch#, speciesID, or subspeciesID. The map files should not contain a header. If you want to include all five columns in the output, five files need to be specified. The map file columns should not contain spaces.  

### Example Files  

Example popmap file:  

```
sample1\tpop1
sample2\tpop1
sample3\tpop2
sample4\tpop2
```

Example speciesID file:  
```
sample1\tGorilla_gorilla
sample2\tGorilla_gorilla
sample3\tPan_troglodytes
sample4\tPan_troglodytes
```  

At least one map file is required. Only the ones the user specify as commmand-line arguments will be included in the output file.  

### Example Output:  

```
Individual batch popID speciesID subspeciesID
oberon10_JJW683p1 1 oberon10 oberon oberon_black
oberon10_JJW684p1 1 oberon10 oberon oberon_black
oberon10_JJW685 2 oberon10 oberon oberon_black
```   

### Usage and Options:  
```./popmap2exDFOIL.py -p [POPMAP_FILENAME] [optional_arguments]  

Required arguments:  
-p [POPMAP_FILENAME]  Specifies popmap filename  

Optional arguments:  
-b [BATCH_FILENAME]  Specifies batch filename  
-S [SPECIES_FILENAME]  Specifies speciesID filename  
-s [SUBSPECIES_FILENAME]  specifies subspeciesID filename  
-o [OUTFILE]  Specifies output filename. Default = "mysampleinfo.txt"  
-h Displays help menu
```  


