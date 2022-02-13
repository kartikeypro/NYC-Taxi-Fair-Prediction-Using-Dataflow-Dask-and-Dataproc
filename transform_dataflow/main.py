import argparse
import logging
from source import pipeline

in_file = " "
out_file = " "

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file",default="",help="the file path for input text to process")


if __name__=='main':
    logging.getLogger().setLevel(logging.info)

