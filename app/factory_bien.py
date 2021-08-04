from pandas.core.frame import DataFrame
from app.base import Base, Session, engine
from app.prix_med import Prix_Median


#{1,	"<1H OCEAN"}
#2	"INLAND"
#3	"NEAR OCEAN"
#4	"ISLAND"
#0	"NEAR BAY"

Base.metadata.create_all(engine)

def read_long_lat_proxi():
    """
        SELECT * FROM prix_median
        --> extraire tous les biens de BD
        Return: list de bien 
    """
    session = Session()
    # data est une liste de tuple
    long_lat_proxi_data = session.query(Prix_Median.longitude,
                         Prix_Median.latitude,
                         Prix_Median.ocean_proximity_str,
                         Prix_Median.ocean_proximity).all()
    session.close()
    list_long_lat = DataFrame(long_lat_proxi_data)
    list_long_lat = list_long_lat.drop_duplicates()
    return list_long_lat
 


def ajout_nv_bien(nvbien: Prix_Median):
    session = Session()
    #verifie la table 'prix_median exist dans DB ou non
    #si non, on va la crÃ©er 
    if not (engine.has_table('prix_median')):
         engine.create_all()
    
    session.add(nvbien)
    session.commit()
    session.close()
    print('ajout a termine !')
    
def proximity_str(proximity_num):
    session = Session()
    ocean_proxi = session.query(Prix_Median.ocean_proximity_str,
                         Prix_Median.ocean_proximity).all() 
    session.close()
    list_ocean_proxi = DataFrame(ocean_proxi).drop_duplicates().reset_index().drop(columns='index')
    print(list_ocean_proxi)
    #list_ocean_proxi = list_ocean_proxi.rename(columns={'0': 'proximi_str', '1': 'proximi'})
    a = list_ocean_proxi[0][list_ocean_proxi[1]==proximity_num]
    return a.values[0]
    