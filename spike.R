# I have this code currently working with selenium-server-standalone-3.9.1.jar. It only seems to work with safari
# I tried running 'selenium-server-4.8.1.jar standalone --port 4444', and while this code connects it doesn't seem to do anything after and doesn't report errors

library(RSelenium)
remDr <- remoteDriver(
  remoteServerAddr = "localhost",
  port = 4444L,
  browserName = "safari"
)
remDr$errorDetails()
remDr$open()
remDr$getStatus()
remDr$navigate("http://www.google.com/ncr")



remDr$closeWindow()