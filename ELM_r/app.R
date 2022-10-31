#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(tidyverse)
library('shinycssloaders')
source("make_network.R")
source('run_python.R')

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Make Networks Shiny"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            fileInput('raw_tcp', "Upload TCP Data",
                      accept = c("text/csv", "text/comma-separated-values,text/plain", ".csv"),
                      buttonLabel = "Select File", placeholder = "Upload File"),
            sliderInput('plot_size', 'Set Plot Size',500,1000,700)),
        #     selectInput('color1',"Choose Color 1", c("lightblue,darkblue,red,yellow,green"),selected = "lightblue"),
        # selectInput('color2',"Choose Color 2", c("lightblue,darkblue,red,yellow,green"),selected = "red")),

        # Show a plot of the generated distribution
        mainPanel(
           uiOutput("vis_plot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
tcp_data <- reactive({
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
}



  
# Run the application 
shinyApp(ui = ui, server = server)
