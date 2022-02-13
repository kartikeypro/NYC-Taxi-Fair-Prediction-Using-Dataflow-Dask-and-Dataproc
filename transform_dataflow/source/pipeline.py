import unittest
import logging
import apache_beam as beam
import pandas as pd
from apache_beam.io.gcp import gcp.gcsio

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()