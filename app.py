from flask import Flask,render_template,request
import pickle
from sklearn.preprocessing import StandardScaler
import numpy as np

model = pickle.load(open(r"C:\Users\veda keerthi\My_personal_files\CODING FILES\MY PROGRAMS\PYTHON\Python_programs\Project\Vehicle price prediction\Car_prediction.pkl",'rb'))
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('vehicle_prediction.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    
    if request.method =='POST':
        diesel,electric,lpg,individual,trustmark_dealer,manual,owner_fourth,owner_second,owner_testdrive,owner_third = 0,0,0,0,0,0,0,0,0,0
        years = int(request.form['year'])
        km_driven = int(request.form['km_driven'])
        km_driven2 = np.log(km_driven)
        fuel_type = request.form['fuel_type']
        if fuel_type =='Petrol':
            petrol=1
            diesel,cng,lpg,electric = 0,0,0,0
        elif fuel_type =='Diesel':
            diesel = 1
            petrol,cng,lpg,electric = 0,0,0,0
        elif fuel_type =='CNG':
            cng = 1
            petrol,diesel,lpg,electric = 0,0,0,0
        elif fuel_type =='LPG':
            lpg = 1
            petrol,diesel,cng,electric=0,0,0,0
        else:
            electric = 1
            petrol,diesel,cng,lpg = 0,0,0,0
        
        seller_type = request.form['seller_type']
        if seller_type == 'Individual':
            individual = 1
        else:
            trustmark_dealer = 1
            
        transmission_manual = request.form['transmission_transmission']
        if transmission_manual =='Manual':
            manual = 1
        else:
            manual = 0
            
        owner = request.form['owner_type']
        if owner =='Test_drive_car':
            owner_testdrive = 1
            owner_fourth, owner_second, owner_third = 0,0,0
        elif owner =='Second_owner':
            owner_second = 1
            owner_fourth,owner_third,owner_testdrive = 0,0,0
        elif owner=='Third_owner':
            owner_third = 1
            owner_fourth,owner_second,owner_testdrive = 0,0,0
        elif owner =='Fourth&Above_owner':
            owner_fourth = 1
            owner_second,owner_third,owner_testdrive = 0,0,0
        else:
            owner_second,owner_third,owner_fourth,owner_testdrive=0,0,0,0
        
        prediction = model.predict([[years,km_driven2,diesel,electric,lpg,
                            individual,trustmark_dealer,manual,
                            owner_fourth,owner_second,
                            owner_testdrive,owner_third]])
        output = round(prediction[0],2)
        if output<=0:
            return render_template('vehicle_prediction.html',result='Sorry you cannot sell this car')
        else:
            return render_template('vehicle_prediction.html',result='You can sell this car at a rate of : {} Lakhs'.format(output))
    else:
        return render_template('vehicle_prediction.html')
    
if __name__ == '__main__':
    app.run()