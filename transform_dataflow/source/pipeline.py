import unittest
import logging
import apache_beam as beam
import pandas as pd
import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from source import transform as tf
import fastavro

# Decalaring Schema for avro file.
schema_dict = {
    "namespace":"avrodata",
    "type":"record",
    "name": "avro",
    "fields":[
        {"name":"fare_amount","type":"float"}
        ,{"name":"pickup_longitude","type":"float"}
        ,{"name":"pickup_latitude","type":"float"}
        ,{"name":"dropoff_longitude","type":"float"}
        ,{"name":"dropoff_latitude","type":"float"}
        ,{"name":"passenger_count","type":"int"}
        ,{"name":"year","type":"int"}
        ,{"name":"month","type":"int"}
        ,{"name":"day","type":"int"}
        ,{"name":"weekday","type":"int"}
        ,{"name":"hour","type":"int"}
        ,{"name":"distance","type":"float"}
    ]
}
avro_schema = fastavro.parse_schema(schema_dict)

def run(argv=None):
    #Pipeline arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file"
    ,default="gs://nycdataset/train.csv"
    ,help="the file path for input text to process")
    args, beam_args = parser.parse_known_args()
    # Pipeline configuration
    beam_options = PipelineOptions(
      beam_args,
      runner = "DataFlowRunner",
      project = "nyc2022",
      job_name = "transforming-nyc-dataset2",
      temp_location = "gs://nycdataset/temporary",
      staging_location = "gs://nycdataset/staging",
      max_num_workers = 40,
      num_workers = 20,
      machine_type = "n1-standard-1",
      region = "asia-south1",
      setup_file = "/Users/kartikeygarg/Documents/GitHub/NYC-Taxi-Fair-Prediction-Using-Dataflow-Dask-and-Dataproc/transform_dataflow/setup.py"
      ) 
    #Pipeline transformations
    with beam.Pipeline(options=beam_options) as p:
      delimited_data = (
        p | beam.io.ReadFromText(args.input_file,skip_header_lines=1)
        | beam.ParDo(tf.getRecord())
        | beam.Filter(tf.throwEmpty)
        | beam.ParDo(tf.mapColumns())
        | beam.ParDo(tf.swap())
        | beam.Filter(tf.removeRows)
        | beam.ParDo(tf.transformDate())
        | beam.ParDo(tf.getDistance())
        | beam.io.WriteToAvro("gs://nycdataset/transformed data/data",schema=avro_schema)
      )


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()