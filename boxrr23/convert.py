import sys
import pandas as pd
from xror import XROR
from pathlib import Path
import bson
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm, _convert_dm_to_cm

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


def load_recording(recording_file):
    try:
        with open(recording_file, "rb") as file:
            recording = XROR.unpack(file.read())
    except bson.errors.InvalidBSON:
        print(f"WARNING: error while trying to read {recording_file}, skipping...")
        return None
    return recording


def convert(dataset_path, demo_mode=True):
    if demo_mode:
        max_users = 5
        max_recs_per_user = 5
        print(
            f"WARNING: Demo mode is active, so only the first {max_users} users will be processed;"
            "set `demo_mode = False` to process all users."
        )
    else:
        max_users = None
        max_recs_per_user = None
    user_dirs = list(Path(dataset_path).glob("*"))[:max_users]

    for user_dir in tqdm(user_dirs, desc="processing users"):
        recording_files = list(user_dir.glob("*.xror"))[:max_recs_per_user]
        for recording_file in recording_files:
            recording = load_recording(recording_file)

            user = recording.data["info"]["user"]["id"]
            app = recording.data["info"]["software"]["app"]["name"]

            if app == "Beat Saber":
                column_names = beatsaber_column_names
                time_scaling = 1000
                unit_converter = _convert_m_to_cm
            elif app == "Tilt Brush":
                column_names = tilt_brush_column_names
                time_scaling = 1
                unit_converter = _convert_dm_to_cm
            else:
                raise Exception("Unknown App")

            df = (
                pd.DataFrame(recording.data["frames"], columns=column_names)
                .pipe(unit_converter)
                .pipe(_convert_coord_system_from_RUB_to_RUF)
                .assign(delta_time_ms=lambda df: (df["delta_time_ms"] - df["delta_time_ms"].iloc[0]) * time_scaling)
            )

            for col in df.select_dtypes(include=["float64"]).columns:
                df[col] = df[col].astype("float32")

            session = recording_file.stem
            yield df, (user, session, app)


def convert_and_store(dataset_path, output_path, format="csv", demo_mode=True):
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    for recording, (user, session, app) in convert(dataset_path, demo_mode):
        output_file_path = output_path / user / session
        output_file_path.parents[0].mkdir(exist_ok=True, parents=True)

        recording = recording.assign(user=user, session=session, app=app)

        match format.lower():
            case "csv":
                recording.round(3).to_csv(output_file_path.with_suffix(".csv"), index=False)
            case "parquet":
                recording.to_parquet(output_file_path.with_suffix(".parquet"))
            case _:
                raise Exception("unkown output format, aborting")
