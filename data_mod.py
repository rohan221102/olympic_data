# id,name,sex,age,height,weight,team,noc,games,year,season,city,sport,event,medal
import pandas as pd

def read_data():
    data = pd.read_csv('olympics.csv')
    return data

# Number of medals won and number of athletes by each country and stored to countries.csv
def count_medals(data):
    countries = data['noc'].unique()
    medals = []
    athletes = []
    for country in countries:
        medals.append(data[(data['noc'] == country) & (data['medal'].notnull())].shape[0])
        athletes.append(data[(data['noc'] == country)]['id'].nunique())
    countries = pd.DataFrame({'noc': countries, 'medals': medals, 'athletes': athletes})
    countries.to_csv('countries.csv', index=False)

# Year, season, country, average male height, average female height, average male weight, average female weight, medals
def avg_height_weight(data):
    data = data[data['height'].notnull()]
    data = data[data['weight'].notnull()]
    
    male_data = data[data['sex'] == 'M']
    female_data = data[data['sex'] == 'F']
    
    male_avg = male_data.groupby(['year', 'season', 'noc']).agg({'height': 'mean', 'weight': 'mean'}).reset_index()
    female_avg = female_data.groupby(['year', 'season', 'noc']).agg({'height': 'mean', 'weight': 'mean'}).reset_index()
    
    avg_data = pd.merge(male_avg, female_avg, on=['year', 'season', 'noc'], suffixes=('_male', '_female'))
    
    avg_data['height_male'] = avg_data['height_male'].round(2)
    avg_data['weight_male'] = avg_data['weight_male'].round(2)
    avg_data['height_female'] = avg_data['height_female'].round(2)
    avg_data['weight_female'] = avg_data['weight_female'].round(2)
    
    # Count the number of medals won that year
    medals_data = data[data['medal'].notnull()]
    medals_count = medals_data.groupby(['year', 'season', 'noc']).size().reset_index(name='medals')
    
    avg_data = pd.merge(avg_data, medals_count, on=['year', 'season', 'noc'], how='left')
    avg_data['medals'] = avg_data['medals'].fillna(0).astype(int)
    
    avg_data.to_csv('height_weight.csv', index=False)

count_medals(read_data())
avg_height_weight(read_data())