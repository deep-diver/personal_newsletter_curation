# Steps to follow to replicate this project.

## 1. Collect data from twitter
The first step is about collecting data.

- [ ] You need twitter API keys issued from [Twitter's Developer Portal](https://developer.twitter.com/en) and [Tweepy](https://www.tweepy.org/) which is a open source project to scrap tweets in OOP manner.
- [ ] You need to scrap tweets using [scrap_tweets.py](https://github.com/deep-diver/personal_newsletter_curation/blob/main/utils/scrap_tweets.py). It is a base source code to collect tweets via Tweepy and save them in CSV file format. In the CSV file, only the text are stored.
- [ ] Next step is to label the collected data via your favoriate Text Classification Annotation Tool. In my case, I have used [docanno](https://github.com/doccano/doccano) which is a free open source tool.
- [ ] The final step is to convert the labeled dataset(CSV) to TFRecord format file. You can use [convert_to_tfrecord.py](https://github.com/deep-diver/personal_newsletter_curation/blob/main/utils/convert_to_tfrecord.py) for this purpose. It simply converts raw text and labels into protocol buffer compatible data types and save them in TFRecord format file.

## 2. Create a GCP AI Platform Pipeline
The second step is to build a machine learning pipeline via Google Cloud Platform.

- [ ] Before directly creating a GCP AI Platform Pipeline, you first need to spin up Kubernetes Cluster on  Google Kubernetes Engine(GKE). One thing to note is that you should include a GPU node pool with **one** GPU node configured. 
- [ ] CPU node pool can be configured as you like. In my case, I have setup with a default type of VM with 2 nodes in it. The only thing to be careful is that you should check `Allow full access to all Cloud APIs` option under `NODE POOLS > CPU NODE POOL > Security` tab.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/cpu-pool.png?raw=true)

- [ ] You should click `Add Node Pool` button to add additional node pool for GPU. GPU node pool is configures like below. The only thing to be careful(just like CPU node pool) is that you should check `Allow full access to all Cloud APIs` option under `NODE POOLS > GPU NODE POOL > Security` tab.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/gpu-pool.png?raw=true)

- [ ] One last thing to configure before spinning up the GKE cluster is the options, `Enable legacy authorization` and `Enable basic authentication(deprecated)` under `CLUSTER > Security` tab

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/security-option.png?raw=true)

- [ ] After spinning up the GKE Cluster successfully, you should install the NVIDIA GPU device drivers. [This guide](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers) explains how in more detail. In order to breifly give a how-to, you first connect to the GKE cluster via Cloud Shell. Then just run the `kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml` CLI in the shell.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/nvidia-driver-configuratin.png?raw=true)
