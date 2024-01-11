from pathlib import Path
import re
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm

JOINTS = ["head", "left_hand", "right_hand"]

column_mapping = {
    "Timestamp": "delta_time_ms",
    "Head_position_x": "head_pos_x",
    "Head_position_y": "head_pos_y",
    "Head_position_z": "head_pos_z",
    "Head_quat_x": "head_rot_x",
    "Head_quat_y": "head_rot_y",
    "Head_quat_z": "head_rot_z",
    "Head_quat_w": "head_rot_w",
    "LeftHand_position_x": "left_hand_pos_x",
    "LeftHand_position_y": "left_hand_pos_y",
    "LeftHand_position_z": "left_hand_pos_z",
    "LeftHand_quat_x": "left_hand_rot_x",
    "LeftHand_quat_y": "left_hand_rot_y",
    "LeftHand_quat_z": "left_hand_rot_z",
    "LeftHand_quat_w": "left_hand_rot_w",
    "RightHand_position_x": "right_hand_pos_x",
    "RightHand_position_y": "right_hand_pos_y",
    "RightHand_position_z": "right_hand_pos_z",
    "RightHand_quat_x": "right_hand_rot_x",
    "RightHand_quat_y": "right_hand_rot_y",
    "RightHand_quat_z": "right_hand_rot_z",
    "RightHand_quat_w": "right_hand_rot_w",
}


def convert(dataset_path):
    dataset_path = Path(dataset_path)
    dataset_path.mkdir(parents=True, exist_ok=True)

    for recording_file in tqdm(list(dataset_path.glob("data/*.csv"))):
        recording = (
            pd.read_csv(recording_file)
            .rename(columns=column_mapping)
            .pipe(_convert_m_to_cm)
            .pipe(_convert_coord_system_from_RUB_to_RUF)
            .assign(delta_time_ms=lambda df: df["delta_time_ms"] * 1000)[column_mapping.values()]
        )

        token, build = recording_file.stem.split("_")
        user = re.findall("FAB\d{3}.", token)[0]

        yield recording, (recording_file.name, user, build)


def convert_and_store(dataset_path, output_path, format="csv"):
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    for recording, (recording_file_name, user, build) in convert(dataset_path):
        output_file_path = output_path / recording_file_name

        recording = recording.assign(user=user, build=build)

        match format.lower():
            case "csv":
                recording.round(3).to_csv(output_file_path.with_suffix(".csv"), index=False)
            case "parquet":
                recording.to_parquet(output_file_path.with_suffix(".parquet"))
            case _:
                raise Exception("unkown output format, aborting")


if __name__ == "__main__":
    dataset_path = "raw_datasets/MooreCrossDomain23"
    output_path = "converted_datasets/MooreCrossDomain23"

    convert_and_store(dataset_path, output_path)
