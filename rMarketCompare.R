library(readxl)
library(ggplot2)
library(plyr)

d <- read_xlsx("C:/Users/HMA03468/Documents/GitHub/eve-marketcompare/combined_data.xlsx")
d2 <-subset(d,(region == 'Catch'))
count(d2$type_id)

#hist(d2$type_id)

hist(d2$average, breaks=10000)
#44138d2

catch <- subset(d, (type_id == 43894))

catch
pc <- ggplot(catch, aes(date, average)  )+
  geom_jitter(aes(color = region))
pc


