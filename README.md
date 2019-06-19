# metagenomic-variation
Pipeline to calculate gene variation in metagenomic samples  
  
Usage: ./a.sh [-h] -i [SAMPLE] -g [GENE NAME] -o [OUTPUT FOLDER] -u [CUSTOM_UNIREF] [-s] [-t NUMBER OF THREADS] [-d]  

### Mandatory arguments:  
-i <input file>  
        File to be used as input. It should be a file in bam format containing the reads.  

-g <gene name>  
The name of the gene of which we want to check the variation.  
        If the name has more than one word the words should be separated by _  

-o <output folder>  
The folder where the output must be stored.  

-u <custom uniref>  
The folder containing the UniRef database.  


### Optional arguments:  
-h  
Display this help  

-s  
Bypass HUMAnN2. The results of HUMAnN2 must be in the folder indicated with the -o option  

-t  
        Number of threads to use. DEFAULT: 1  

-d  
        Setup the UniRef databse to be used in DIAMOND.  
        If it has not been configured before and HUMAnN2 must run, this option must be selected  
