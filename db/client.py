from pymongo import MongoClient

#Base de datos local
#db_client = MongoClient().local

#Base de datos en la nube
db_client = MongoClient("mongodb+srv://jesusdanielgonzalez121:0Id9CDWMsO4JhbnS@cluster0.hkyib.mongodb.net/").local



