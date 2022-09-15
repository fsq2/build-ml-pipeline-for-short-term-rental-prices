#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd 


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    
    logger.info("Set Max & Min For Price Col")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2) & df['price'].between(min_price, max_price)
    df = df[idx].copy()
    
    logger.info("Fix Date For Last Reveiw Col")
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    df.to_csv("clean_sample.csv", index=False)
    
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,)
  
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of the input artifact in W&D",
        required=True       
    )
    parser.add_argument(
        "--output_artifact",
        type=str,
        help=" Name of the output ",
        required=True
    )
    
    parser.add_argument(
        "--output_type",
        type=str,
        help=" Type of the output",
        required=True
    )
    
    parser.add_argument(
        "--output_description",
        type=str,
        help="Output describtion",
        required=True
    )
    
    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min value for the price column",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max value for the price column",
        required=True
    )

    args = parser.parse_args()

    go(args)
