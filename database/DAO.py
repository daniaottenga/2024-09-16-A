from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getLL():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select Lat, Lng 
from state"""
            cursor.execute(query)

            maxLat = 0
            maxLng = 0
            minLat = 10000
            minLng = 10000
            for row in cursor:
                if row["Lat"] > maxLat:
                    maxLat = row["Lat"]
                if row["Lng"] > maxLng:
                    maxLng = row["Lng"]
                if row["Lat"] < minLat:
                    minLat = row["Lat"]
                if row["Lng"] < minLng:
                    minLng = row["Lng"]

            result = [maxLat, minLat, maxLng, minLng]

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getShape():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select DISTINCT(shape) 
from sighting 
where shape <> "unknown" """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(lat, long, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
from state
where Lat > %s and Lng > %s and id in (select state from sighting where shape = %s) """
            cursor.execute(query, (lat, long, shape))

            for row in cursor:
                neigh = row["Neighbors"].split(" ")
                result.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], neigh))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(lat, long, shape):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select tab1.state s1, tab2.state s2, d1+d2 somma
from (select state, sum(duration) d1
from sighting
group by state) tab1, (select state, sum(duration) d2
from sighting
group by state) tab2
where tab1.state < tab2.state and tab1.state in (select id
from state
where Lat > %s and Lng > %s and id in (select state from sighting where shape = %s)) and tab2.state in (select id
from state
where Lat > %s and Lng > %s and id in (select state from sighting where shape = %s))
group by tab1.state, tab2.state"""
            cursor.execute(query, (lat, long, shape, lat, long, shape))

            for row in cursor:
                result[(row["s1"], row["s2"])] = row["somma"]

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result




