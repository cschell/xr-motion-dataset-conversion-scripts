import sys
import pandas as pd
from xror import XROR
from pathlib import Path
import bson
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm

beatsaber_column_names = [
    "delta_time_ms",
    "head_pos_x",
    "head_pos_y",
    "head_pos_z",
    "head_rot_x",
    "head_rot_y",
    "head_rot_z",
    "head_rot_w",
    "left_hand_pos_x",
    "left_hand_pos_y",
    "left_hand_pos_z",
    "left_hand_rot_x",
    "left_hand_rot_y",
    "left_hand_rot_z",
    "left_hand_rot_w",
    "right_hand_pos_x",
    "right_hand_pos_y",
    "right_hand_pos_z",
    "right_hand_rot_x",
    "right_hand_rot_y",
    "right_hand_rot_z",
    "right_hand_rot_w",
]

tilt_brush_column_names = [
    "delta_time_ms",
    "right_hand_pos_x",
    "right_hand_pos_y",
    "right_hand_pos_z",
    "right_hand_rot_x",
    "right_hand_rot_y",
    "right_hand_rot_z",
    "right_hand_rot_w",
    "drawing",
]

DEMO_MODE = False

if DEMO_MODE:
    MAX_USERS = 5
    print(
        f"WARNING: Demo mode is active, so only the first {MAX_USERS} users will be processed;"
        "set `DEMO_MODE = False` to process all users."
    )
else:
    MAX_USERS = None


def load_recording(recording_file):
    try:
        with open(recording_file, "rb") as file:
            recording = XROR.unpack(file.read())
    except bson.errors.InvalidBSON:
        print(f"WARNING: error while trying to read {recording_file}, skipping...")
        return None
    return recording


def convert(dataset_path, output_path):
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)

    recording_files = Path(dataset_path).glob("*/*.xror")

    user_dirs = Path(dataset_path).glob("*")

    for user_dir in tqdm(list(user_dirs), desc="processing users", total=MAX_USERS):
        recording_files = user_dir.glob("*.xror")
        for file_idx, recording_file in enumerate(recording_files):
            recording = load_recording(recording_file)
            if MAX_USERS and file_idx >= MAX_USERS:
                break

            user_id = recording.data["info"]["user"]["id"]
            app = recording.data["info"]["software"]["app"]["name"]

            if app == "Beat Saber":
                column_names = beatsaber_column_names
                time_scaling = 1000
            elif app == "Tilt Brush":
                column_names = tilt_brush_column_names
                time_scaling = 1
            else:
                raise Exception("Unknown App")

            df = (
                pd.DataFrame(recording.data["frames"], columns=column_names)
                .pipe(_convert_m_to_cm)
                .pipe(_convert_coord_system_from_RUB_to_RUF)
                .assign(delta_time_ms=lambda df: (df["delta_time_ms"] - df["delta_time_ms"].iloc[0]) * time_scaling)
            )

            recording_output_path = output_path / app / user_id
            recording_output_path.mkdir(parents=True, exist_ok=True)

            session_id = recording_file.stem
            df.round(3).to_csv(recording_output_path / f"{session_id}.csv", index=False)


if __name__ == "__main__":
    dataset_path = "raw_datasets/BOXRR-23"
    output_path = "converted_datasets/BOXRR-23"

    convert(dataset_path, output_path)
