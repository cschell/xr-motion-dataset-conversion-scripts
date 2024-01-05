import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm, _euler_to_quat

JOINTS = ["head", "left_hand", "right_hand"]
column_mapping = {
    "timestamp_ms": "delta_time_ms",
    "frame-movements-pos-x-head": "head_pos_x",
    "frame-movements-pos-y-head": "head_pos_y",
    "frame-movements-pos-z-head": "head_pos_z",
    "frame-movements-euler-x-head": "head_rot_x",
    "frame-movements-euler-y-head": "head_rot_y",
    "frame-movements-euler-z-head": "head_rot_z",
    "frame-movements-quat-w-head": "head_rot_w",
    "frame-movements-pos-x-lcontroller": "left_hand_pos_x",
    "frame-movements-pos-y-lcontroller": "left_hand_pos_y",
    "frame-movements-pos-z-lcontroller": "left_hand_pos_z",
    "frame-movements-euler-x-lcontroller": "left_hand_rot_x",
    "frame-movements-euler-y-lcontroller": "left_hand_rot_y",
    "frame-movements-euler-z-lcontroller": "left_hand_rot_z",
    "frame-movements-quat-w-lcontroller": "left_hand_rot_w",
    "frame-movements-pos-x-rcontroller": "right_hand_pos_x",
    "frame-movements-pos-y-rcontroller": "right_hand_pos_y",
    "frame-movements-pos-z-rcontroller": "right_hand_pos_z",
    "frame-movements-euler-x-rcontroller": "right_hand_rot_x",
    "frame-movements-euler-y-rcontroller": "right_hand_rot_y",
    "frame-movements-euler-z-rcontroller": "right_hand_rot_z",
    "frame-movements-quat-w-rcontroller": "right_hand_rot_w",
}


recording_path = Path("Data_Set_for_Exploring_the_Stability_of_Behavioral_Biometrics_in_Virtual_Reality.csv")


def convert(dataset_file_path, output_path, assumed_fps=90):
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_csv(dataset_file_path, index_col=False)
    num_sessions = dataset["session-uuid"].unique().size

    for session_id, df in tqdm(dataset.groupby("session-uuid"), total=num_sessions):
        recording = (
            df.rename(columns=column_mapping)
            .pipe(_euler_to_quat)
            .pipe(_convert_m_to_cm)
            .pipe(_convert_coord_system_from_RUB_to_RUF)
            .assign(delta_time_ms=lambda df: np.arange(len(df)) * (1000 / assumed_fps))[
                sorted(list(column_mapping.values()))
            ]
        )
        user = df["user-token"].iloc[0]
        recording.round(3).to_csv(output_path / f"{user}_{session_id}.csv", index=False)


if __name__ == "__main__":
    dataset_file_path = "raw_datasets/LiebersBeatSaber23/Data_Set_for_Exploring_the_Stability_of_Behavioral_Biometrics_in_Virtual_Reality.csv"
    output_path = "converted_datasets/LiebersBeatSaber23"

    convert(dataset_file_path, output_path)
