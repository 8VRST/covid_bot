# -*- coding: utf-8 -*-
import os
import psycopg2
import neverpushit
from neverpushit import database_host, database_name, database_password, database_user

connection_to_the_database = psycopg2.connect(
                        host=database_host,
                        database=database_name,
                        user=database_user,
                        password=database_password)

cursor = connection_to_the_database.cursor()


def return_belarus_data(country):

        country = country

        cursor.execute("select * from covid_stat where country = " + """'""" + country + """'""")

        country_data = cursor.fetchone()

        belarus_info = str('📊⬜️🟥⬜️ ПО ПОСЛЕДНИМ ОФИЦИАЛЬНЫМ ДАННЫМ В БЕЛАРУСИ:\n\n🤒 ' +  country_data[3] + ' случаев' + 
        ' | ' + country_data[4] + ' новых случаев' + ' | ' + country_data[5] + ' активных носителей' + ' | ' + country_data[6] + ' случаев на миллион населения ' + 
        '\n\n💪 ' + country_data[7] + ' выздоровевших' + ' | ' + country_data[8] + ' новых выздоровевших' +
        '\n\n🏥 ' + country_data[9] + ' в критическом состоянии*' +
        '\n\n⚰️ ' + country_data[10] + ' смертей' + ' | ' + country_data[11] + ' новых смертей' ' | ' + country_data[12] + ' смертей на миллион населения' +  
        '\n\n🧪 ' + country_data[13] + ' тестов' + ' | ' + country_data[14] + ' тестов на миллион населения ' + 
        '\n\n👨‍👩‍👧‍👦 ' + 'население составляет ' + country_data[15] + 'человек' +
        '\n\n🕰 дата и время последнего обновления информации: ' + country_data[0] + ' в ' + country_data[1] + ' по GMT+3' +
        '\n\n*некоторое время назад власти совсем перестали давать данные по этому показателю, поэтому неопределённое время может быть "0" вместо реальных цифр')

        return belarus_info

def return_country_data(country):

        country = country

        cursor.execute("select * from covid_stat where country = " + """'""" + country + """'""")

        country_data = cursor.fetchone()

        country_info = str('📊 ПО ПОСЛЕДНИМ ОФИЦИАЛЬНЫМ ДАННЫМ В ВЫБРАННОЙ СТРАНЕ:' + '\n\n🤒 ' + country_data[3] + ' случаев' + 
        ' | ' + country_data[4] + ' новых случаев' + ' | ' + country_data[5] + ' активных носителей' + ' | ' + country_data[6] + ' случаев на миллион населения ' + 
        '\n\n💪 ' + country_data[7] + ' выздоровевших' + ' | ' + country_data[8] + ' новых выздоровевших' +
        '\n\n🏥 ' + country_data[9] + ' в критическом состоянии' +
        '\n\n⚰️ ' + country_data[10] + ' смертей' + ' | ' + country_data[11] + ' новых смертей' ' | ' + country_data[12] + ' смертей на миллион населения' +  
        '\n\n🧪 ' + country_data[13] + ' тестов' + ' | ' + country_data[14] + ' тестов на миллион населения ' + 
        '\n\n👨‍👩‍👧‍👦 ' + 'население составляет ' + country_data[15] + 'человек' + 
        '\n\n🕰 дата и время последнего обновления информации: ' + country_data[0] + ' в ' + country_data[1] + ' по GMT+3')

        return country_info

def return_world_data():

        cursor.execute("select * from covid_stat where country = 'World'")

        world_data = cursor.fetchone()

        world_info = str('📊🌐 ПО ПОСЛЕДНИМ ОФИЦИАЛЬНЫМ ДАННЫМ В МИРЕ:\n\n🤒 ' + world_data[3] + ' случаев' + 
        ' | ' + world_data[4] + ' новых случаев' + ' | ' + world_data[5] + ' активных носителей' + ' | ' + world_data[6] + ' случаев на миллион населения ' + 
        '\n\n💪 ' + world_data[7] + ' выздоровевших' ' | ' + world_data[8] + ' новых выздоровевших' + 
        '\n\n🏥 ' + world_data[9] + ' в критическом состоянии' +
        '\n\n⚰️ ' + world_data[10] + ' смертей' + ' | ' + world_data[11] + ' новых смертей' ' | ' + world_data[12] + ' смертей на миллион населения' + 
        '\n\n🕰 дата и время последнего обновления информации: ' + world_data[0] + ' в ' + world_data[1] + ' по GMT+3')

        return world_info

replace_values = {" И " : " и ", " Острова" : " острова", " Административный Регион" : " административный регион", "Кот-Д'Ивуар" : "Кот-д'Ивуар", "Сша" : "США", "Оаэ" : "ОАЭ"}

def multiple_replace(target_str, replace_values):
    
    for x, y in replace_values.items():
        target_str = target_str.replace(x, y)
        
    return target_str