#!/usr/bin/env python

import sys
import re
import getopt
import ftplib
from ftplib import FTP
import pandas as pd
import gzip
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists


def fetch_data_via_ftp():
    ftp = FTP('ftp.nass.usda.gov')
    ftp.login()
    ftp.cwd('quickstats')

    files = []

    try:
        files = ftp.nlst()
    except ftplib.error_perm, resp:
        if str(resp) == "550 No files found":
            print "No files in this directory"
        else:
            raise

    crops_file = [f for f in files if re.match('^qs.crops_', f)][0]

    ftp.retrbinary('RETR ' + crops_file, open('nass_crops.csv.gz', 'wb').write)
    ftp.quit()
    print 'Done extracting data'

    # Extract data from file within date period
    print 'Unzipping file...'
    target_file = open('nass_crops.csv', 'w')
    with gzip.open('nass_crops.csv.gz', 'rb') as f:
        file_content = f.read()
        target_file.write(file_content)
        target_file.close()


def read_file(start_date, end_date):
    dataframe = pd.read_csv('nass_crops.csv', sep='\t')

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    columns = ['DOMAIN_DESC', 'COMMODITY_DESC', 'STATISTICCAT_DESC', 'AGG_LEVEL_DESC', 'COUNTRY_NAME', 'STATE_NAME', 'COUNTY_NAME', 'UNIT_DESC', 'VALUE', 'YEAR']
    dataframe = dataframe[columns]

    filtered_dataframe = dataframe[(dataframe.YEAR >= start_year) & (dataframe.YEAR <= end_year)]

    return filtered_dataframe


def write_dataframe_to_db(dataframe, database_host, database_name, database_user, database_password, port):
    # create database
    connection_string = "postgres://" + database_user + ":" + database_password + "@" + database_host + ":" + str(port)
    engine = create_engine(connection_string)

    if not database_exists(connection_string + '/' + database_name):
        create_database(connection_string + '/' + database_name)

    dataframe.to_sql('fact_data', engine, if_exists='replace')


def begin_nass_harvest(database_host, database_name, database_user, database_password,
                       port, start_date, end_date):
    print "Run 'python harvest.py -h' for help\n\n"

    print "Supplied Args (some default): "
    print "Database Host: {}".format(database_host)
    print "Database Name: {}".format(database_name)
    print "Database Username: {}".format(database_user)
    print "Database Password: {}".format(database_password)
    print "Database Port (hard-coded): {}".format(port)
    print "Harvest Start Date: {}".format(start_date)
    print "Harvest End Date: {}\n".format(end_date)

    print "Started Fetching data...."
    print "This might take a while. Grab yourself some coffee."
    #fetch_data_via_ftp()
    print "*********** DONE FETCHING DATA **************"

    print "Reading data into a dataframe..."
    dataframe = read_file(start_date, end_date)
    print "*********** DONE READING DATA **************"

    print "Writing data to database"
    write_dataframe_to_db(dataframe, database_host, database_name, database_user, database_password, port)
    print "*********** DONE WRITING DATA **************"


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["database_host=", "database_name=", "start_date=",
                                               "database_user=", "database_pass=", "end_date="])
    except getopt.GetoptError:
        print 'Flag error. Probably a mis-typed flag. Make sure they start with "--". Run python ' \
              'harvest.py -h'
        sys.exit(2)

    # define defaults
    database_host = 'localhost'
    database_name = 'gro'
    port = 5432
    database_user = 'gro'
    database_password = 'gro123'
    start_date = '2005-1-1'
    end_date = '2015-12-31'

    for opt, arg in opts:
        if opt == '-h':
            print "\nThis is my harvest script for the Gro Hackathon NASS harvest"
            print '\nExample:\npython harvest.py --database_host localhost --database_name gro2\n'
            print '\nFlags (all optional, see defaults below):\n ' \
              '--database_host [default is "{}"]\n ' \
              '--database_name [default is "{}"]\n ' \
              '--database_user [default is "{}"]\n ' \
              '--database_pass [default is "{}"]\n ' \
              '--start_date [default is "{}"]\n ' \
              '--end_date [default is "{}"]\n'.format(database_host, database_name, database_user,
                                                      database_password, start_date, end_date)
            sys.exit()
        elif opt in ("--database_host"):
            database_host = arg
        elif opt in ("--database_name"):
            database_name = arg
        elif opt in ("--database_user"):
            database_user = arg
        elif opt in ("--database_pass"):
            database_password = arg
        elif opt in ("--start_date"):
            start_date = arg
        elif opt in ("--end_date"):
            end_date = arg

    begin_nass_harvest(database_host, database_name, database_user, database_password,
                       port, start_date, end_date)

if __name__ == "__main__":
    main(sys.argv[1:])

