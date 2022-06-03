import rom pystalk import BeanstalkClient
import json
import requests

client = BeanstalkClient('127.0.0.1', 11300)

TUBE_NAME='alprd' #alprd nom tube par defaut module alprd

client.watch(TUBE_NAME)

url = "http://192.168.5.64/ProjetBTS-master/FonctionsAPIbis.php/"

while True:

    # Wait for a second to get a job. If there is a job, process it and delete it from the queue.
    # If not, return to sleep.
    job = client.reserve_job()

    if job is None:
        print ("Aucune plaque detecté, patience...")

    else:
        print ("------------------------------------------------------")
        plates_info = json.loads(job.job_data) # convert it into a Python Dictionary
        json_string = json.dumps(plates_info) # convert a python object into an equivalent JSON object
        json_str = json.dumps(json_string, indent=4, sort_keys=True) #formate

        with open("data.json", "a+") as f:
                f.write(json_str)
                f.write("\n")
                f.close()

        with open("data.json", "r") as f:
                data = plates_info
                r1 = requests.get("http://192.168.5.64/ProjetBTS-master/api.php/get")
                r2 = requests.get(url)
                api1 = r1.json() #converted to JSON object
                api2 = r2.json()
                lenght = len(api2)

                for i in api1:
                        for j in api2:
                                for k in data['results']:
                                        if (i['Plaque']==k['plate']):
                                                for element in lenght:
                                                        if (j['Park_plaque']==k['plate']):
                                                                if (j['Car_presence']==1):
                                                                        Plaque1 = j['plate']
                                                                        Rput1 = requests.put(url, data = {'Park_plaque' : Plaque1, 'Car_presence' : 0})
                                                                        print (Rput1.text)
                                                                        print ('La voiture est sortie')
                                                                        break
                                                                else:
                                                                        Plaque2 = j['plate']
                                                                        Rput2 = requests.put(url , data = {'Park_plaque' : Plaque2, 'Car_presence' : 1})
                                                                        print (Rput2.text)
                                                                        print ('Ouvrir le portail')
                                                                        print ('Sortie de voiture confirmée')
                                                                        break
                                                        break
                                                break
                                        break
                                break
                        break
                f.close()
        client.delete_job(job.job_id)

