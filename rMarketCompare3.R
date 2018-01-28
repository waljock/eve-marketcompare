library(readxl)
library(ggplot2)
library(plyr)
library(data.table)
library(dplyr)


d <- read.csv("C:/Users/Walter/Documents/GitHub/eve-marketcompare/combined_data.csv")
types <- read_xls("C:/Users/Walter/Documents/GitHub/eve-marketcompare/InvTypes.xls")

types <- types[c(1,3,5)]

d$today <- Sys.Date()
d$datediff <- as.numeric(difftime(d$today,  d$date))
d <- subset(d,(datediff <= 30) & (average <=7500000) & (volume <=80))
d <- d[-c(1,2)]
c <- subset(d, region == 'Catch')
j <- subset(d, region == 'Jita')


dsortedc <- c[order(c$region,c$type_id,c$date),]
dsortedj <- j[order(j$region,j$type_id,j$date),]

#dCatch <- subset(dsorted, d$region == 'Catch')
dsortedc$dolvol <- ((dsortedc$average * dsortedc$volume)/(dsortedc$datediff))
dsortedj$dolvol <- ((dsortedj$average * dsortedj$volume)/(dsortedj$datediff))

d2c <- subset(dsortedc, region == 'Catch')
d2j <- subset(dsortedj, region == 'Jita')
hist(d2c$dolvol,breaks=100)
hist(d2j$volume,breaks=100)



d2c$dd <- as.numeric(d2c$datediff)
d2j$dd <- as.numeric(d2j$datediff)

d3c <- d2c[c(1,6,7,12)]
d3j <- d2j[c(1,6,7,12)]

cat <- d3c %>%
  select (type_id, volume, average, dd) %>%
  group_by(type_id) %>%
  summarise(average=mean(average), dd=mean(dd), volume = mean(volume))

jit <- d3j %>%
  select (type_id, volume, average, dd) %>%
  group_by(type_id) %>%
  summarise(average=mean(average), dd=mean(dd), volume = mean(volume))

plot(cat$average, cat$volume)
plot(jit$average, jit$volume)

s <- merge(cat, jit, by='type_id')

s$profit <- s$average.x - s$average.y
s$margin <- s$average.x/s$average.y

fin <- merge(s, types, by.x='type_id', by.y='TYPEID')

write.csv(fin,'C:/Users/Walter/Documents/GitHub/eve-marketcompare/finfin.csv')



# pc <- ggplot(catch, aes(date, average)  )+
#   geom_jitter(aes(color = region))
# pc
# 
# 
