#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#set up packages and source code
require(shiny)
require(tidyverse)
require('shinycssloaders')
require(reticulate)
require(listviewer)
require(DT)
source("make_network.R")
#source('run_python.R')
use_condaenv('r-reticulate')
source_python('bibleMarginaliaNoMain.py')
source_python(paste0(dirname(getwd()),'/Code_Files/stationerStandardization.ipynb'))
source_python(paste0(dirname(getwd()),'/Code_Files/authors.py'))
# Define UI for application that draws a histogram
ui <- 
  fluidPage(

    # Application title
titlePanel("Early Modern London Shiny App"),
tags$head(
tags$style(HTML("
    @import url('https://fonts.googleapis.com/css2?family=Yusei+Magic&display=swap');
    h2 {
        font-family: 'Yusei Magic', sans-serif;
        background-color: #003087;
        color: white;
      }
    body"))),
    # Sidebar with a slider input for number of bins 
    tabsetPanel(
      tabPanel("Process TCP XMLs!",
               sidebarLayout(
                 sidebarPanel(
                   fileInput('xlm_dir', "Upload XML Directory",
                             buttonLabel = "Select XML Directory", placeholder = "Upload DIR"),
                   textInput('author_id', "Select your author", placeholder = "Input Author")
               ),
               mainPanel()
               )),
      tabPanel(
        "Network Visualiser",
    sidebarLayout(
        sidebarPanel(
            fileInput('raw_tcp', "Upload TCP Data",
                      accept = c("text/csv", "text/comma-separated-values,text/plain", ".csv"),
                      buttonLabel = "Select File", placeholder = "Upload File"),
            sliderInput('plot_size', 'Set Plot Size',500,1000,700)),
        # selectInput('color1',"Choose Color 1", c("lightblue,darkblue,red,yellow,green"),selected = "lightblue"),
        # selectInput('color2',"Choose Color 2", c("lightblue,darkblue,red,yellow,green"),selected = "red")),
        # Show a plot of the generated distribution
        mainPanel(
           uiOutput("vis_plot")
        )
      )
    ),
    tabPanel(
      "Sermon Visualizer",
      sidebarPanel(
        fileInput('raw_xml', "Upload XML Data",
                  accept = ".xml",
                  buttonLabel = "Select File", placeholder = "Upload File"),
    ),
    mainPanel(
      DTOutput('xml_table')
    )
  )
)
)
# Define server logic required to draw a histogram
server <- 
  function(input, output) {
  
tcp_data <- 
  reactive({
  req(input$raw_tcp)
  make_network(input$raw_tcp$datapath, physics = TRUE)
})

output$visualize_tcp <- 
  renderVisNetwork({
    req(input$raw_tcp)
    tcp_data()
  })

output$vis_plot <- 
  renderUI({visNetworkOutput('visualize_tcp',height = input$plot_size, width = input$plot_size) %>% 
      withSpinner(type = 4)})

xml_data <- 
  reactive({
    req(input$raw_xml)
    getMarginalia(input$raw_xml$datapath)
  })


xml_dir_processed <- 
  reactive({
    #req(input$xlm_dir)
    #req(input$author_id)
    print(input$xlm_dir$datapath)
    getAuthorTCPMetadata(input$xlm_dir$datapath,input$author_id,paste0(getwd(),"/csv_outputs"))
  })

# reshape_list <- function(list1) {
#   df_shaped = c()
#   count = 0
#   for (x in integer(length(list1)/5)) {
#     if ((count + 1)*5 <= length(list1)) {
#       df_shaped <- append(df_shaped,c(list1[count * 5 + 1:(count + 1)*5]))
#       print(df_shaped)}
#     else {
#       temp <- c(list1[count * 5 + 1:(count * 5 + 1) + (5 - (((count + 1)*5) - length(list1)))])
#       temp <- append(temp,rep(NA,(((count + 1)*5) - length(list1))))
#       df_shaped <- append(df_shaped,temp)
#     }
#     count <- count + 1
#   }
#   return(df_shaped)
# }

output$xml_table <- 
  renderDT({
    data.frame(unlist(strsplit(xml_data()[[1]],"''"))) %>% 
      rename("Biblical Marginalia" = 1)
  })
}



  
# Run the application 
shinyApp(ui = ui, server = server)
