## Snapshot Configuration for ES


### Manual Configuration

* Take the zip file and extract it in your local system ; you must need python 3

```
unzip es-manager.zip
```

* Export these environment variables in your system before run the python script

**Note : "snapdeldays" and "snaprepo" are optional and it required only when you pass "myenv=production" to take snapshots and store it in blobe storage, otherwise it will just check the indices and delete which older than "indicesdeldays"**

```
export myenv=development
export host="http://10.50.144.190:9200/"
export indicesdeldays=90
export snaprepo=development-elasticsearch-storage
export snapdeldays=180
```

* Activate the python virtualenv

```
cd es-manager/
source ./bin/activate
```

* Run the python script and check the logs....!!!

```
python3 snapshot.py
```
* Deactivate and exit from the environment

```
deactivate
```

### Kubernetes cronjab with configmap

**For kubernetes cornjob, you have to create the configmap with the zip file and then create the cronjob with "es-snapshots-cronjob.yaml"**

```
kubectl -n elasticsearch create configmap snapshot-cm --from-file snapshot.py
```