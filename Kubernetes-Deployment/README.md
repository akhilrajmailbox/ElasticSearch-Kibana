# ElasticSearch on AKS

[kudos](https://medium.com/faun/https-medium-com-thakur-vaibhav23-ha-es-k8s-7e655c1b7b61)

[help](https://www.datadoghq.com/blog/elasticsearch-game-day/)

## Create Namespace for Elasticsearch Deployment
```
kubectl apply -f es-namespace.yaml
```

## Deploy master nodes
```
kubectl apply -f es-master-deployment.yaml
kubectl apply -f es-master-service.yaml
kubectl -n elasticsearch get pods
```

## Deploy data nodes
```
kubectl apply -f es-data-storageclass.yaml
kubectl get storageclass
kubectl apply -f es-data-deployment.yaml
kubectl apply -f es-data-service.yaml
kubectl -n elasticsearch get pods
```

## Deploy client nodes
```
kubectl apply -f es-client-deployment.yaml
kubectl apply -f es-client-service.yaml
kubectl -n elasticsearch get pods
```

ElasticSearch can access on this url : `http://<<es_client_loadbalancer_IPAddress>>:9200`


## Deploy Elastic HQ (Monitoring tool)
```
kubectl apply -f es-hq-deployment.yaml
kubectl apply -f es-hq-service.yaml
kubectl -n elasticsearch get pods
```

Elastic HQ can access on this url : `http://<<es_HQ_loadbalancer_IPAddress>>/#!/clusters/my-es`

## Deploy Kibana Server
```
kubectl apply -f kibana-deployment.yaml
kubectl apply -f kibana-service.yaml
kubectl -n elasticsearch get pods
```

kibana can access on this url : `http://<<kibana_loadbalancer_IPAddress>>/app/kibana#/home?_g=()`


## Deploy Elastic APM Server
```
kubectl -n elasticsearch create configmap apm-server-cm --from-file=apm-server.yml
kubectl apply -f es-apm-deployment.yaml
kubectl apply -f es-apm-service.yaml
kubectl -n elasticsearch get pods
```

Elastic APM can access on this url : `http://<<es_APM_loadbalancer_IPAddress>>`

## Check the services, pods, pvc and pv
```
kubectl -n elasticsearch get pods
kubectl -n elasticsearch get services
kubectl -n elasticsearch get pvc
kubectl get pv
```


## Scaling Considerations

### client nodes

We can deploy autoscalers for our client nodes depending upon our CPU thresholds. A sample HPA for client node might look something like this:

```
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: es-client
  namespace: elasticsearch
spec:
  maxReplicas: 5
  minReplicas: 2
  scaleTargetRef:
    apiVersion: extensions/v1beta1
    kind: Deployment
    name: es-client
targetCPUUtilizationPercentage: 80
```

Whenever the autoscaler will kick in, we can watch the new client-node pods being added to the cluster, by observing the logs of any of the master-node pods.

### data nodes

In case of Data-Node Pods all we have to do it increase the number of replicas using the K8 Dashboard or GKE console. The newly created data node will be automatically added to the cluster and start replicating data from other nodes.

### master nodes

Master-Node Pods do not require autoscaling as they only store cluster-state information but in case you want to add more data nodes make sure there are no even number of master nodes in the cluster also the environment variable NUMBER_OF_MASTERS is updated accordingly.



## PVC Resizing Configuration

[here](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/)

1. Delete all the pods which are using pvc (delete the StatefulSet)
2. edit all pvc with as follows

`kubectl -n elasticsearch edit  pvc storage-es-data-0`


```
uodate the storage entry.
```

3. redeploy the `StatefulSet`



## The LOG Battle: Logstash and Fluentd

* source data processing pipeline
  * Logstash
  * Fluentd
* lightweight shippers
  * Filebeat
  * Fluentbit

[here](https://medium.com/tensult/the-log-battle-logstash-and-fluentd-c65f2f7c24b4)

### filebeat

[installation 1](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html)

[installation 2](https://crunchify.com/setup-guide-install-configure-filebeat/)

[configuration](https://www.elastic.co/guide/en/beats/filebeat/5.1/filebeat-configuration-details.html)