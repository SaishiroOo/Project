from pystalk import BeanstalkClient
import json
import requests

client = BeanstalkClient('127.0.0.1', 11300)

TUBE_NAME='alprd' #alprd nom tube par defaut module alprd

client.watch(TUBE_NAME)

url = "http://192.168.5.64/ProjetBTS-master/FonctionsAPIbis.php/"

while True:

    # Wait for a second to get a job. If there is a job, process it and delete it from the queue.
    # If not, return to sleep.
    job = client.reserve_job(timeout=1.0)

    if job is None:
        print ("Aucune plaque detecté, patience...")

    else:
        print ("------------------------------------------------------")
        plates_info = json.loads(job.job_data) # convert it into a Python Dictionary
        json_string = json.dumps(plates_info) # convert a python object into an equivalent JSON object
        json_str = json.dumps(json_string, indent=2, sort_keys=True) #formate
        with open("data.json", "a+") as f:
                f.write(json_str)
                f.write("\n")
                f.close()

        with open("data.json", "r") as f:
                data = plates_info

                r = requests.get("http://192.168.5.64/ProjetBTS-master/api.php/get")
                api = r.json() #converted to JSON object
                for i in api:
                        for j in data['results']:
                                if (i['Plaque']==j['plate']):
                                        Plaque = j['plate']
                                        Rpost = requests.post(url , data = {'Park_plaque' : Plaque, 'Car_presence' : '1'})
                                        print(Rpost.text)
                                        break
                                else:
                                        print ('ne pas ouvrir le portail')
                                        break
                        if (i['Plaque']==j['plate']):
                                 print ('ouvrir le portail')
                                 print ('la voiture est rentrée')
                                 break
                        else:
                                 break
        client.delete_job(job.job_id)
