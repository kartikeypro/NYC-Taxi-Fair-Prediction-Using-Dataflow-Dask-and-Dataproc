# NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc
Project involves the transformation of data using GCP Dataflow job, compressed avro data blocks are ingested into bigquery as a single table, data is extracted for specific duration using bigquery after partitioning and clustering and stored in gcs, and finally modelling and analysis is done on this data using Dask running on Dataproc.
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

8. Based on the given transformations an ETL job was formulated using Apache Beam Python SDK. Uncompressed CSV file is read from gcs bucket, then transformation are executed and finally it is stored in compressed avro files. The files for the same can be found under the directory "transform-dataflow". Following was the configuration of the job:
<img width="825" alt="Screenshot 2022-02-20 at 2 27 34 AM" src="https://user-images.githubusercontent.com/32822178/154818820-64283751-15f2-43be-94b3-9dfe18d92f3b.png">

9. Python directory construction remains very important here. Ex. Creating __init__.py file in each sub directory, declaring requirements.txt or setup.py file, calling import by absolute path. 

10. Sometimes all the workers are not able to scale because of low availiabilty of resources at the selected region. Like in my case, I specified to use 40 workers but only 2 workers could scale up. While this can be avoided by selecting other region but it invites extra cost and huge latency because my storage buckets are stored in India and using any data centre outside India for computation would inevitably invite extra burden. 

11. Pipeline graph and some of its key metrics: (For more information go to detail.txt in tansform-dataflow directory)
<img width="785" alt="Screenshot 2022-02-20 at 10 48 35 AM" src="https://user-images.githubusercontent.com/32822178/154829528-3d108453-05d3-40a5-bd99-ac3d3689fd51.png">![CPU utilization (All Workers)](https://user-images.githubusercontent.com/32822178/154829558-cf6c235b-b8dd-4bb5-8daf-3fc43d6382b8.png)![Throughput (elements_sec)](https://user-images.githubusercontent.com/32822178/154829565-11eeff58-bfcd-40fa-8052-ffccc7681459.png)

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
