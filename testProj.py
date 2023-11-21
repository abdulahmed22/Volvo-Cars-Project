
import pandas as pd
import numpy as np 
import  matplotlib.pyplot as plt

#############
def process_data_and_plot(data, title_suffix=''):
    # Extract 'Lev.YearMonth' as strings
    months = data['Lev.YearMonth'].astype(str)

    # Get unique months in the dataset
    unique_months = sorted(months.unique())  ##sendning order for both lager and not lager

    # Initialize lists to store data for each month
    recycled_sum_per_month = []
    not_recycled_sum_per_month = []

    # Iterate over each unique month
    for month in unique_months:
        # Filter the data for the current month
        indexes_of_month = months[months.str.contains(month)].index.to_list()

        # Extract 'RodKodbeskr' for the current month
        data_month = data.loc[indexes_of_month, 'RodKodbeskr']


        ## For testing the result:
        data_amin=data.loc[indexes_of_month, 'Kvantitet kg']
        print(title_suffix)
        print(month)
        print(len(data_amin))
        print("data month :")
        print (data_amin)
        #################################

        # Get indices where 'RodKodbeskr' contains 'Recycle' for the current month
        indexes_of_Recycled_month = data_month[data_month.str.contains(r'Recycle', case=False)].index.tolist()

        # Get indices where 'RodKodbeskr' does not contain 'Recycle' for the current month
        indexes_of_Not_Recycled_month = data_month[~data_month.str.contains(r'Recycle', case=False)].index.tolist()

        # Extract weights for recycled and not recycled items for the current month
        weight_recycled_month = data.loc[indexes_of_Recycled_month, 'Kvantitet kg']
        weight_Not_recycled_month = data.loc[indexes_of_Not_Recycled_month, 'Kvantitet kg']

        # Sum weights for recycled and not recycled items for the current month
        recycled_sum_per_month.append(sum(weight_recycled_month))
        not_recycled_sum_per_month.append(sum(weight_Not_recycled_month))


       # Print total_weight_per_month, total_recycled, and total_not_recycled for each month
    for i, month in enumerate(unique_months):
        if i < len(recycled_sum_per_month) and i < len(not_recycled_sum_per_month):
            total_weight = recycled_sum_per_month[i] + not_recycled_sum_per_month[i]
            total_recycled = recycled_sum_per_month[i]
            total_not_recycled = not_recycled_sum_per_month[i]

            # Print whether it's for "Lager" or "Rest"
            location_type = 'Lager' if 'Lager' in title_suffix else 'Rest'
            print(f'{location_type} - Month: {month}, Total Weight: {total_weight}, Total Recycled: {total_recycled}, Total Not Recycled: {total_not_recycled}')
        else:
            print(f'Error: Index {i} out of range')

        


    # Plotting for Each Month (Total Weight)
    total_weight_per_month = [total_recycled + total_not_recycled for total_recycled, total_not_recycled in zip(recycled_sum_per_month, not_recycled_sum_per_month)]

    plt.figure(figsize=(10, 6))
    plt.bar(unique_months, total_weight_per_month, color='blue')
    plt.xlabel('Month')
    plt.ylabel(f'Total Weight {title_suffix}')
    plt.title(f'Total Weight for Each Month in the Year {title_suffix}')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    # Plotting for the Whole Year (Together)
    total_recycled_sum = sum(recycled_sum_per_month)
    total_not_recycled_sum = sum(not_recycled_sum_per_month)

    # Plotting for Each Month
    width = 0.35  # the width of the bars
    months_range = range(len(unique_months))

    plt.bar(months_range, recycled_sum_per_month, width, label='Recycled', color='green')
    plt.bar(months_range, not_recycled_sum_per_month, width, bottom=recycled_sum_per_month, label='Not Recycled', color='gray')

    # Configure the plot
    plt.xlabel('Month')
    plt.ylabel(f'Total Weight {title_suffix}')
    plt.title(f'Total Weight for Each Month {title_suffix}')
    plt.xticks(months_range, unique_months)
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():

    df = pd.read_excel("Volvo Cars Waste data-Stena Recyling report_2023.xlsx")
    #df_des = pd.read_excel("Volvo Cars Waste data-Support data.xlsx")

    #filtiring the Rod code
    RodKod = df['RodKodbeskr']
    indexes1 = RodKod[RodKod == "-1 N/A"].index.tolist()
    df_filtered = df.drop(index=indexes1)
    

    #filtiring the returants 
    place = df_filtered['Hämtställe Märkning']
    indexes2 = place[place.isin(["Rest. Jacob, kundnr: 0468801", "Rest. Emma, kundnr: 0185512", "Rest. Hive Food Market kundnr: 0468777", "Rest. Höjden, kundnr: 0468785", "Rest. The Harvest (Volvo PVD)"])].index.tolist()
    df_filtered2 = df_filtered.drop(index=indexes2)
    

    #filtiring the city
    city = df_filtered2['Hämtställe Ort']
    indexes3 = city[city == 'Mölndal'].index.tolist()
    df_filtered3 = df_filtered2.drop(index = indexes3)



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
    

    process_data_and_plot(df_filtered3.loc[indexes_for_lager], 'Lager')
    process_data_and_plot(df_filtered3.drop(index=indexes_for_lager), 'Rest')

###


   



    # Plotting
    #weight_lager_jan_num=sum(weight_lager_jan)
    #weight_lager_feb_num=sum(weight_lager_feb)
    #plt.bar(['January', 'February'], [weight_lager_jan_num, weight_lager_feb_num])
   

        

    
    #print(indexes_of_jan)
    #print(len(indexes_of_jan))






    #the total for lager
    #tot_for_lager=data_for_the_lager['Kvantitet kg']
    #tot_for_lager_x=sum(tot_for_lager)
    #print(9090909090)
    #print("The total for lager "+str(tot_for_lager_x))


    #for lager in 01

    


    #tot_for_Not_lager=data_for_the_rest['Kvantitet kg']
    #tot_for_lager_y=sum(tot_for_Not_lager)
    #print(9393939393)
   # print("The total for Not lager "+str(tot_for_lager_y))





   # places= data_for_the_lager['RodKodbeskr']
    #indexes_of_Recycled=places[places.str.contains(r'Recycled')].index.tolist()
   # print(indexes_of_Recycled)
    #print(len(indexes_of_Recycled))



    #data_recycled=data_for_the_lager.loc[indexes_of_Recycled]
    #data_not_recycled=data_for_the_lager.drop(index=indexes_of_Recycled)
    #print(data_recycled)
    #print(data_not_recycled)

   # weight_rec=data_recycled['Kvantitet kg']
   # x=sum(weight_rec)
   # print(x)

   # weight_not_rec=data_not_recycled['Kvantitet kg']
    #y=sum(weight_not_rec)
    #print(y)

    #tot=x+y
    #print(tot)
    ###


    
    #places2=data_for_the_rest['RodKodbeskr']
    #indexes_of_Recycled_not_lager=places2[places2.str.contains(r'Recycled')].index.tolist()
    #print(indexes_of_Recycled_not_lager)
    #print(len(indexes_of_Recycled_not_lager))
    #data_recycled_not_lager=data_for_the_rest.loc[indexes_of_Recycled_not_lager]
    

   
    #data_not_recycled_not_lager=data_for_the_rest.drop(index=indexes_of_Recycled_not_lager)
    #print(data_recycled_not_lager)
    #print(data_not_recycled_not_lager)

    #weight_rec_not_lager=data_recycled_not_lager['Kvantitet kg']
    #x1=sum(weight_rec_not_lager)
    #print(x1)
    

   # weight_not_rec_not_kager=data_not_recycled_not_lager['Kvantitet kg']
   # y1=sum(weight_not_rec_not_kager)
    #print(y1)
    #tot1=x1+y1

    #print(tot1)
   


    
   

   
    


if __name__ == '__main__':
    main()