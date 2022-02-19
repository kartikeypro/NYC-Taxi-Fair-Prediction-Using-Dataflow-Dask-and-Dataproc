import argparse
import logging
from source import pipeline

if __name__=='main':
    logging.getLogger().setLevel(logging.info)
    pipeline.run()
