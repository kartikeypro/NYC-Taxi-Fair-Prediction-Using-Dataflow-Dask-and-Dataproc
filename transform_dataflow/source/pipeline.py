import unittest
import logging
import apache_beam as beam
import pandas as pd
import apache_beam as beam
import argparse


in_file = " "
out_file = " "

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file",default="",help="the file path for input text to process")
    


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()