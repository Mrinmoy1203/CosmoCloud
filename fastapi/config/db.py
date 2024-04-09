from pymongo import MongoClient
#conn=MongoClient("mongodb+srv://Mrinmoy1203:AWvI0a4tzzAbXmsx@cluster0.evaeote.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0n")
conn=MongoClient("mongodb+srv://Mrinmoy1203:AWvI0a4tzzAbXmsx@cluster0.evaeote.mongodb.net/")
db = conn["Adree"]
collection = db["col"]
