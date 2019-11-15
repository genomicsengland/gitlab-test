rm(list = objects())
options(stringsAsFactors = FALSE,
	scipen = 200)
library(wrangleR)

library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
p <- getprofile(
				"indx_con",
				file = '.gel_config'
				  )
con <- dbConnect(drv,
              dbname = "metrics",
              host     = p$host,
              port     = p$port,
              user     = p$user,
              password = p$password)
 
d <- dbGetQuery(con, 'select participant_id from consent_reading.participant order by random() limit 10;')
cat(d$participant_id[1]) 
write.table(d, 'test-data.txt')
