library(readxl)
library(ggplot2)
library(plyr)

d <- read_xlsx("C:/Users/Walter/Documents/GitHub/eve-marketcompare/combined_data.xlsx")
d$today <- Sys.Date()
d$datediff <- difftime(d$today,  d$date)
d <- subset(d,(datediff <= 30))
d <- d[-c(1,2)]
d <- subset(d, region == 'Catch')


dsorted <- d[order(d$region,d$type_id,d$date),]

#dCatch <- subset(dsorted, d$region == 'Catch')
dsorted$dolvol <- ((dsorted$average * dsorted$volume)/as.numeric(d$datediff))
hist(dsorted$dolvol,breaks=100)

d2 <- subset(dsorted, region == 'Catch')
hist(d2$dolvol,breaks=100)
hist(d2$volume,breaks=100)

write.csv(d2,'C:/Users/Walter/Documents/GitHub/eve-marketcompare/catchHist.csv')

d2$dd <- as.numeric(d2$datediff)

d3 <- d2[c(1,6,7,9,12)]
#by_cyl <- mtcars %>% group_by(cyl)

# by_type <- grouping(type_id)
# 
# 
# d3 %>% summarize()

# by_cyl %>% summarise(
#   disp = mean(disp),
#   hp = mean(hp)
# )


# pc <- ggplot(catch, aes(date, average)  )+
#   geom_jitter(aes(color = region))
# pc
# 
# 
