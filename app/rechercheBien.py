# coding: utf8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import load

from app.base import Base, Session, engine
from app.prix_med import Prix_Median


def filtre():
    Base.metadata.create_all(engine)
    session = Session()
    # data est une liste de tuple
    data = session.query(Prix_Median.id_prix_median,
                         Prix_Median.longitude,
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
    return df_data