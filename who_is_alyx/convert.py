from pathlib import Path
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))

JOINTS = ["head", "left_hand", "right_hand"]

column_mapping = {
    "delta_time_ms": "delta_time_ms",
    "hmd_pos_x": "head_pos_x",
    "hmd_pos_y": "head_poqs_y",
    "hmd_pos_z": "head_pos_z",
    "hmd_rot_x": "head_rot_x",
    "hmd_rot_y": "head_rot_y",
    "hmd_rot_z": "head_rot_z",
    "hmd_rot_w": "head_rot_w",
    "left_controller_pos_x": "left_hand_pos_x",
    "left_controller_pos_y": "left_hand_pos_y",
    "left_controller_pos_z": "left_hand_pos_z",
    "left_controller_rot_x": "left_hand_rot_x",
    "left_controller_rot_y": "left_hand_rot_y",
    "left_controller_rot_z": "left_hand_rot_z",
    "left_controller_rot_w": "left_hand_rot_w",
    "right_controller_pos_x": "right_hand_pos_x",
    "right_controller_pos_y": "right_hand_pos_y",
    "right_controller_pos_z": "right_hand_pos_z",
    "right_controller_rot_x": "right_hand_rot_x",
    "right_controller_rot_y": "right_hand_rot_y",
    "right_controller_rot_z": "right_hand_rot_z",
    "right_controller_rot_w": "right_hand_rot_w",
}


def convert(dataset_path, output_path):
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    for recording_file in tqdm(list(dataset_path.glob("players/*/*/vr-controllers*.csv"))):
        player_id, session = recording_file.parts[-3:-1]
        is_part_1 = not (recording_file.stem[-1] == "2")

        recording = pd.read_csv(recording_file).rename(columns=column_mapping)[column_mapping.values()]

        recording.round(3).to_csv(output_path / f"{player_id}_{session}_{'1' if is_part_1 else '2'}", index=False)


if __name__ == "__main__":
    dataset_path = "raw_datasets/who-is-alyx"
    output_path = "converted_datasets/who-is-alyx"

    convert(dataset_path, output_path)
