library(tidyverse)
library(stringr)
library(visNetwork)
library(reticulate)
source_python(paste0(dirname(getwd()),'/Code_Files/stationerStandardization.ipynb'))

#TO-DO: ADD COMMENTS/SECTIONS

make_network <- function(x, physics,color1,color2) {
  

if (TRUE) {
df <- 
   read.csv(x,header = TRUE) %>% 
   filter(!str_detect(date,"-")) %>% 
   mutate(date = as.integer(date))
df2 <- 
  df %>% 
  mutate(Decade = cut(date, c(1580,1590,1600,1610,1620,1630,1640,1650,1660,1670,1680),labels = FALSE),
         Printer = ifelse(str_detect(publisher,"by"), 
                            str_extract(str_extract(publisher, "Printed by [A-Za-z]+ [A-Za-z]+"), "[A-Za-z]+ [A-Za-z]+$"), 
                            NA),
         Publisher = ifelse(str_detect(publisher,"to"), 
                            str_extract(str_extract(publisher, "to be sold by [A-Za-z]+ [A-Za-z]+"), "[A-Za-z]+ [A-Za-z]+$"), 
                            NA),
         Publisher = ifelse(str_detect(publisher,"for"), 
                            str_extract(str_extract(publisher, " for [A-Za-z]+ [A-Za-z]+"), "[A-Za-z]+ [A-Za-z]+$"), 
                            Publisher),
         Publisher = ifelse(str_detect(publisher,"to the"), 
                            str_extract(str_extract(publisher, "to the [A-Za-z]+ [A-Za-z]+ [A-Za-z]+"), "[A-Za-z]+ [A-Za-z]+ [A-Za-z]+$"), 
                            Publisher),
         Author = str_extract_all(author,"[A-Za-z]+, [A-Za-z]+"),
         Location = ifelse(str_detect(publisher,"at"), 
                        str_extract(publisher, "at .*$"), 
                        NA),
         Location2 = ifelse(!is.na(Location),str_extract(Location,"[A-Z].*$"),Location))
df_nodes_1 <<- 
  df2 %>% 
  select(Author,Publisher,Location,Location2,Decade) %>% 
  unnest(Author) %>% 
  unique() %>% 
  filter(!is.na(Publisher)) %>% 
  mutate(Publisher = ifelse(str_detect(Publisher,"Cambridge"), "Cambridge", Publisher),
         Author = paste0(str_extract(Author,"[A-Za-z]+"), " ", str_extract(Author,"[A-Za-z]+$"))) 

df_edges <- 
  df_nodes_1 %>% 
  select(Author,Publisher) %>% 
  unnest(Author) %>% 
  unique() %>% 
  filter(!is.na(Publisher)) %>% 
  rename(IN = Author, OUT = Publisher)

 df_nodes <- 
   rbind(df_nodes_1 %>% 
           select(Author, Location, Decade) %>% 
           rename(ID = Author)
           ,
         df_nodes_1 %>% 
           select(Publisher, Location, Decade) %>% 
           rename(ID = Publisher)) %>% 
   unique()
 
 # df_nodes <- 
 #   df_nodes_2 %>% 
 #   left_join(df_nodes_2 %>% 
 #               select(-Decade), by = "ID") %>% 
 #   filter(Location.x != Location.y)

author_lists <-
  as.list(df2 %>% 
            select(Author))

for (x in author_lists$Author) {
  current_list <- 
    x %>% 
    unique
  num <- length(current_list)
  for (y in c(1:num)) {
    if (num == 1) {
      break
    }
    for (z in c(y + 1:num)) {
      df_edges <- rbind(df_edges,c(current_list[y],current_list[z]))
    } 
  }
}

df_edges <- 
  df_edges %>% filter(!(is.na(OUT))) %>% 
  unique()

id <- 
    df_nodes %>% 
  pull(ID) %>% 
    unique()
 

nodes <- data.frame(id = id, label = id) %>% 
          mutate(group = ifelse(id %in% (df_nodes_1 %>% pull(Author)), "Author", "Publisher"))
edges <- data.frame(from = df_edges %>% pull(IN), to = df_edges %>% pull(OUT)) 

}

if (physics) {
return(visNetwork(nodes, edges, width = "100%", height = 700) %>% 
  visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE) %>% 
  visPhysics(enabled = TRUE) %>% 
    visGroups(groupname = "Author", color = "red") %>%
    visGroups(groupname = "Publisher", color = "lightblue") %>% 
    visLegend(width = 0.1, position = "right", main = "Group"))
} else {
  return(visNetwork(nodes, edges, width = "100%", height = 800) %>% 
    visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE) %>% 
    visPhysics(enabled = FALSE) %>% 
    visGroups(groupname = "Author", color = "red") %>%
    visGroups(groupname = "Publisher", color = "lightblue") %>% 
    visLegend(width = 0.1, position = "right", main = "Group"))
}
}

make_network("perkinsTCP.csv", TRUE)
make_network("charityTCP.csv", TRUE)
