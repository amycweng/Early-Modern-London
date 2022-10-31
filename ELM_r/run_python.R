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


