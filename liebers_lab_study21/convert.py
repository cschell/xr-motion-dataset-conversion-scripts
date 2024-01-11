from pathlib import Path
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm, _euler_to_quat

JOINTS = ["head", "left_hand", "right_hand"]
column_mapping = {
    "timestamp_ms": "delta_time_ms",
    "CenterEyeAnchor_pos_X": "head_pos_x",
    "CenterEyeAnchor_pos_Y": "head_pos_y",
    "CenterEyeAnchor_pos_Z": "head_pos_z",
    "CenterEyeAnchor_euler_X": "head_rot_x",
    "CenterEyeAnchor_euler_Y": "head_rot_y",
    "CenterEyeAnchor_euler_Z": "head_rot_z",
    "LeftControllerAnchor_pos_X": "left_hand_pos_x",
    "LeftControllerAnchor_pos_Y": "left_hand_pos_y",
    "LeftControllerAnchor_pos_Z": "left_hand_pos_z",
    "LeftControllerAnchor_euler_X": "left_hand_rot_x",
    "LeftControllerAnchor_euler_Y": "left_hand_rot_y",
    "LeftControllerAnchor_euler_Z": "left_hand_rot_z",
    "RightControllerAnchor_pos_X": "right_hand_pos_x",
    "RightControllerAnchor_pos_Y": "right_hand_pos_y",
    "RightControllerAnchor_pos_Z": "right_hand_pos_z",
    "RightControllerAnchor_euler_X": "right_hand_rot_x",
    "RightControllerAnchor_euler_Y": "right_hand_rot_y",
    "RightControllerAnchor_euler_Z": "right_hand_rot_z",
}


def convert(dataset_path, output_path):
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    for recording_file in tqdm(list(dataset_path.glob("*.csv"))):
        recording = (
            pd.read_csv(recording_file)
            .rename(columns=column_mapping)
            .pipe(_euler_to_quat)
            .pipe(_convert_m_to_cm)
            .pipe(_convert_coord_system_from_RUB_to_RUF)[
                sorted(list(column_mapping.values()) + [f"{j}_rot_w" for j in JOINTS])
            ]
        )

        recording.round(3).to_csv(output_path / recording_file.name, index=False)


if __name__ == "__main__":
    dataset_path = "raw_datasets/LiebersLabStudy21"
    output_path = "converted_datasets/LiebersLabStudy21"

    convert(dataset_path, output_path)
