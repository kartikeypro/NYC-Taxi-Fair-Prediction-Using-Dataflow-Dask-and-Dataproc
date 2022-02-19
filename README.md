# NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc
Project involves the transformation of data using GCP Dataflow job, data is extracted for specific duration using bigquery after partitioning and clustering, then further modelling and analysis is done using Dask running on Dataproc.
Project Steps:
1. Dataset directory of approximately 6 GB is stored in the local system. Aim is to transfer the entire resources and computation on Google Cloud.
2. Google cloud project with the name nyc 2022 is created and service account for the same is initialised ([Documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects)).
3. Then gsuite libraries (gcloud,gsuilt, bq) are installed using command line.
4. Gcloud account is initalised using ([Documentation](https://cloud.google.com/sdk/docs/initializing)):
```
gcloud init
```
5. Secret key (json file) for the service account created in cloud project nyc2022 is set to the variable GOOGLE_APPLICATION_CREDENTIALS:
```
export GOOGLE_APPLICATION_CREDENTIALS=path_to_secretkey_json_file
```
5. The datset is stored in the google cloud storage using following command:
```
gsutil -m cp local_file_path cloud_storage_path
m: multiprocessing flag
```
![image: test.csv and train.csv in nycdataset cloud storage bucket.](https://github.com/kartikeypro/NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc/blob/main/Assets/Screenshot%202022-02-19%20at%205.59.04%20PM.png)


7. A jupyter notebook is created to observe 100000 values out of the huge nyc dataset and certain transformations and manipulations are suggested based on the observed data.
<img width="1053" alt="Screenshot 2022-02-20 at 2 23 07 AM" src="https://user-images.githubusercontent.com/32822178/154818688-90d3197c-e31a-412b-9e53-09b34a11dfd1.png">
