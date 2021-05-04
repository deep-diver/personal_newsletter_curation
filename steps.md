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

- Now we are ready to create a GCP AI Platform Pipeline. Actually, it is possible to create a GKE cluster on the go, but only the default configuration can be provided. In order to enable GPU node pool, the above steps are required. (*The reason why we need a GPU node pool is that BERT based model is too huge to be even evaluated with CPUs*). 

- [ ] Simply click the `NEW INSTANCE` button on AI Platform Pipeline service, then it will bring you to the new page. Then clicke the `CONFIGURE` button on that new page.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/ai-platform-pipeline-spinup.png?raw=true)

- [ ] A new page called `Kubeflow Pipelines Overview` will be loaded. This is the page you can configure your pipeline. Just make sure the GKE cluster that we have just created is selected under `Cluster` menu. Then simply hit the `Deploy` button on the bottom. It will take few minutes to complete the pipeline creation step. 

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/kubeflow-pipeline-spinup.png?raw=true)

## 3. Run TFX Pipeline

- [ ] The initial TFX Pipeline can be setup through AI Platform Notebook. In order to setup a notebook, open up the pipeline dashboard by clicking `OPEN PIPELINES DASHBOARD` button. When the dashboard page pops up, find `Open TF 2.1 Notebook` link. It says `TF 2.1`, but it supports further versions too. When clicking that link, it will bring you to a page for setting up a AI Platform Notebook instance. With the default setting, please click `CREATE` button at the bottom. It will take a couple of minutes to finish setting it up. On the popped up window(Ready to open notebook), you can click `OPEN` button, then it will redirect you to the JupyterLab page.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/notebook-connect.png?raw=true)

- [ ] Please run the cells on the `template.ipynb` notebook sequentially until you encounter a cell containing `ENDPOINT` variable to setup. You have to setup the `AI Platform Pipeline's Endpoint URL`, and you can find the URL easily by looking up the URL text box on the pipeline dashboard page. After setting `ENDPOINT` with an appropriate value, then hit run the cell. 

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/ai-pipeline-url-to-jupyter.png?raw=true)

- You are all set up for interacting with AI Platform Pipeline via AI Platform Notebook. The only thing left is to run the actual `TFX` code. The JupyterLab doesn't have any files or folders, so lets create them first.

- [ ] Please run the cells on the `template.ipynb` notebook sequentially from where you stopped until you encounter a cell containing `TFX CLI` which is `!tfx template copy ...`. When you run that cell, it will create template directories for you. The name of root directory is `my_pipeline`. If you navigate the subdirectories, you will see the directory tree structures like below.

![](https://github.com/deep-diver/personal_newsletter_curation/blob/main/assets/image/create-tfx-template.png?raw=true)

[BERT](https://github.com/tensorflow/workshops/blob/master/blog/TFX_Pipeline_for_Bert_Preprocessing.ipynb)
