library(askpass)

get_dv_username_password <- function() {
  username <<- askpass("Username for builtin account")
  password <<- askpass("Password for builtin account")
}