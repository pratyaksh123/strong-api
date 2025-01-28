#!/bin/bash

# Export environment variables to a file so cron can access them
printenv | grep -v "no_proxy" > /etc/environment

# Start the given command
exec "$@"