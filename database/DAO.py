from database.DB_connect import DBConnect
from model.go_products import Prodotto
from model.go_retailers import Retailer


class DAO:
    @staticmethod
    def getAnni():
        cnx= DBConnect.get_connection()
        cursor = cnx.cursor()
        query= "SELECT distinct YEAR(`Date`) AS Year FROM go_daily_sales"
        cursor.execute(query)

        anni = []
        for row in cursor:
            anni.append(row[0])

        cursor.close()
        cnx.close()
        return anni

    @staticmethod
    def getBrand():
        cnx= DBConnect.get_connection()
        cursor= cnx.cursor()
        query = "SELECT distinct Product_brand FROM go_products"
        cursor.execute(query)
        brand = []
        for b in cursor:
            brand.append(b[0])
        cursor.close()
        cnx.close()

        return brand

    @staticmethod
    def getRetailers():
        cnx= DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM go_retailers"
        cursor.execute(query)

        retailers = []
        for row in cursor:
            retailers.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"]))
        #prodotti = cursor.fetchall()

        cursor.close()
        cnx.close()
        return retailers

    @staticmethod
    def getTopVendite(anno, brand, retailer_code):
        cnx= DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Assicuriamoci che se anno è una stringa vuota diventi None
        if anno == "" or anno is None:
            anno = None
        else:
            anno = int(anno)  # Forza il cast a intero per YEAR()

        query = """
                SELECT s.Date, p.Product_brand, r.Retailer_name, (s.Unit_sale_price * s.Quantity) AS revenue 
                FROM go_daily_sales s 
                JOIN go_products p ON s.Product_number = p.Product_number 
                JOIN go_retailers r ON s.Retailer_code = r.Retailer_code 
                WHERE YEAR(s.Date) = COALESCE(%s, YEAR(s.Date)) 
                  AND p.Product_brand = COALESCE(%s, p.Product_brand) 
                  AND r.Retailer_code = COALESCE(%s, r.Retailer_code) 
                ORDER BY revenue DESC 
                LIMIT 5
            """

        # Passiamo ogni parametro una sola volta
        cursor.execute(query, (anno, brand, retailer_code))
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_analisi_vendite(anno, brand, retailer_code):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        if anno == "" or anno is None:
            anno = None
        else:
            anno = int(anno)

        # Query che recupera i dati necessari per le statistiche
        query = """
                SELECT s.Unit_sale_price, s.Quantity, s.Retailer_code, s.Product_number
                FROM go_daily_sales s
                JOIN go_products p ON s.Product_number = p.Product_number
                WHERE YEAR(s.Date) = COALESCE(%s, YEAR(s.Date))
                  AND p.Product_brand = COALESCE(%s, p.Product_brand)
                  AND s.Retailer_code = COALESCE(%s, s.Retailer_code)
            """
        cursor.execute(query, (anno, brand, retailer_code))
        #cursor.execute(query, (anno, anno, brand, brand, retailer_code, retailer_code))
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result