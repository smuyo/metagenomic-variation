

library('seqLogo')


file <- #Indicate file of which the sequence logo must be drawn
initial <- #Indicate initial position of the sequence logo
final <- #Indicate final position of the sequence logo

ali <- read.csv(file)
ali1 <- ali[c(initial,final),c(3:6)]
name <- gsub(".csv","",file)

proportion <- function(x){
  rs <- sum(x);
  return(x / rs);
}

pmw <- apply(ali1,1,proportion)
bad <- apply(pmw,MARGIN = 2, function(x) all(is.nan(x)))
pmw1 <- pmw[,!bad]
pmw1 <- makePWM(pmw1)
svg(filename = paste(name,'_logo.svg', sep = ''), width = 300)
plot.new()
seqLogo(pmw1,yfontsize = 8,ic.scale = FALSE)
dev.off()