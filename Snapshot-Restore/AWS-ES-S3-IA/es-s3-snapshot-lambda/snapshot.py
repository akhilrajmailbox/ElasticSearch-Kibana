import boto3
import requests
import time
import os

def snapshot(event, context):
    # snapshot.snapshot > call from lambda
    myenv=os.environ['myenv']
    host=os.environ['host']
    indicesdeldays=int(os.environ['indicesdeldays'])


    indicesfilter = "_cat/indices/prefix-*?h=i,cd"
    deleteindicesepoch = int(round((time.time() - 60*60*24*indicesdeldays) * 1000)) # epoch time for 90 days before from present time
    service = 'es'
    headers = {"Content-Type": "application/json"}
    waitcompletion = "?wait_for_completion=true"


    ## deleting indices
    getindices = host + indicesfilter
    getindicesrequest = requests.get(getindices)


    for i in getindicesrequest.text.strip().split('\n'):

            delindicename = str(i.split(' ')[0])
            delindiceepoch = int(i.split(' ')[-1])
            if delindiceepoch <= deleteindicesepoch:
                print(delindicename + " deleting...")
                deleteindices = host + delindicename
                deleteindicesrequest = requests.delete(deleteindices)
                print(deleteindicesrequest.status_code)
                print(deleteindicesrequest.text)
            else:
                print(delindicename + " is not going to delete now.....")


    ## creating and deleting snapshots
    if myenv == "production":
        # Create snapshots
        snaprepo=os.environ['snaprepo']
        snappath='_snapshot/' + snaprepo + '/'
        snapurl = host + snappath
        createsnapshotsuffix = int(round(time.time() * 1000))
        createsnapshotname = "snapshot-" + str(createsnapshotsuffix)

        snapcreateurl = snapurl + createsnapshotname + waitcompletion
        snaprequest = requests.put(snapcreateurl, data='{"indices": "prefix-prod-*"}', headers=headers)
        print(snaprequest.status_code)
        print(snaprequest.text)

        # Delete snapshots
        snapdeldays=int(os.environ['snapdeldays'])
        getsnappath='_cat/snapshots/' + snaprepo + '/'
        deletesnapepoch = int(round(time.time() - 60*60*24*snapdeldays))
        snapfilter = "?h=id,start_epoch"
        getsnaps = host + getsnappath + snapfilter
        getsnapsrequest = requests.get(getsnaps)

        for i in getsnapsrequest.text.strip().split('\n'):
            delsnapname = str(i.split(' ')[0])
            delsnapepoch = int(i.split(' ')[-1])
            if delsnapepoch <= deletesnapepoch:
                print(delsnapname + " deleting...")
                deletesnap = host + snappath + delsnapname
                deletesnaprequest = requests.delete(deletesnap)
                print(deletesnaprequest.status_code)
                print(deletesnaprequest.text)
            else:
                print(delsnapname + " is not going to delete now.....")

    else:
        print("myenv =" + myenv)