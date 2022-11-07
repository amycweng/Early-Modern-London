library(tidyverse)
library(stringr)
library(reticulate)
use_condaenv('r-reticulate')
source_python('bibleMarginaliaNoMain.py')

convert_xml <- function(filepaths) {
  for (x in list.files(filepaths)) {
  getMarginalia(x)
  }
}

#output <- getMarginalia(paste0(dirname(getwd()),'/Sample_XML/A01529.P4.xml'))

#print(output[1])
#print(output[2])
