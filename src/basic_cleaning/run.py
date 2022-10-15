#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd
import os 


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    logger.info("Downloading artifact")
    
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)
    
    # Drop outliers
    min_price = 10
    max_price = 350

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    filename = "clean_sample.csv"
    df.to_csv(filename,index=False)
    
    artifact = wandb.Artifact(
                     args.output_artifact,
                     type=args.output_type,
                     description=args.output_description,
                    )
    artifact.add_file(filename)
    
    logger.info("Logging artifact")
    run.log_artifact(artifact)

    os.remove(filename)
    
    
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type = str,
        help = "Fully-qualified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type = str,
        help = "Fully-qualified name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type = str,
        help = "Type for the output",
        required=True
    )
    
    
    parser.add_argument(
        "--output_description", 
        type= str,
        help = "Description for the output",
        required=True
    )
    
    
    parser.add_argument(
        "--min_price", 
        type = float,
        help= "Min price to transform",
        required=True
    )
    
    parser.add_argument(
        "--max_price", 
        type = float,
        help = "Max price to transform",
        required=True
    )


    args = parser.parse_args()

    go(args)
