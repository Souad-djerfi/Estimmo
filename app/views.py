# coding: utf8
from app import app
from flask import render_template, request, abort, redirect, url_for, flash
import datetime
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from app import models
from joblib import load
from app import rechercheBien, factory_bien, prix_med

app.config.update(SECRET_KEY  = 'ma cle secrete')


# C'est ici qu'on demande à notre appli flask d'acheminer toutes les demandes d'URL à la racine vers la fonction index()
# A chaque fois qu'on ouvrira un navigateur pour accéder à l'indexe, c'est cette fonction qui sera appelé
# @app.route est un décorateur de la varibale app qui va encapsuler la fonction index() et acheminer les demande vers cette fonction

@app.route('/')
def index():
    #date = datetime.datetime.now().strftime("%x %X")
    return render_template( 'index.html')

@app.route('/dashboard')
def dashboard():
    models.graphique()
    date = datetime.datetime.now().strftime("%x %X")
    return render_template( 'Pages/dashboard.html', date=date)

@app.route('/estimation_bien',methods=['GET','post'])    
def estimation_bien():
    income=request.form['Median_income']
    tRooms=request.form['Total_rooms']
    ocean_proximity=request.form['Ocean_proximity']
    model = load('D:\IA\Projet-Certif-Agile\save_model\housing_regression_model_saved1.joblib')
    prediction = round(model.predict([[float(income), float(ocean_proximity)]])[0],2)
    l_ocean_proximity={'0':'NEAR BAY','1':'<1H OCEAN','2':'INLAND','3':'NEAR OCEAN','4':'ISLAND'}
    data={'income':income,
           'tRooms':tRooms,
           'ocean_proximity':l_ocean_proximity[ocean_proximity],
           'predict':prediction
           }
    return render_template('Pages/prediction.html',**data)        

@app.route('/recherche',methods=['POST','GET']) 
def recherche():
    filtre=pd.DataFrame()
    total_data=rechercheBien.filtre()
    if request.method=='POST':
        proximity=request.form.getlist('Ocean_proximity')
        
        for pr in proximity:
            filtre=filtre.append(total_data[total_data[11]==pr] )
            
        if request.form['population'] !='':
            
            population=float(request.form['population'])
            filtre=filtre[filtre[6]>population]
             
        if request.form['trooms']!='':
            trooms=float(request.form['trooms'])   
            filtre=filtre[filtre[4]>trooms] 
        if  request.form['mincome']!='':
            mincome=float(request.form['mincome'])
            filtre=filtre[filtre[8]>mincome]
    if filtre.empty:
            filtre=total_data[:100]     
    
    data={'filtre':filtre,
            'nbre_ligne':filtre.shape[0]}
    
    return render_template('Pages/recherche.html',**data)     

@app.route('/modifier_bien',methods=['POST','GET']) 
def modifier_bien(): 
    return render_template('Pages/recherche.html')  

@app.route('/supprimer_bien',methods=['POST','GET']) 
def supprimer_bien(): 
    return render_template('Pages/recherche.html')  

    
@app.route('/ajout_bien', methods = ['POST', 'GET'])
def ajout_bien():
    
    ocean_proxi=""
    longtitude=""
    latitude=""
    median_age=""
    total_rooms=""
    total_bedrooms=""
    population=""
    house_hold=""
    median_income=""
    median_house_value=""
    if request.method == 'POST':
        
        #récupere tous les champs de formulaire
        ocean_proxi = request.form['ocean_proxi']
        longtitude = request.form['longtitude']
        latitude = request.form['latitude']
        median_age = request.form['median_age']
        total_rooms = request.form['total_rooms']
        total_bedrooms = request.form['total_bedrooms']
        population = request.form['population']
        house_hold = request.form['house_hold']
        median_income = request.form['median_income']

        ocean_proxi_str = factory_bien.proximity_str(float(ocean_proxi))#Conversion proximity_str
        #load modèle préditif
        model = load('D:\IA\Projet-Certif-Agile\save_model\housing_regression_model_saved1.joblib')
        median_house_value = round(model.predict([[float(median_income), float(ocean_proxi)]])[0],2)
        #if request.form['Estimer_ajouter']=="Estimer_bien":
          
        if request.form['Estimer_ajouter']=="ajouter_bien":    
            nouveau_bien = prix_med.Prix_Median(float(longtitude), float(latitude), float(median_age), float(total_rooms), float(total_bedrooms), 
                            float(population), int(house_hold), float(median_income), median_house_value, int(ocean_proxi), ocean_proxi_str)
            factory_bien.ajout_nv_bien(nouveau_bien)
            flash("Le bien a été bien ajouté!",'success') 
            return redirect(url_for('ajout_bien'))

    data={'longtitude':longtitude,
            'latitude':latitude,
            'median_age':median_age,
            'total_rooms':total_rooms,
            'total_bedrooms':total_bedrooms,
            'population':population,
            'house_hold':house_hold,
            'median_income':median_income,
            'median_house_value':median_house_value
            }    
    return render_template("Pages/ajout_bien.html", **data)    


"""@app.route('/ajout_bien', methods = ['POST', 'GET'])
def ajout_bien():
    if request.method == 'POST':
        #récupere tous les champs de formulaire
        ocean_proxi = request.form['ocean_proxi']
        longtitude = request.form['longtitude']
        latitude = request.form['latitude']
        median_age = request.form['median_age']
        total_rooms = request.form['total_rooms']
        total_bedrooms = request.form['total_bedrooms']
        population = request.form['population']
        house_hold = request.form['house_hold']
        median_income = request.form['median_income']
        ocean_proxi_str = factory_bien.proximity_str(float(ocean_proxi))
        print("oceannnnnnnnnnnnnnnnnn",ocean_proxi_str)
        #load modèle préditif
        model = load('D:\IA\Projet-Certif-Agile\save_model\housing_regression_model_saved1.joblib')
        median_house_value = round(model.predict([[float(median_income), float(ocean_proxi)]])[0],2)
        nouveau_bien = prix_med.Prix_Median(float(longtitude), float(latitude), float(median_age), float(total_rooms), float(total_bedrooms), 
                            float(population), int(house_hold), float(median_income), median_house_value, int(ocean_proxi), ocean_proxi_str)
        factory_bien.ajout_nv_bien(nouveau_bien)
    return render_template("Pages/ajout_bien.html")"""
       
@app.route('/estim_ajout_bien', methods = ['POST', 'GET'])
def estim_ajout_bien():  
    print("coucoucocuocucocoucoucoucocuocucoucocuocucou")
    return render_template("Pages/ajout_bien.html")     