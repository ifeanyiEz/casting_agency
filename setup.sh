#!/bin/bash

export SECRET="EzuFSNDCastingAgencyCapstoneProject"
export AUTH0_DOMAIN="ezufsndcap.us.auth0.com"
export API_AUDIENCE="http://localhost:5000"
export ALGORITHMS=['RS256']
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL="postgresql://ezugworie:E2u8w0r1e@localhost:5432/casting"
export EXCITED="true"
echo "setup.sh script executed successfully!"
