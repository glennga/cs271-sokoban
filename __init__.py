import logging.config
import json
import os

with open('config/logging.json') as logging_config_file:
    logging_json = json.load(logging_config_file)
    logging_output_dir = logging_json['handlers']['fileHandler']['filename'].split('/')[0]
    if not os.path.exists(logging_output_dir):
        os.makedirs(logging_output_dir)

    logging.config.dictConfig(logging_json)
