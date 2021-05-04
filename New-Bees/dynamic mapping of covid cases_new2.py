import pandas as pd
import geopandas as gpd
import PIL
import io


data=pd.read_csv('D:/ABC/internal hack/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

data=data.groupby('Country/Region').sum()

data = data.drop(columns=['Lat','Long'])

data_transposed = data.T
##data_transposed.plot(y=['India','Australia','US','China','Russia','Brazil'], use_index=True, figsize=(8,8))

world = gpd.read_file(r'D:/ABC/internal hack/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/World_Countries.shp')

world.replace('Myanmar','Burma', inplace=True)
world.replace('Cape Verde','Cabo Verde', inplace=True)
world.replace('Democratic Republic of the Congo','Congo (Brazzaville)', inplace=True)
world.replace('Congo','Congo (Kinshasa)', inplace=True)
world.replace('Ivory Coast',"Cote d'Ivoire", inplace=True)
world.replace('Czech Republic','Czechia', inplace=True)
world.replace('Swaziland','Eswatini', inplace=True)
world.replace('South Korea','Korea, South', inplace=True)
world.replace('Macedonia','North Macedonia', inplace=True)
world.replace('St. Kitts and Nevis','Saint Kitts and Nevis', inplace=True)
world.replace('St. Lucia','Saint Lucia', inplace=True)
world.replace('St. Vincent and the Grenadines','Saint Vincent and the Grenadines', inplace=True)
world.replace('Western Samoa','Samoa', inplace=True)
world.replace('Taiwan','Taiwan*', inplace=True)
world.replace('East Timor','Timor-Leste', inplace=True)
world.replace('United States','US', inplace=True)
world.replace('Palestine','West Bank and Gaza', inplace=True)

##for index, row in data.iterrows():
  ##  if index not in world['COUNTRY'].to_list():
   ##     print(index+':is not in the list')
    ##else:
     ##   pass
 
merge = world.join(data, on ='COUNTRY', how = 'right')

image_frames=[]

for dates in merge.columns.to_list()[2:468]:

    ax=merge.plot(column = dates,
                  cmap = 'OrRd',
                  figsize = (25,25),
                  legend = True,
                  scheme = 'user_defined',
                  classification_kwds = {'bins':[10,20,50,100,500,1000,5000,10000,500000]},
                  edgecolor = 'black',
                  linewidth = 0.4)

    ax.set_title('Total Confirmed Coronavirus Cases'+dates, fontdict =
             {'fontsize':20}, pad =12.5)

    ax.set_axis_off()

    ax.get_legend().set_bbox_to_anchor((0.18,0.6))
    
    img = ax.get_figure()
    
    f=io.BytesIO()
    img.savefig(f, format = 'png',bbox_inches='tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))
    


image_frames[0].save('Dynamic COVID-19 Map.gif', format = 'GIF',
                     append_images = image_frames[1:],
                     save_all = True, duration = 300,
                     loop = 0)

f.close()
