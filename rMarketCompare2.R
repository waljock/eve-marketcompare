library(readxl)
library(ggplot2)
library(plyr)

d <- read_xlsx("C:/Users/Walter/Documents/GitHub/eve-marketcompare/combined_data.xlsx")
d2 <-subset(d,(region == 'Catch'))
ct <-count(d2$type_id)
ct <- ct[order(ct$freq),]


#hist(d2$type_id)

hist(d2$average, breaks=10000)
#44138d2

catch <- subset(d, (type_id == 1319
                    ))

catch
pc <- ggplot(catch, aes(date, average)  )+
  geom_jitter(aes(color = region))
pc


