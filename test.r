rm(list = objects())
options(stringsAsFactors = FALSE,
	scipen = 200)
library(wrangleR)

library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
p <- getprofile(
				"mis_con",
				file = '.gel_config'
				  )
con <- dbConnect(drv,
             dbname = "gel_mi",
             host     = p$host,
             port     = p$port,
             user     = p$user,
             password = p$password)

d <- dbGetQuery(con, 'select participant_id from cdm.vw_participant_level_data limit 10;')
cat(d$participant_id[1])
