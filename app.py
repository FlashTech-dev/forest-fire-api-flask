from imp import load_module
from xml.etree.ElementTree import tostring
from flask import Flask, jsonify, render_template, request
import pandas as pd
app = Flask(__name__, template_folder='template')
import pickle
import numpy as np
import joblib
def DataPrediction(data):
  test_df = pd.DataFrame() 
  for i in range(3):
    SampleModel = joblib.load('pickle/SampleModel_'+ str(i) + '.pkl')
    predictedValues = SampleModel.predict(data)
    columnName = 'predict' + str(i)
    test_df[columnName] = predictedValues

  test_finalPrediction = []
  for j in range(len(test_df)):
    row_list = test_df.iloc[j].values.tolist()
    majority_count = max(set(row_list) , key=row_list.count)
    test_finalPrediction.append(majority_count)

  test_finalPrediction = np.array(test_finalPrediction)
  return(test_finalPrediction)



@app.route('/api',methods = ['POST'])
def api():
  
    df=pd.DataFrame({"SOURCE_SYSTEM_TYPE":[request.get_json()["SOURCE_SYSTEM_TYPE"]],
    "SOURCE_SYSTEM":[request.get_json()["SOURCE_SYSTEM"]],
    "NWCG_REPORTING_AGENCY":[request.get_json()["NWCG_REPORTING_AGENCY"]],
    "FIRE_YEAR":[request.get_json()["FIRE_YEAR"]],
    "STAT_CAUSE_CODE":[request.get_json()["STAT_CAUSE_CODE"]],
    "LATITUDE":[request.get_json()["LATITUDE"]],
    "LONGITUDE":[request.get_json()["LONGITUDE"]],
    "OWNER_CODE":[request.get_json()["OWNER_CODE"]],
    "STATE":[request.get_json()["STATE"]],
    "DISCOVERY_MONTH":[request.get_json()["DISCOVERY_MONTH"]],
    "DISCOVERY_TOD":[request.get_json()["DISCOVERY_TOD"]],
    "STATE_PRCNT_FOREST":[request.get_json()["STATE_PRCNT_FOREST"]],
    "AVG_TEMP":[request.get_json()["AVG_TEMP"]],
    "AVG_PREC":[request.get_json()["AVG_PREC"]]})

    predictions = DataPrediction(df)
    df['PREDICTED_CLASS'] = predictions
  #Simplifying the predicted class by giving area covered in each class
    predictedRange = []
    for i in range(len(df)):
        key = df.iloc[i]['PREDICTED_CLASS']
        if   ( key == 1 ):
            predictedRange.append('0-0.25 acres')
        elif ( key == 2 ):
            predictedRange.append('0.26-9.9 acres')
        elif ( key == 3 ):
            predictedRange.append('10.0-99.9 acres')
        elif ( key == 4 ):
            predictedRange.append('100-299 acres')
        elif ( key == 5 ):
            predictedRange.append('300-999 acres')
        elif ( key == 6 ):
            predictedRange.append('1000-5000 acres')
        else:
            predictedRange.append('5000+ acres')
    
    df['Area Range'] = predictedRange
    return (df.to_string())

   


if __name__ == '__main__':
    app.run(debug=True)
