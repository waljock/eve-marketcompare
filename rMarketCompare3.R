library(readxl)
library(ggplot2)
library(plyr)
library(data.table)
library(dplyr)

d <- read_xlsx("C:/Users/Walter/Documents/GitHub/eve-marketcompare/combined_data.xlsx")
d$today <- Sys.Date()
d$datediff <- as.numeric(difftime(d$today,  d$date))
d <- subset(d,(datediff <= 30) & (average <=7500000) & (volume <=80))
d <- d[-c(1,2)]
c <- subset(d, region == 'Catch')
j <- subset(d, region == 'Jita')


dsorted <- c[order(c$region,c$type_id,c$date),]
dsortedc <- j[order(j$region,j$type_id,j$date),]

#dCatch <- subset(dsorted, d$region == 'Catch')
dsorted$dolvol <- ((dsorted$average * dsorted$volume)/(dsorted$datediff))
hist(dsorted$dolvol,breaks=100)

d2 <- subset(dsorted, region == 'Catch')
hist(d2$dolvol,breaks=100)
hist(d2$volume,breaks=100)

write.csv(d2,'C:/Users/Walter/Documents/GitHub/eve-marketcompare/catchHist.csv')

d2$dd <- as.numeric(d2$datediff)

d3 <- d2[c(1,6,7,12)]

cars <- d3 %>%
  select (type_id, volume, average, dd) %>%
  group_by(type_id) %>%
  summarise(average=mean(average), dd=mean(dd), volume = mean(volume))

plot(cars$average, cars$volume)






# pc <- ggplot(catch, aes(date, average)  )+
#   geom_jitter(aes(color = region))
# pc
# 
# 
