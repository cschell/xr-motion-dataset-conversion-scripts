# %%

from tqdm import tqdm
from huggingface_hub import HfApi

from convert import convert

# HfApi().create_repo(repo_id="cschell/who-is-alyx-test", repo_type="dataset")

dataset_path = "raw_datasets/who-is-alyx"

for recording, (player_id, session, is_part_1) in tqdm(convert(dataset_path)):
    recording.to_parquet(
        f"hf://datasets/cschell/who-is-alyx-test/player_{int(player_id):02d}/{session}/recording_part-{'1' if is_part_1 else '2'}.parquet"
    )

# %%

import pandas as pd

pd.read_parquet("hf://datasets/cschell/who-is-alyx/player_04/2022-01-25/recording_part-1.parquet")
