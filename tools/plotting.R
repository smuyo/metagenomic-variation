#This script maked the variation plots of all the csv files 
#produced by the pipeline contained in a folder

library('ggplot2')
library('gridExtra')
library('grid')


fileli <- list.files()
fileli1 <- gsub(".csv","",fileli)

for (which in c(1:length(fileli1))) {
ali <- read.csv(fileli[which])
ali1 <- ali[,c(3:6)]
if (nrow(ali1) > 0) {
  
  ali$Coverage <- ali$A+ali$C+ali$G+ali$T
  plotobj <- ggplot(ali, aes(Nucleotide, Variation,)) +
    geom_line() +
    labs(title = fileli[which]) +
    ylim(0,1) +
    ylab('Mutation rate') +
    theme_light()
  
  plotobj2 <- ggplot(ali, aes(Nucleotide, Coverage)) +
    geom_line() +
    scale_y_reverse() +
    scale_x_continuous(labels = NULL, position = 'top') +
    xlab(NULL) +
    ylab('Read Depth') +
    theme_light()
  svg(filename = paste(fileli1[which],'.svg', sep = ''))
  grid.newpage()
  grid.draw(rbind(ggplotGrob(plotobj), ggplotGrob(plotobj2), size = "first"))
  dev.off()
  }
}

