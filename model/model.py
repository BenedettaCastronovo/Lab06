from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getAnni()

    def getBrand(self):
        return DAO.getBrand()

    def getRetailers(self):
        return DAO.getRetailers()

    def getTopVendite(self, anno, brand, retailer):
        return DAO.getTopVendite(anno, brand, retailer)

    def get_analisi_vendite(self, anno, brand, retailer_code):
        return DAO.get_analisi_vendite(anno, brand, retailer_code)