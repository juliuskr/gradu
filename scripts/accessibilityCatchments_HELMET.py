#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python-script for calculating car, public transportation and cycling accessibility with HELMET-data

Author: Julius Krötzl - 3.2.2019

"""

import pandas as pd
import numpy as np


# Työvoiman saavutettavuus joukkoliikenteellä: Kuinka paljon asukkaita saavuttaa alueen 30 minuutissa nykyisin?

def createCatchmentsLoglog(travelmode, year, landuse, maxtraveltime, datafolder, a, b):

    # Luetaan matka-ajat
#    fpttmatrix = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/2030_aht_auto_korj_pysakointi2min.csv'
#    ttmatrix = pd.read_csv(fpttmatrix, sep=',')
    
    fppmatrix = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/nyky_pyora_pysakointi1min_12kmh.csv'
    ttmatrix = pd.read_csv(fppmatrix, sep=',')
    
    # Luetaan väestö- tai työpaikkamäärät
    fplanduse = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/output_korjattu/landuse.csv'
    lutable = pd.read_csv(fplanduse,sep=',', skiprows=0)
        
    # Yhdistetään maankäyttödata matka-aikataulukon viimeiseksi sarakkeeksi ja luodaan siitä uusi merged-taulukko
    merged = ttmatrix.merge(lutable[['id', landuse]],how='left')
    
    # Luodaan uusi results-taulukko, jossa on 2 saraketta: alueen id ja väestö-/työpaikkakertymä halutun ajan sisällä
    results = pd.DataFrame(columns=['id', landuse[0] + year[2:] + travelmode[:2] + '_' + str(a) + str(b)])
        
    # Iteroinnin avulla käydään läpi jokainen sarake jlnykypop-taulukossa
    for column in merged:
        print(column)
        # luodaan tyhjä lista
        list=[]
        # käydään läpi jokainen minuutti 0:n ja maxtraveltime:n välillä
        for value in range(maxtraveltime):
            # valitaan sarakkeen kohdalla kaikki solut, joissa matka-aika on value ja value+1 välillä
            pop = merged.loc[((merged[column] >= value) & (merged[column] < value+1))]
            # lasketaan valittujen solujen summa
            total = pop[landuse].sum()
            # kerrotaan summa matka-ajan neliön käänteisluvulla
            weighted_value = total * 1/(1+(value/a)**b)
            # lisätään painotettu arvo listaan
            list.append(weighted_value)
            # lasketaan listan summa
            sum_list = sum(list)
        # Luodaan uusi new_row-niminen lista, joka sisältää sarakkeen otsikon sekä sen sisältämän väestömäärän 30 minuutissa
        new_row = [column, sum_list]
        # Sijoitetaan new_row-lista results-taulukkoon
        results.loc[len(results)] = new_row
        
    # Poistetaan results-taulukon ensimmäinen ja viimeinen rivi
    results = results.drop(results.index[[0, len(results)-1]])
    
    # Pyöräily: ota p-kirjain pois id-sarakkeen arvoista
    if travelmode=='pyora':
        results['id'] = results.id.str[:-1]

        
    # Tallennetaan tulokset csv-tekstitiedostoksi haluttuun kansioon
    outfp = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/output_korjattu/'  + landuse + '_' + travelmode + '_' + year + '_loglogistic_a' + str(a) + '_b' + str(b) + '_max' + str(maxtraveltime) + 'min.csv'
    results.to_csv(outfp)
    
def gaussianCatchments(travelmode, year, landuse, maxtraveltime, z, datafolder):

    # Luetaan matka-ajat
#    fpttmatrix = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/2030_aht_auto_korj_pysakointi2min.csv'
#    ttmatrix = pd.read_csv(fpttmatrix, sep=',')
#    fpttmatrix = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/2030_aht_jl_korj_transp.txt'
#    ttmatrix = pd.read_csv(fpttmatrix, delim_whitespace=True)
    
    fppmatrix = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/nyky_pyora_pysakointi1min_12kmh.csv'
    ttmatrix = pd.read_csv(fppmatrix, sep=',')
    
    # Luetaan väestö- tai työpaikkamäärät
    fplanduse = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/opiskelupaikat_2015.csv'
    lutable = pd.read_csv(fplanduse, skiprows=0, sep=',')
        
    # Yhdistetään maankäyttödata matka-aikataulukon viimeiseksi sarakkeeksi ja luodaan siitä uusi merged-taulukko
    merged = ttmatrix.merge(lutable[['id', landuse]],how='left')
    
    # Luodaan uusi results-taulukko, jossa on 2 saraketta: alueen id ja väestö-/työpaikkakertymä halutun ajan sisällä
    results = pd.DataFrame(columns=['id', landuse[0] + year + travelmode[:2] + '_z' + str(z)])
        
    # Iteroinnin avulla käydään läpi jokainen sarake jlnykypop-taulukossa
    for column in merged:
        print(column)
        # luodaan tyhjä lista
        list=[]
        # käydään läpi jokainen minuutti 0:n ja maxtraveltime:n välillä
        for value in range(maxtraveltime):
            # valitaan sarakkeen kohdalla kaikki solut, joissa matka-aika on value ja value+1 välillä
            pop = merged.loc[((merged[column] >= value) & (merged[column] < value+1))]
            # lasketaan valittujen solujen summa
            total = pop[landuse].sum()
            # kerrotaan summa matka-ajan neliön käänteisluvulla
            weighted_value = total * np.exp(-value**2/z)
            # lisätään painotettu arvo listaan
            list.append(weighted_value)
            # lasketaan listan summa
            sum_list = sum(list)
        # Luodaan uusi new_row-niminen lista, joka sisältää sarakkeen otsikon sekä sen sisältämän väestömäärän 30 minuutissa
        new_row = [column, sum_list]
        # Sijoitetaan new_row-lista results-taulukkoon
        results.loc[len(results)] = new_row
        
    # Pyöräily: ota p-kirjain pois id-sarakkeen arvoista
    if travelmode=='pyora':
        results['id'] = results.id.str[:-1]
        
    # Poistetaan results-taulukon ensimmäinen ja viimeinen rivi
    results = results.drop(results.index[[0, len(results)-1]])
        
    # Tallennetaan tulokset csv-tekstitiedostoksi haluttuun kansioon
    outfp = '/Users/juliuskrotzl/OneDrive/Gradu/GIS/output_korjattu/'  + landuse + '_' + travelmode + '_' + year + '_gaussian_z' + str(z) + '_max' + str(maxtraveltime) + 'min.csv'
    results.to_csv(outfp)
    
    
gaussianCatchments(travelmode='pyora', year='2030', landuse='opiskelupa', maxtraveltime=60, z=900, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu')
    
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='vaesto', maxtraveltime=90, a=25, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='kul_vap_ai', maxtraveltime=60, a=20, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='liikuntapa', maxtraveltime=50, a=15, b=3.0, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='muu_kauppa', maxtraveltime=75, a=17, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='esik_paiva', maxtraveltime=20, a=6, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='koulut_lkm', maxtraveltime=70, a=17, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='asiointi2', maxtraveltime=70, a=19, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='ravintolat', maxtraveltime=50, a=18, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
createCatchmentsLoglog(travelmode='pyora', year='2030', landuse='paiv_kaupp', maxtraveltime=35, a=9, b=2.8, datafolder='/Users/juliuskrotzl/Helsingin kaupunki/Saavutettavuustyökalu/data')
