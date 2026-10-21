import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error,r2_score

df=pd.read_csv('crop_yield.csv')
df['Season']=df['Season'].str.strip().str.lower()
df['State']=df['State'].str.strip().str.lower()
df['Crop']=df['Crop'].str.strip()

x=df[[
        'Crop','Crop_Year','Season','State',
        'Area','Annual_Rainfall','Fertilizer',
        'Pesticide']]
y=df['Yield']

categorical_f=['Crop','Season','State']
numerical_f=['Crop_Year','Area','Annual_Rainfall','Fertilizer','Pesticide']

preprocessor=ColumnTransformer(
    transformers=[
        ('categorical',OneHotEncoder(handle_unknown='ignore'),categorical_f),
        ('numerical','passthrough',numerical_f)
    ]
)

model=RandomForestRegressor(
    n_estimators=200,random_state=42,n_jobs=-1)

pipeline=Pipeline(
    steps=[
        ('preprocessor',preprocessor),
        ('model',model)
    ]
)

x_train,x_test,y_train,y_test=train_test_split(
    x,y,test_size=0.2,random_state=42
)

pipeline.fit(x_train,y_train)

predictions=pipeline.predict(x_test)
mae=mean_absolute_error(y_test,predictions)
r2=r2_score(y_test,predictions)

print('model trained successfully!')
print(f'MAE:{mae:.2f}')
print(f'R2 score:{r2:.2f}')

with open('model.pkl','wb') as file:
    pickle.dump(pipeline,file)
print('model saved as model.pkl')