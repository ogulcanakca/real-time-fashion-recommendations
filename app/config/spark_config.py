# app/config/spark_config.py

import os


class SparkConfig:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    CHECKPOINT_LOCATION = os.path.join(parent_dir, "checkpoints/reviews/")
