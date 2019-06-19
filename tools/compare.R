library('ggplot2')
library('gridExtra')
library('grid')

file1 <- "" #Specify file 1
name1 <- "" #Specify name of sample 1

file2 <- "" #Specify file 2
name2 <- "" #Specify name of sample 2

reference <- "" #Specify reference name

vari1 <- read.csv(file1)
vari2 <- read.csv(file2)

plotobj <- ggplot(vari1, aes(Nucleotide, Variation,)) +
  geom_line() +
  labs(title = paste(paste(name1,name2, sep = " + "), reference, sep = ": ")) +
  ylim(0,1) +
  ylab('Mutation rate') +
  theme_light()

plotobj2 <- ggplot(vari2, aes(Nucleotide, Variation,)) +
  geom_line() +
  ylim(0,1) +
  ylab('Mutation rate') +
  theme_light()
svg(filename = "combine.svg")
grid.newpage()
grid.draw(rbind(ggplotGrob(plotobj), ggplotGrob(plotobj2), size = "first"))
dev.off()

