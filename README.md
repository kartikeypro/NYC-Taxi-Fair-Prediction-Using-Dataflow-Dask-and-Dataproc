# NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc
Project involves the transformation of data using GCP Dataflow job and then further modelling and analysis is done using Dask running on Dataproc.
Project Steps:
1. Dataset directory of approximately 6 GB is stored in the local system. Aim is to transfer the entire resources and computation on Google Cloud.
2. Google cloud project with the name nyc 2022 is created and service account for the same is initialised.
3. Then gsuite libraries(gcloud,gsuilt, bq) are installed using command line.
4. The datset stored in the system using following command:
```
gsutil -m cp local_file_path cloud_storage_path
m: multiprocessing flag
```
5. 
