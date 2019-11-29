rm(list = objects())
options(stringsAsFactors = FALSE,
	scipen = 200)
library(wrangleR)

library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
p <- getprofile(c("indx_con","cdt_bot_slack_api_token"),
				file = '.gel_config'
				  )
con <- dbConnect(drv,
              dbname = "ngis_genomicrecord_beta",
              host     = p$indx_con$host,
              port     = p$indx_con$port,
              user     = p$indx_con$user,
              password = p$indx_con$password)
 
#d <- dbGetQuery(con, 'select referral_human_readable_stored_id as participant_id from referral order by random() limit 10;')
d <- dbGetQuery(con, 'select participant_id from cdm.participant limit 10;')
cat(d$participant_id[1]) 
write.table(d, 'test-data.txt')

send_df_to_slack_as_file <- function(d, channel, api_token, filename = NA, comment = NA){
	require(knitr)
	require(slackr)
	slackr_setup(channel = channel, 
				api_token = api_token)
	fn <- tempfile()
	writeLines(kable(d, format = 'rst'), fn)
	slackr_upload(fn, title = filename, initial_comment = comment, channels = channel, api_token = api_token)
}

send_df_to_slack_as_file(d, 'simon-test', p$cdt_bot_slack_api_token, 'data', paste('this has been uploaded by Gitlab on', Sys.Date()))
