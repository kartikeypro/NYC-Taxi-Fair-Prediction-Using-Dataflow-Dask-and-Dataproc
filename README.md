# NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc
Project involves the transformation of data using GCP Dataflow job and then further modelling and analysis is done using Dask running on Dataproc.
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
![image: test.csv and train.csv in nycdataset cloud storage bucket.](https://drive.google.com/file/d/1gjmm3XkBQpIQ6KNO9NZ98mdQP2PORIsM/view?usp=sharing)
6. 
