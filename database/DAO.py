from database.DB_connect import DBConnect
from model.address import Address
from model.fornitore import Fornitore
from model.product import Product


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
                    HAVING numero_ID_NIL < 1200 AND numero_ID_NIL > 100
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

    @staticmethod
    def getAllProducts():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select i.item_id , i.name, i.category, i.price, i.short_description, i.depth, i.height, i.width
                    from tesi299809.ikeaproducts i 
                    where i.`depth` is not null and i.height is not null and i.width is not null"""
        cursor.execute(query, )
        for row in cursor:
            result.append(Product(row['item_id'], row['name'], row['category'], row['price'], row['short_description'], row['depth'], row['height'], row['width']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllFornitori():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from tesi299809.fornitori f """
        cursor.execute(query, )
        for row in cursor:
            result.append(Fornitore(**row))
        cursor.close()
        conn.close()
        return result