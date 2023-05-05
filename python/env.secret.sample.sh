export DATAVERSE_SERVER_URL=
export DATAVERSE_USERNAME_FOR_PERM_TEST=
export DATAVERSE_TEST_USER_USERNAME=

# For built in login testing
export DATAVERSE_TEST_USER_PASSWORD_BUILTIN=

# For sso login testing
export DATAVERSE_SSO_OPTION_VALUE=

#The tests will make a subfolder named "seleniumdownloads" during testing and then delete it at the end
export DOWNLOAD_PARENT_DIR=

#Increment this to add a fixed additional wait to all sleep statements. Useful for when a server is being slow etc.
export EXTRA_WAIT=0