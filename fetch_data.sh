# remove existing data directory if it exists
if [ -d './data' ]
then
    echo 'Overwrite previous data? (y/n) ?'
    read response
    if [ $response = 'y' ]
    then
    	rm -rf ./data
    else
        exit
    fi
fi

# make data dir
mkdir data
echo 'Creating data directory ... '
echo


######### Get data from European Center for Disease Prevention ################

# Global Cases
wget -O ./data/covid_19_cases_european.csv https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/ 

#####################################################################

######### Get data for India ################

# India Cases
wget -O ./data/state_daily_india.csv https://api.covid19india.org/csv/latest/state_wise_daily.csv	

#####################################################################


######### Get data for USA ################

# India Cases
wget -O ./data/state_daily_usa.csv https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv

#####################################################################

# create log of downloaded file timestamp in UTC
date -u > timestamp_data.log

echo
echo 'Data Download Complete'
echo
