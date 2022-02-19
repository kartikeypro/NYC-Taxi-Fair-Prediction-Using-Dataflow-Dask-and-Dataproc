import argparse
import logging
from source import pipeline

if __name__=='__main__':
    logging.getLogger().setLevel(logging.INFO)
    pipeline.run()
