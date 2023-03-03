# holds api calls we need for our testing
require(data.table)
# known api needs:
# - delete dataverse

#Currently this is programmed to read from a secret_table file located at a fixed directory
#TODO: This needs to be made dynamic once I understand how to do this better in rstudio
dframe <- read.table(file='/Users/madunlap/Documents/GitHub/secret_table.txt',header=FALSE,
                     sep='=',col.names=c('key','value'))
print(dframe)
dtable <- data.table(dframe,key='key')
print(dtable)
print(dtable["DATAVERSE_API_TOKEN"]$value)
print(dtable["DATAVERSE_SERVER_URL"]$value)