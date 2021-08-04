# coding: utf8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import load

from app.base import Base, Session, engine
from app.prix_med import Prix_Median


def graphique():
    Base.metadata.create_all(engine)
    session = Session()
    # data est une liste de tuple
    data = session.query(Prix_Median.longitude,
                         Prix_Median.latitude,
                         Prix_Median.housing_median_age,
                         Prix_Median.total_rooms,
                         Prix_Median.total_bedrooms,
                         Prix_Median.population,
                         Prix_Median.households,
                         Prix_Median.median_income,
                         Prix_Median.median_house_value,
                         Prix_Median.ocean_proximity,
                         Prix_Median.ocean_proximity_str).all()
    session.close()

    df_data = pd.DataFrame(data).dropna()
    df_data=df_data.rename(columns = {0: 'longitude', 1: 'latitude',2: 'housing_median_age',3: 'total_rooms',4: 'total_bedrooms',5: 'population',6: 'households',7: 'median_income',8: 'median_house_value',9: 'ocean_proximity',10:'ocean_proximity_str'})
    palette=sns.color_palette("Paired")
    sns.set_palette(palette)

    plt.figure(figsize=[15,20])
    plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.5)

    plt.subplot(421)
    sns.scatterplot(data=df_data, x="longitude", y="latitude", hue="median_house_value")
    plt.title("Distribution géographique des prix médians")
    plt.xticks(rotation=45)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.axis("scaled")

    plt.subplot(422)
    sns.scatterplot(data=df_data, x="median_house_value", y="median_income", hue="ocean_proximity_str")
    plt.title("Distribution des prix médians suivant les salaires médians")
    plt.xticks(rotation=45)
    plt.xlabel('Prix médians en $')
    plt.ylabel('Salaires médians')

    plt.subplot(423)
    sns.histplot(data=df_data, x="total_rooms", kde=True)
    plt.title("Distribution des biens suivant leur surface totale (in²)")
    plt.xticks(rotation=45)
    plt.xlim(0, 12000)
    plt.xlabel('Surface totale (in²)')

    plt.subplot(424)
    sns.histplot(data=df_data, x="total_bedrooms", kde=True)
    plt.title("Distribution des biens suivant la surface des chambres (in²)")
    plt.xticks(rotation=45)
    plt.xlim(0, 2000)
    plt.xlabel('Surface chambres (in²)')

    plt.subplot(425)
    sns.histplot(data=df_data, x="population", kde=True)
    plt.title("Distribution des biens suivant la population")
    plt.xticks(rotation=45)
    plt.xlim(0, 4000)
    plt.xlabel('Polulation')

    plt.subplot(426)
    sns.histplot(data=df_data, x="households", kde=True)
    plt.title("Distribution des biens suivant le nb de foyer du quartier")
    plt.xticks(rotation=45)
    plt.xlim(0, 2000)
    plt.xlabel('Nb de foyer')

    plt.subplot(427)
    sns.histplot(data=df_data, x="median_income", kde=True)
    plt.title("Distribution des biens sur les revenus médians")
    plt.xticks(rotation=45)
    plt.xlabel('Revenu médian en m$')

    plt.subplot(428)
    sns.histplot(data=df_data, x="housing_median_age", kde=True)
    plt.title("Distribution des biens suivant leur age médian")
    plt.xticks(rotation=45)
    plt.xlabel('Age médian')

    plt.savefig("app/static/Image/dashboard.png")
    
    return None


    def prediction(mincome, oceanP):
        # load model et return prediction
        model = load('D:\IA\Projet-Certif-Agile\save_model\housing_regression_model_saved.joblib')
        x = model.predict([[mincome, oceanP]])[0]
        return round(x,2)