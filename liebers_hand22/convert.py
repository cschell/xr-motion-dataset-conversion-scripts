from pathlib import Path
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm

JOINTS = ["left_hand", "right_hand"]
column_mapping = {
    "Unity.realtimeSinceStartup": "delta_time_s",
    "Unity.HeadPosition.position_x": "head_pos_x",
    "Unity.HeadPosition.position_y": "head_pos_y",
    "Unity.HeadPosition.position_z": "head_pos_z",
    "Unity.HeadPosition.rotation.quaternion_x": "head_rot_x",
    "Unity.HeadPosition.rotation.quaternion_y": "head_rot_y",
    "Unity.HeadPosition.rotation.quaternion_z": "head_rot_z",
    "Unity.HeadPosition.rotation.quaternion_w": "head_rot_w",
    "Unity.L_Wrist.position_x": "left_hand_pos_x",
    "Unity.L_Wrist.position_y": "left_hand_pos_y",
    "Unity.L_Wrist.position_z": "left_hand_pos_z",
    "Unity.L_Wrist.rotation.quaternion_x": "left_hand_rot_x",
    "Unity.L_Wrist.rotation.quaternion_y": "left_hand_rot_y",
    "Unity.L_Wrist.rotation.quaternion_z": "left_hand_rot_z",
    "Unity.L_Wrist.rotation.quaternion_w": "left_hand_rot_w",
    "Unity.R_Wrist.position_x": "right_hand_pos_x",
    "Unity.R_Wrist.position_y": "right_hand_pos_y",
    "Unity.R_Wrist.position_z": "right_hand_pos_z",
    "Unity.R_Wrist.rotation.quaternion_x": "right_hand_rot_x",
    "Unity.R_Wrist.rotation.quaternion_y": "right_hand_rot_y",
    "Unity.R_Wrist.rotation.quaternion_z": "right_hand_rot_z",
    "Unity.R_Wrist.rotation.quaternion_w": "right_hand_rot_w",
}


def convert(dataset_path):
    dataset_path = Path(dataset_path)

    dataset_path.mkdir(parents=True, exist_ok=True)

    for recording_file in tqdm(list(dataset_path.glob("*.tsv"))):
        info = dict([attr.split("-") for attr in recording_file.stem.split("_")])
        try:
            recording = (
                pd.read_csv(recording_file, sep="\t", low_memory=False)
                .rename(columns=column_mapping)
                .pipe(_convert_m_to_cm)
                .pipe(_convert_coord_system_from_RUB_to_RUF)
                .assign(delta_time_ms=lambda df: df["delta_time_s"] * 1000)[
                    sorted(list(column_mapping.values()) + ["delta_time_ms"])
                ]
            )

            user = int(info["PID"])
            session = int(info["SESSION"])
            xr = info["XR"]
            scene = info["SCENE"]
            yield recording, (recording_file.name, user, session, xr, scene)
        except pd.errors.ParserError as e:
            print(f"WARNING: error parsing {recording_file}, skipping...")
            continue


def convert_and_store(dataset_path, output_path, format="csv"):
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    for recording, (recording_file_name, user, session, xr, scene) in convert(dataset_path):
        recording["user"] = user
        recording["session"] = session
        recording["xr"] = xr
        recording["scene"] = scene

        output_file_path = output_path / recording_file_name

        match format.lower():
            case "csv":
                recording.round(3).to_csv(output_file_path.with_suffix(".csv"), index=False)
            case "parquet":
                recording.to_parquet(output_file_path.with_suffix(".parquet"))
            case _:
                raise Exception("unkown output format, aborting")


if __name__ == "__main__":
    dataset_path = "raw_datasets/LiebersHand22/"
    output_path = "converted_datasets/LiebersHand22"

    convert_and_store(dataset_path, output_path)
