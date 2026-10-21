import pandas as pd
import pickle

df=pd.read_csv('crop_yield.csv')
df['Season']=df['Season'].str.strip().str.lower()
df['State']=df['State'].str.strip().str.lower()
df['Crop']=df['Crop'].str.strip()

with open('model.pkl','rb') as file:
    model=pickle.load(file)

def recommend_crops(state,season,area,rainfall,top_n=3):
    state=state.strip().lower()
    season=season.strip().lower()
    data=df[
        (df['State']==state) &
        (df['Season']==season)
    ]
    if data.empty:
        return []
    crops=data['Crop'].unique()
    predictions=[]
    latest_year=int(df['Crop_Year'].max())
    for crop in crops:
        crop_data=data[data['Crop']==crop]
        avg_fert=crop_data['Fertilizer'].mean()
        avg_pest=crop_data['Pesticide'].mean()
        input_data=pd.DataFrame([{
            'Crop':crop,'Crop_Year':latest_year,'Season':season,
            'State':state,'Area':area,'Annual_Rainfall':rainfall,
            'Fertilizer':avg_fert,'Pesticide':avg_pest
        }])
        predicted_yield=model.predict(input_data)[0]
        predictions.append({
            'Crop':crop,'predicted_yield':round(float(predicted_yield),2)
        })

    predictions.sort(
        key=lambda x:x['predicted_yield'],
        reverse=True
    )
    recommendations=predictions[:top_n]
    for rank,recommendation in enumerate(recommendations,start=1):
        recommendation['rank']=rank
    return recommendations
def get_options():

    combinations = (
        df[['State', 'Season']]
        .drop_duplicates()
        .sort_values(['State', 'Season'])
    )

    options = {}

    for _, row in combinations.iterrows():

        state = row['State']
        season = row['Season']

        if state not in options:
            options[state] = []

        options[state].append(season)

    return options