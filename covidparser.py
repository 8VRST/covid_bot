# -*- coding: utf-8 -*-
import os
import parser
import requests
import urllib3
import urllib.request
from lxml import html
import bs4
from bs4 import BeautifulSoup
import json
import re
from flask import Flask, request, flash, url_for, redirect, render_template
from data.text_data import countries_dictionary

basedir = os.path.abspath(os.path.dirname(__file__))


headers = {'User-Agent' : 'Chrome'}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CovidInfoParser:

    def parted_page():

        url = 'https://www.worldometers.info/coronavirus/'

        response = requests.get(url, verify=False, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table_div_world_stat = soup.find('table', {'id' : 'main_table_countries_today'}).find('tbody', {'class' : 'total_row_body'}).find_all('td')

        table_div_countries_stat = soup.find('table', {'id' : 'main_table_countries_today'}).find('tbody').find_all('td')

        table_div_countries_list = soup.find('tbody').find_all('a', {'class': 'mt_a'})

        table_div_list = [table_div_world_stat, table_div_countries_stat, table_div_countries_list]

        return table_div_list

    def countries_list():

        countries_list = list()

        for country in CovidInfoParser.parted_page()[2]:
            country = country.text
            countries_list.append(country)
        
        countries_sorted_list = sorted(countries_list)

        return countries_sorted_list

    def covid_data_countries(country):
        
        country = country

        countries_data_list = list()

        for countries_data in CovidInfoParser.parted_page()[1]:
            countries_data = countries_data.text
            countries_data_list.append(countries_data)

        def country_index_in_list():

            if country == 'Australia':

                for element in countries_data_list:
                    if element == country:
                        country_index_in_table = countries_data_list.index(element)
                        break

            else:

                    for country_number in range(len(countries_data_list)):
                        if country in countries_data_list[country_number]:
                            country_index_in_table = country_number
                            break
                    
            return country_index_in_table

        country_total_cases = str(countries_data_list[int(country_index_in_list())+1])
        country_new_cases = str(countries_data_list[int(country_index_in_list())+2])
        country_total_deaths = str(countries_data_list[int(country_index_in_list())+3])
        country_new_deaths = str(countries_data_list[int(country_index_in_list())+4])
        country_total_recovered = str(countries_data_list[int(country_index_in_list())+5])
        country_new_recovered = str(countries_data_list[int(country_index_in_list())+6])
        country_active_cases = str(countries_data_list[int(country_index_in_list())+7])
        country_critical_cases = str(countries_data_list[int(country_index_in_list())+8])
        country_per1M_cases = str(countries_data_list[int(country_index_in_list())+9])
        country_per1M_deaths = str(countries_data_list[int(country_index_in_list())+10])
        countrys_total_tests = str(countries_data_list[int(country_index_in_list())+11])
        country_tests_per1M = str(countries_data_list[int(country_index_in_list())+12])
        country_population = str(countries_data_list[int(country_index_in_list())+13])

        formatted_countries_data = [country_total_cases, country_new_cases, country_total_deaths, country_new_deaths, 
         country_total_recovered, country_active_cases, country_critical_cases, country_per1M_cases, country_per1M_deaths,
         countrys_total_tests, country_tests_per1M, country_new_recovered, country_population]

        for index_for_countries_data in range(len(formatted_countries_data)):
            if formatted_countries_data[index_for_countries_data] == '':
                formatted_countries_data[index_for_countries_data] = '0'
            elif formatted_countries_data[index_for_countries_data] == 'N/A':
                formatted_countries_data[index_for_countries_data] = 'нет данных о'

        return formatted_countries_data

    def covid_data_world():

        world_data_list = list()

        for world_data in CovidInfoParser.parted_page()[0]:
            world_data = world_data.text
            world_data_list.append(world_data)

        total_cases = str(world_data_list[2])
        new_cases = str(world_data_list[3])
        total_deaths = str(world_data_list[4])
        new_deaths = str(world_data_list[5])
        total_recovered = str(world_data_list[6])
        new_recovered = str(world_data_list[7])
        active_cases = str(world_data_list[8])
        crirtical_cases = str(world_data_list[9])
        per1M_cases = str(world_data_list[10]).replace('.', ',')
        per1M_deaths = str(world_data_list[11]).replace('.', ',')
        total_tests = str(world_data_list[12])
        tests_per1M = str(world_data_list[13])
        population = str(world_data_list[14])

        formatted_world_data = [total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, crirtical_cases,
                per1M_cases,  per1M_deaths, total_tests, tests_per1M, population, new_recovered]

        for index_for_world_data in range(len(formatted_world_data)):
            if formatted_world_data[index_for_world_data] == '':
                formatted_world_data[index_for_world_data] = '0'


        return formatted_world_data
        