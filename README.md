# NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc
Today, new machine learning models are churning out like eggs from chicken. While they remain successfull at proving their performance with a small subset of dataset but when it comes to petabytes of data, which is quite common in today's context, they all fail to scale and emulate their performance. It is very important for machine learning models and data transformation practices to be scalable from starting. This is what I aim to do here. This project involves the transformation of csv data using GCP Dataflow job into compressed avro data blocks, which is then ingested into bigquery as a single table, data is extracted for a specific duration using bigquery after partitioning and clustering and stored in gcs, and finally modelling and analysis is done on this data using Dask, Rapids and GPUs running on Dataproc and VM Instance. **Please watch this before starting with the description** 

[![name](https://github.com/kartikeypro/NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc/blob/main/Assets/Screenshot%202022-02-21%20at%2011.46.40%20AM.png)](https://youtu.be/yaY85CqyamY)

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
6. If you still face problem interacting with gcloud due to accessibility issues you can try following commands:
```
gcloud auth login
gcloud auth-application default login
```
8. The datset is stored in the google cloud storage using following command:
```
gsutil -m cp local_file_path cloud_storage_path
m: multiprocessing flag
```
![image: test.csv and train.csv in nycdataset cloud storage bucket.](https://github.com/kartikeypro/NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc/blob/main/Assets/Screenshot%202022-02-19%20at%205.59.04%20PM.png)


7. A jupyter notebook is created to observe 100000 values out of the huge nyc dataset and certain transformations and manipulations are suggested based on the observed data.
<img width="1053" alt="Screenshot 2022-02-20 at 2 23 07 AM" src="https://user-images.githubusercontent.com/32822178/154818688-90d3197c-e31a-412b-9e53-09b34a11dfd1.png">

8. Based on the given transformations an ETL job was formulated using Apache Beam Python SDK. Uncompressed CSV file is read from gcs bucket, then transformation are executed and finally it is stored in compressed avro files. The files for the same can be found under the directory "transform-dataflow". Following was the configuration of the job:
<img width="825" alt="Screenshot 2022-02-20 at 2 27 34 AM" src="https://user-images.githubusercontent.com/32822178/154818820-64283751-15f2-43be-94b3-9dfe18d92f3b.png">

9. Python directory construction remains very important here. Ex. Creating __init__.py file in each sub directory, declaring requirements.txt or setup.py file, calling import by absolute path. 

10. Sometimes all the workers are not able to scale because of low availiabilty of resources at the selected region. I scaled 40 workers in my case. One should usually avoid doing so many workers as it tantamounts to considerable cost. One can do this job even in 5 workers quite comfortably. This ETL job took 5 minutes from the time all workers scaled up to process 54 million rows!! 

11. Pipeline graph and some of its key metrics: (For more information go to detail.txt in tansform-dataflow directory)
![Screenshot from 2022-02-21 10-24-59](https://user-images.githubusercontent.com/32822178/154892483-32278538-5c6e-4f0f-bb09-92a50b38920e.png)
![CPU utilisation (All workers)](https://user-images.githubusercontent.com/32822178/154893106-fe182067-deb4-40ab-b1aa-72e67b2c6537.png)
![Throughput (elements_sec)](https://user-images.githubusercontent.com/32822178/154893172-d9e5a7fc-6a2e-495e-a1bd-a9c62c47bf2d.png)


12. Git Graph as of this point.
<img width="1061" alt="Screenshot 2022-02-20 at 11 14 10 AM" src="https://user-images.githubusercontent.com/32822178/154830226-11c50978-47a2-4556-8748-2ed5bc039c1a.png">

13. Ouput of dataflow pipeline is stored as compressed avro files. The size of the avro files (More columns than input file) is approximately 1.1 GB as compared to the input file of 5.6 GB. **More than 80% compression level has been achieved.** 

14. Now these avro files are transferred to bigquery using bq cli command tools.

```
bq --location=asia-south1 mk --dataset dataset_name   # Constructs dataset inside current project
bq load --source_format=AVRO dataset.table_name avro_file_path # Creates table from the input avro data present
```
15. Now, data has been stored in big query, I am going to compare the query cost between between unpartitioned and partitioned data. We are going to build our training model on years 2011 and 2012 and test it on some entries of 2013. So, we have to query that data out.
16. Table partitioned on year column using following query:
```
CREATE TABLE nyc_dataset.partnyc
PARTITION BY RANGE_BUCKET(year, GENERATE_ARRAY(2009, 2016 ,1)) AS
SELECT * FROM `nyc2022.nyc_dataset.nycData`
```
17. Let's query out the data for 2011 and 2012 from unpartitioned table.
```
SELECT * FROM `nyc2022.nyc_dataset.nycData` 
WHERE YEAR=2011 OR YEAR=2012
```
<img width="888" alt="Screenshot 2022-02-20 at 3 07 48 PM" src="https://user-images.githubusercontent.com/32822178/154836755-7be39bcc-418f-48dc-a31e-19f5e3e95a38.png">

18. Now, let us run the same query on partitoned table.
```
SELECT * FROM `nyc2022.nyc_dataset.partnyc` 
WHERE YEAR=2011 OR YEAR=2012
```
<img width="887" alt="Screenshot 2022-02-20 at 3 13 56 PM" src="https://user-images.githubusercontent.com/32822178/154836973-78fdc806-2747-4960-9eb5-fbc84875b2d1.png">
Query result for partitioned table is dramatically better than unparttioned table.

19. Now, I am going to roll out dataproc cluster and run my model on dask, rapids and GPU. 
20. Ran some initalization functions given below on cloud interactive terminal:
```
SCRIPT_BUCKET=gs://goog-dataproc-initialization-actions-asia-south1
gsutil cp ${SCRIPT_BUCKET}/gpu/install_gpu_driver.sh nycdataset/gpu/install_gpu_driver.sh
gsutil cp ${SCRIPT_BUCKET}/dask/dask.sh nycdataset/dask/dask.sh
gsutil cp ${SCRIPT_BUCKET}/rapids/rapids.sh nycdataset/rapids/rapids.sh
gsutil cp ${SCRIPT_BUCKET}/python/pip-install.sh nycdataset/python/pip-install.sh
```

21. **ROADBLOCK** I cannot create dataproc cluster from my free account, google free trial is a hoax!.
22. Sorry but I can't take you ahead of this. I can't use my company account to roll out clusters but I can surely show you other projects on similar lines in full confidentiality. If you are interested please follow and message me on twitter @itskartikey.
23. I'll try to complete this project once I receive my salary xD
