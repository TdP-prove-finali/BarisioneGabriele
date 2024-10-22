from database.DB_connect import DBConnect
from model.Address import Address


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllQuartiere():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT NIL, COUNT(DISTINCT CONCAT(NUMERO, TIPO, ANNCSU)) AS numero_ID_NIL, ID_NIL
                    FROM tesi299809.civicmilano
                    WHERE ID_NIL IS NOT NULL
                    GROUP BY NIL
                    ORDER BY ID_NIL  """
        cursor.execute(query, )
        for row in cursor:
            result.append([row["ID_NIL"], row["NIL"], row["numero_ID_NIL"]])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAddressSpecifcQuartiere(SelQuartiere):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select CODICE_VIA ,NUMERO ,TIPO , ANNCSU ,ID_NIL,  NIL , LAT_WGS84 , LONG_WGS84  
                    from tesi299809.civicmilano n 
                    where n.ID_NIL = %s
                    group by n.NUMERO , n.TIPO, n.ANNCSU
                    order by n.ANNCSU, n.NUMERO   """
        cursor.execute(query, (SelQuartiere[0], ))
        for row in cursor:
            result.append(Address(**row))
        cursor.close()
        conn.close()
        return result