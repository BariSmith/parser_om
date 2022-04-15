'''D. Считать содержимое файла из пункта А, создать программно 
базу данных mongodb, сохранить все данные в коллекцию. 
Средствами mongo удалить записи, в которых в третьем столбце 
первый символ буква.'''

from pymongo.operations import DeleteOne
import pandas as pd
from pymongo import MongoClient
import json




def mongoimport(csv_path='/home/vadym_a/Documents/tcsv.csv',
                db_name="myData", 
                db_url='127.0.0.1', 
                db_port=27017):
    
    
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    col = db["table3mg"]
    data = pd.read_csv(csv_path)
    payload = json.loads(data.to_json(orient='records'))
    col.remove()
    col.insert(payload)
    return col.count()
    #Далі написано видалення всіх записів із 2ї колонки, 
    # але в мене не спрацьовує $regex хоч за документацією все правильно
    # myquery = db.col.find({ "C": {$regex: [/^A-Z/]}})
    # col.DeleteOne(myquery)

mongoimport()