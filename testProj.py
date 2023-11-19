import pandas as pd
import numpy as np 


def main():

    df = pd.read_excel("Volvo Cars Waste data-Stena Recyling report_2023.xlsx")
    df_des = pd.read_excel("Volvo Cars Waste data-Support data.xlsx")

    #filtiring the Rod code
    RodKod = df['RodKodbeskr']
    indexes1 = RodKod[RodKod == "-1 N/A"].index.tolist()
    df_filtered = df.drop(index=indexes1)
    #print(df_filtered)

    #filtiring the returants 
    place = df_filtered['Hämtställe Märkning']
    indexes2 = place[place.isin(["Rest. Jacob, kundnr: 0468801", "Rest. Emma, kundnr: 0185512", "Rest. Hive Food Market kundnr: 0468777", "Rest. Höjden, kundnr: 0468785", "Rest. The Harvest (Volvo PVD)"])].index.tolist()
    df_filtered2 = df_filtered.drop(index=indexes2)
    #print(df_filtered2)

    #filtiring the city
    city = df_filtered2['Hämtställe Ort']
    indexes3 = city[city == 'Mölndal'].index.tolist()
    df_filtered3 = df_filtered2.drop(index = indexes3)
    #print(df_filtered3)


    #RA


    place = df_filtered3['Hämtställe Märkning']
    indexes_for_ra = place[place.str.contains(r'\bRA\b')].index.tolist()
    #print(indexes_for_ra)
    ra_data = df_filtered3.loc[indexes_for_ra]
    #print(ra_data['Hämtställe Märkning'])


    #RB 
    place = df_filtered3['Hämtställe Märkning']
    indexes_for_rb = place[place.str.contains(r'\bRB\b')].index.tolist()
    #print(indexes_for_rb)
    rb_data = df_filtered3.loc[indexes_for_rb]
    #print(rb_data['Hämtställe Märkning'])

    #Lammhult
    place = df_filtered3['Hämtställe Märkning']
    indexes_for_lammhult = place[place.str.contains(r'\bLammhult\b')].index.tolist()
    #print(indexes_for_lammhult)
    lammhult_data = df_filtered3.loc[indexes_for_lammhult]

    indexes_for_lager = indexes_for_ra + indexes_for_rb + indexes_for_lammhult
    indexes_for_lager = sorted(indexes_for_lager)
    #print(indexes_for_lager)

    data_for_the_lager = df_filtered3.loc[indexes_for_lager]
    data_for_the_rest= df_filtered3.drop(index=indexes_for_lager)
    weight_amin=data_for_the_lager['Kvantitet kg']
    print(2222222222222222222222222222222222222222222222222)

    z=sum(weight_amin)
    print(z)





    places= data_for_the_lager['RodKodbeskr']
    indexes_of_Recycled=places[places.str.contains(r'Recycled')].index.tolist()
    print(indexes_of_Recycled)
    print(len(indexes_of_Recycled))



    data_recycled=data_for_the_lager.loc[indexes_of_Recycled]
    data_not_recycled=data_for_the_lager.drop(index=indexes_of_Recycled)
    print(data_recycled)
    print(data_not_recycled)

    weight_rec=data_recycled['Kvantitet kg']
    x=sum(weight_rec)
    print(x)

    weight_not_rec=data_not_recycled['Kvantitet kg']
    y=sum(weight_not_rec)
    print(y)

    tot=x+y
    print(tot)
    ##


    
    places2=data_for_the_rest['RodKodbeskr']
    indexes_of_Recycled_not_lager=places2[places2.str.contains(r'Recycled')].index.tolist()
    #print(indexes_of_Recycled_not_lager)
    print(len(indexes_of_Recycled_not_lager))
    data_recycled_not_lager=data_for_the_rest.loc[indexes_of_Recycled_not_lager]
    

   
    data_not_recycled_not_lager=data_for_the_rest.drop(index=indexes_of_Recycled_not_lager)
    #print(data_recycled_not_lager)
    #print(data_not_recycled_not_lager)

    weight_rec_not_lager=data_recycled_not_lager['Kvantitet kg']
    x1=sum(weight_rec_not_lager)
    #print(x1)
    

    weight_not_rec_not_kager=data_not_recycled_not_lager['Kvantitet kg']
    y1=sum(weight_not_rec_not_kager)
    #print(y1)
    tot1=x1+y1
    #print("total"+tot1)


    
    print(len(data_not_recycled_not_lager))
    print(len(data_for_the_rest))
    print(len(data_for_the_lager))
    print(len(indexes1)+len(indexes2)+len(indexes3))

    print(444444444445555555555)
    print(x+y)

    







    


    #print(rb_data['Kvantitet kg'])



if __name__ == '__main__':
    main()