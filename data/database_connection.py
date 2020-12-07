# -*- coding: utf-8 -*-
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
import datetime
import sys
from text_data import countries_dictionary
sys.path.append("..")
import covidparser
import neverpushit
from neverpushit import database_host, database_name, database_password, database_user


class Database:

        connection_to_the_database = psycopg2.connect(
                        host=database_host,
                        database=database_name,
                        user=database_user,
                        password=database_password)

        cursor = connection_to_the_database.cursor()

        def create_database():

                Database.cursor.execute('create table if not exists covid_stat (Last_update_date text, Last_update_time text, Country text unique, Cases text, New_cases text, Active_cases text, Cases_per1M text, Recovered text, New_recovered text, Critical_cases text, Deaths text, New_deaths text, Deaths_per1M text, Tests text, Tests_per1M text, population text)')

                Database.connection_to_the_database.commit()
                Database.connection_to_the_database.close()


        def data_skeleton():

                info_execute = 'select * from covid_stat'
                Database.cursor.execute(info_execute)

                rows = Database.cursor.fetchall()

                covid_stat_countries = [row[2] for row in rows]

                data_list = covidparser.CovidInfoParser.covid_data_world()
                datestamp_world = str(datetime.date.today().strftime('%d.%m.%Y'))
                timestamp_world = str(datetime.datetime.now().strftime('%H:%M'))
                Database.cursor.execute('insert into covid_stat (Last_update_date, Last_update_time, Country, Cases, New_cases, Active_cases, Cases_per1M, Recovered, New_recovered, Critical_cases, Deaths, New_deaths, Deaths_per1M, Tests, Tests_per1M) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                (datestamp_world, timestamp_world, 'World', data_list[0], data_list[1], data_list[5], data_list[7], data_list[4], data_list[12], data_list[6], data_list[2], data_list[3], data_list[8], data_list[9], data_list[10],))
                Database.connection_to_the_database.commit()

                for country in countries_dictionary[0]:
                        if country not in  covid_stat_countries:
                                data_list = covidparser.CovidInfoParser.covid_data_countries(country)
                                datestamp = str(datetime.date.today().strftime('%d.%m.%Y'))
                                timestamp = str(datetime.datetime.now().strftime('%H:%M'))
                                Database.cursor.execute('insert into covid_stat (Last_update_date, Last_update_time, Country, Cases, New_cases, Active_cases, Cases_per1M, Recovered, New_recovered, Critical_cases, Deaths, New_deaths, Deaths_per1M, Tests, Tests_per1M, population) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                (datestamp, timestamp, country, data_list[0], data_list[1], data_list[5], data_list[7], data_list[4], data_list[11], data_list[6], data_list[2], data_list[3], data_list[8], data_list[9], data_list[10], data_list[12],))
                                Database.connection_to_the_database.commit()

                Database.connection_to_the_database.close()

        def data_updater():
                
                world_data_list = covidparser.CovidInfoParser.covid_data_world()
                world_datestamp = str(datetime.date.today().strftime('%d.%m.%Y'))
                world_timestamp = str(datetime.datetime.now().strftime('%H:%M'))
                Database.cursor.execute("update covid_stat set Last_update_date = %s, Last_update_time = %s, Cases = %s, New_cases = %s, Active_cases = %s, Cases_per1M = %s, Recovered = %s, New_recovered = %s, Critical_cases = %s, Deaths = %s, New_deaths = %s, Deaths_per1M = %s, Tests = %s, Tests_per1M = %s where country = 'World'", 
                        (world_datestamp, world_timestamp, world_data_list[0], world_data_list[1], world_data_list[5], world_data_list[7], world_data_list[4], world_data_list[12], world_data_list[6], world_data_list[2], world_data_list[3], world_data_list[8], world_data_list[9], world_data_list[10],))
                Database.connection_to_the_database.commit()


                for country in countries_dictionary[0]:
                        country_data_list = covidparser.CovidInfoParser.covid_data_countries(country)
                        country_datestamp = str(datetime.date.today().strftime('%d.%m.%Y'))
                        country_timestamp = str(datetime.datetime.now().strftime('%H:%M'))
                        Database.cursor.execute("update covid_stat set Last_update_date = %s, Last_update_time = %s, Cases = %s, New_cases = %s, Active_cases = %s, Cases_per1M = %s, Recovered = %s, New_recovered = %s, Critical_cases = %s, Deaths = %s, New_deaths = %s, Deaths_per1M = %s, Tests = %s, Tests_per1M = %s, population = %s where country = " + """'""" + country + """'""", 
                        (country_datestamp, country_timestamp, country_data_list[0], country_data_list[1], country_data_list[5], country_data_list[7], country_data_list[4], country_data_list[11], country_data_list[6], country_data_list[2], country_data_list[3], country_data_list[8], country_data_list[9], country_data_list[10], country_data_list[12],))
                        Database.connection_to_the_database.commit()

while True:
        Database.data_updater()