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
            query = """select shape 
from sighting 
where shape <> "" """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])

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




