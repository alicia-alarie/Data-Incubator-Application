# -*- coding: utf-8 -*-
"""
Created on Sat May  2 12:35:57 2020

@author: alicia
"""

import re
import requests
import requests_ftp
import requests_cache
import lxml
import json
from bs4 import BeautifulSoup
from collections import Counter
from matplotlib import pyplot as plt
plt.style.use('ggplot')
import pandas as pd
requests_cache.install_cache('coll_cache')
import sqlalchemy as sqla
import numpy as np


## Create database engine
sqlite_file = 'litb.sqlite'
litb = sqla.create_engine('sqlite:///' + sqlite_file)
# litb.execute('CREATE TABLE "clothing" ('
#                                             'Name VARCHAR, '
#                                             'Price FLOAT,'
#                                             'Gender VARCHAR,'
#                                             'Fabric VARCHAR,'
#                                             'Elasticity VARCHAR,'
#                                             'Pattern VARCHAR,'
#                                             'Fit_type VARCHAR,'
#                                             'Garment_Type VARCHAR,'
#                                             'Special_Size VARCHAR,'
#                                             'Popular_Country VARCHAR,'
#                                             'Waistline VARCHAR,'
#                                             'Trends VARCHAR,'
#                                             'Season VARCHAR,'
#                                             'Neckline VARCHAR,'
#                                             'Care VARCHAR,'
#                                             'Style VARCHAR,'
#                                             'Design VARCHAR,'
#                                             'Dress_Type VARCHAR,'
#                                             'Jumpsuit_Type VARCHAR,'
#                                             'Tops_Type VARCHAR,'
#                                             'Bottoms_Type VARCHAR,'
#                                             'Swimwear_Type VARCHAR,'
#                                             'Lingerie_Type VARCHAR,'
#                                             'Outerwear_Type VARCHAR,'
#                                             'Occasion VARCHAR,'
#                                             'Sleeve_Length VARCHAR,'
#                                             'Pattern_Theme VARCHAR,'
#                                             'Dress_Code VARCHAR,'
#                                             'Size_Suggestion VARCHAR,'
#                                             'Includes VARCHAR,'
#                                             'Hats_Category VARCHAR,'
#                                             'Gloves_Category VARCHAR,'
#                                             'Neckties_Type VARCHAR,'
#                                             'Jewelry_type VARCHAR,'
#                                             'Scarf_Type VARCHAR,'
#                                             'Panties_Category VARCHAR,'
#                                             'Nightwear_Style VARCHAR,'
#                                             'Bra_Style VARCHAR,'
#                                             'Bra_Category VARCHAR,'
#                                             'Category VARCHAR,'
#                                             'Sportswear_Category VARCHAR,'
#                                             'Outerwear_Length VARCHAR,'
#                                             'Production_Mode VARCHAR,'
#                                             'Feel VARCHAR,'
#                                             'Listing_Date VARCHAR,'
#                                             'Image_URL VARCHAR)')

# Scrape Mens and Womens
for g in range(0,2):
    if g==0:
        gender='womens'
    elif g==1:
        gender='mens'
    
    #Scrape All pages of Mens/Womens Clothing Listings
    for p in range(1,750):
        print('page:', p)
        print('\n\n\n\n\n')
        
        # websites for scraping
        if gender=='mens':
            urlbase="https://www.lightinthebox.com/index.php?main_page=info_check&action=get_ajax_category&cid=5585&show_count=52&img_width=384&img_height=500&img_width_class=240&img_height_class=312&sort=6d&current_page=" +str(p)+ "&page_size=60&mini_price=0&max_price=0&is_contain_oos=false&is_module=true&prm_page=2&prm_module=1&prm_position=4&page_from=products_category&product_count=16&template_id=150&category_name=Men%27s+Clothing&products_count=8"
        elif gender=='womens':
            urlbase = "https://www.lightinthebox.com/index.php?main_page=info_check&action=get_ajax_category&cid=71&show_count=50&img_width=285&img_height=375&img_width_class=190&img_height_class=250&sort=6d&current_page=" + str(p) + "&page_size=60&mini_price=0&max_price=0&selected_tags=&keyword_str=&is_module=false&selected_attributes=&is_contain_oos=&prm_page=2&prm_module=1&prm_position=1&page_from=products_category&product_count=20&template_id=157&category_name=Women%27s+Clothing&products_count=10"
        
        #request data and store in json object
        dataparams = {"forceFlatResults":"forceFlatResults"}
        req = requests.get(urlbase,params=dataparams)
        req.url
        html = req.text
        s=json.loads(html)
        if len(s.keys())>1:
            prod_list=s['product_list']
            print(len(prod_list))
    
            if len(prod_list)>0:
                
                #Scrape Each Product tile of Each Page
                for prod in prod_list:
                    
                    #go to page referenced in tile and request it's information
                    url =prod['prod_url']
                    tilereq = requests.get(url)
                    tilehtml = tilereq.text
                    
                    #store in Beautiful Soup object
                    tiledata = BeautifulSoup(tilehtml,'lxml')
                    #print(tiledata)
                    
                    #parse price
                    price = tiledata.find(name='strong',attrs={"itemprop" : "price"}).text
                    price=price.replace('$','')
                    price=price.split('-')
                    price=float(price[len(price)-1])
                    
                    #parse name
                    name= tiledata.find(name='h1').text
                    name=name[0:name.find('#')].replace("'",'')
                    name=name.replace('-','')
                    print(name)
                    
                    #Image URL
                    imgdata=tiledata.find(name='img')
                    Image_URL=imgdata['src']
                    
                    #Initialize Specification Values as N/A
                    Gender='N/A'
                    Fabric='N/A'
                    Elasticity='N/A'
                    Pattern='N/A'
                    Fit_Type='N/A'
                    Garment_Type='N/A'
                    Special_Size='N/A'
                    Popular_Country='N/A'
                    Waistline='N/A'
                    Trends='N/A'
                    Season='N/A'
                    Neckline='N/A'
                    Care='N/A'
                    Style='N/A'
                    Design='N/A'
                    Dress_Type='N/A'
                    Jumpsuit_Type='N/A'
                    Tops_Type='N/A'
                    Bottoms_Type='N/A'
                    Lingerie_Type='N/A'
                    Swimwear_Type='N/A'
                    Outerwear_Type='N/A'
                    Occasion='N/A'
                    Sleeve_Length='N/A'
                    Pattern_Theme='N/A'
                    Dress_Code='N/A'
                    Size_Suggestion='N/A'
                    Includes='N/A'
                    Hats_Category='N/A'
                    Gloves_Category='N/A'
                    Neckties_Type='N/A'
                    Jewelry_Type='N/A'
                    Scarf_Type='N/A'
                    Panties_Category='N/A'
                    Nightwear_Style='N/A'
                    Bra_Style='N/A'
                    Bra_Category='N/A'
                    Category='N/A'
                    Sportswear_Category='N/A'
                    Outerwear_Length='N/A'
                    Production_Mode='N/A'
                    Feel='N/A'
                    Listing_Date='N/A'
                    
                    #Parse Item Sepcifications
                    bigtitle= tiledata.find(name='div', attrs={'class': 'bigTitle'})
                    if bigtitle is None:
                        bigtitle= tiledata.find(name='div', attrs={'class': 'specTitle'})
                    
                    if bigtitle != None:
                        specs=bigtitle.find_all(name='tr')
                        if specs != None:
                            
                            #Parse the Values for Each Type of Specification
                            for spec in specs:
                                
                                #Find the Specification Name and Values
                                specname=spec.find(name='th').text
                                values=spec.find(name='td')
                                if values!=None:
                                    values=values.text
                                    values=values.replace('\n','')
                                    values=values[0:len(values)-1]
                                    
                                    #Assign the correct Values to each Specification
                                    if specname=='Gender':
                                        Gender=values.replace("'",'')
                                    elif specname=='Fabric':
                                        Fabric=values
                                    elif specname=='Elasticity':
                                        Elasticity=''
                                        Elasticity=values
                                    elif specname=='Pattern':
                                        Pattern=values
                                    elif specname=='Fit Type':
                                        Fit_Type=values
                                    elif specname=='Special Size':
                                        Special_Size=values
                                    elif specname=='Popular Country':
                                        Popular_Country=values
                                    elif specname=='Waistline':
                                        Waistline=values
                                    elif specname=='2020 Trends':
                                        Trends=values
                                    elif specname=='Season':
                                        Season=values
                                    elif specname=='Neckline':
                                        Neckline=values
                                    elif specname=='Look After Me':
                                        Care=values
                                    elif specname=='Style':
                                        Style=values
                                    elif specname=='Design':
                                        Design=values
                                    elif specname=='Dresses Type':
                                        Dress_Type=values
                                        Garment_Type='Dress'
                                    elif specname=='Jumpsuit Type':
                                        Jumpsuit_Type=values
                                        Garment_Type='Jumpsuit'
                                    elif specname=='Tops Type':
                                        Tops_Type=values
                                        Garment_Type='Top'
                                    elif specname=='Bottoms Type':
                                        Bottoms_Type=values
                                        Garment_Type='Bottom'
                                    elif specname=='Bottom Type':
                                        Bottoms_Type=values
                                        Garment_Type='Bottom'
                                    elif specname=='Swimwear Type':
                                        Swimwear_Type=values
                                        Garment_Type='Swimwear'
                                    elif specname=='Lingerie Type':
                                        Lingerie_Type=values
                                    elif specname=='Outerwear Type':
                                        Outerwear_Type=values
                                        Garment_Type='Outerwear'
                                    elif specname=='Occasion':
                                        Occasion=values
                                    elif specname=='Sleeve Length':
                                        Sleeve_Length=values
                                    elif specname=='Pattern Theme':
                                        Pattern_Theme=values
                                    elif specname=='Dress Code':
                                        Dress_Code=values
                                    elif specname=='Size_Suggestion':
                                        Size_Suggestion=values
                                    elif specname=='Inlcudes':
                                        Inlcudes=values
                                    elif specname=='Hats Category':
                                        Hats_Category=values
                                        Garment_Type='Hat'
                                    elif specname=='Gloves Category':
                                        Gloves_Category=values
                                        Garment_Type='Gloves'
                                    elif specname=='Neckties & Bows':
                                        Neckties_Type=values
                                        Garment_Type='Neckties'
                                    elif specname=='Jewelry Type':
                                        Jewelry_Type=values
                                        Garment_Type='Jewelry'
                                    elif specname=='Scarf Type':
                                        Scarf_Type=values
                                        Garment_Type='Scarf'
                                    elif specname=='Panties Category':
                                        Panties_Category=values
                                        Garment_Type='Panties'
                                    elif specname=='Nightwear Style':
                                        Nightwear_Style=values
                                        Garment_Type='Nightwear'
                                    elif specname=='Bra Style':
                                        Bra_Style=values
                                        Garment_Type='Bra'
                                    elif specname=='Bra Category':
                                        Bra_Category=values
                                        Garment_Type='Bra'
                                    elif specname=='Category':
                                        Category=values
                                    elif specname=='Sports Clothing Sub Category':
                                        Sportswear_Category=values
                                        Garment_Type='Sportswear'
                                    elif specname=='Outerwear Length':
                                        Outerwear_Length=values
                                        Garment_Type='Outerwear'
                                    elif specname=='Production Mode':
                                        Production_Mode=values
                                    elif specname=='Feel of Sensation':
                                        Feel=values
                                    elif specname=='Listing Date':
                                        Listing_Date=values
                            
                    
                    #add entry to sql database file
                    sql = ''' INSERT INTO clothing("name",Price,"Gender","Fabric","Elasticity","Pattern","Fit_Type","Garment_Type","Special_Size","Popular_Country","Waistline","Trends","Season","Neckline","Care","Style","Design","Dress_Type","Jumpsuit_Type","Tops_Type","Bottoms_Type","Swimwear_Type","Lingerie_Type","Outerwear_Type","Occasion","Sleeve_Length","Pattern_Theme","Dress_Code","Size_Suggestion","Includes","Hats_Category","Gloves_Category","Neckties_Type","Jewelry_Type","Scarf_Type","Panties_Category","Nightwear_Style","Bra_Style","Bra_Category","Category","Sportswear_Category","Outerwear_Length","Production_Mode","Feel","Listing_Date","Image_URL")
                              VALUES("{name}",{price},"{Gender}","{Fabric}","{Elasticity}","{Pattern}","{Fit_Type}","{Garment_Type}","{Special_Size}","{Popular_Country}","{Waistline}","{Trends}","{Season}","{Neckline}","{Care}","{Style}","{Design}","{Dress_Type}","{Jumpsuit_Type}","{Tops_Type}","{Bottoms_Type}","{Swimwear_Type}","{Lingerie_Type}","{Outerwear_Type}","{Occasion}","{Sleeve_Length}","{Pattern_Theme}","{Dress_Code}","{Size_Suggestion}","{Includes}","{Hats_Category}","{Gloves_Category}","{Neckties_Type}","{Jewelry_Type}","{Scarf_Type}","{Panties_Category}","{Nightwear_Style}","{Bra_Style}","{Bra_Category}","{Category}","{Sportswear_Category}","{Outerwear_Length}","{Production_Mode}","{Feel}","{Listing_Date}","{Image_URL}") '''.format(name= name.replace('"',''), price=price, Gender=Gender.replace('"',''),Fabric=Fabric.replace('"',''),Elasticity=Elasticity.replace('"',''), Pattern=Pattern.replace('"',''), Fit_Type=Fit_Type.replace('"',''), Garment_Type=Garment_Type.replace('"',''), Special_Size=Special_Size.replace('"',''), Popular_Country=Popular_Country.replace('"',''), Waistline=Waistline.replace('"',''), Trends=Trends.replace('"',''), Season=Season.replace('"',''), Neckline=Neckline.replace('"',''), Care=Care.replace('"',''), Style=Style.replace('"',''), Design=Design.replace('"',''), Dress_Type=Dress_Type.replace('"',''), Jumpsuit_Type=Jumpsuit_Type.replace('"',''), Tops_Type=Tops_Type.replace('"',''), Bottoms_Type=Bottoms_Type.replace('"',''), Swimwear_Type=Swimwear_Type.replace('"',''), Lingerie_Type=Lingerie_Type.replace('"',''), Outerwear_Type=Outerwear_Type.replace('"',''), Occasion=Occasion.replace('"',''), Sleeve_Length=Sleeve_Length.replace('"',''), Pattern_Theme=Pattern_Theme.replace('"',''), Dress_Code=Dress_Code.replace('"',''), Size_Suggestion=Size_Suggestion.replace('"',''), Includes=Includes.replace('"',''), Hats_Category=Hats_Category.replace('"',''), Gloves_Category=Gloves_Category.replace('"',''), Neckties_Type=Neckties_Type.replace('"',''), Jewelry_Type=Jewelry_Type.replace('"',''), Scarf_Type=Scarf_Type.replace('"',''), Panties_Category=Panties_Category.replace('"',''), Nightwear_Style=Nightwear_Style.replace('"',''), Bra_Style=Bra_Style.replace('"',''),Bra_Category=Bra_Category.replace('"',''),Category=Category.replace('"',''),Sportswear_Category=Sportswear_Category.replace('"',''),Outerwear_Length=Outerwear_Length.replace('"',''),Feel=Feel.replace('"',''),Production_Mode=Production_Mode.replace('"',''),  Listing_Date=Listing_Date.replace('"',''), Image_URL=Image_URL.replace('"',''), if_exists='replace')
                    litb.execute(sql)
            
    #Import database into Python as a Pandas DataFrame for verification 
    data=pd.read_sql_query("select * from clothing", litb)
    
    
