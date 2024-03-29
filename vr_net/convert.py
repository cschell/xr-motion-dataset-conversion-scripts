from pathlib import Path
import sys
import pandas as pd
from tqdm import tqdm
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
from datetime import datetime

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_m_to_cm

columns = [
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

joints = [
    "head",
    "left_hand",
    "right_hand",
]


def load_and_convert_recording(file_path):
    df = pd.read_csv(file_path).sort_values(["timestamp", "device_id"])

    origin = [0, 0, 0, 1]

    frames_np = np.zeros((df["framecounter"].max() + 1, len(columns)))
    frames_np[:] = np.nan
    timestamps = np.zeros(len(frames_np), dtype=datetime)
    timestamps[:] = np.nan

    for _, row in df.iterrows():
        if not row["timestamp"]:
            continue
        points = list(map(float, row["deviceToAbsoluteTracking"].split()))

        t_mat = np.array(
            [
                [points[0], points[1], points[2], points[3]],
                [points[4], points[5], points[6], points[7]],
                [points[8], points[9], points[10], points[11]],
                [0, 0, 0, 1],
            ]
        )
        position = np.matmul(t_mat, origin)
        rotation = Rotation.from_matrix(t_mat[0:3, 0:3]).as_quat()

        device_id = row["device_id"]
        frame_idx = row["framecounter"]
        timestamps[frame_idx] = row["timestamp"] / 1000
        frames_np[frame_idx, device_id * 7 : (device_id + 1) * 7] = np.concatenate([position[:3], rotation])

    recording = (
        pd.DataFrame(frames_np, columns=columns)
        .assign(timestamp=pd.to_timedelta(timestamps - np.nanmin(timestamps), unit="s"))
        .dropna(subset="timestamp")
        .set_index("timestamp")
        .interpolate(method="time")
        .assign(delta_time_ms=lambda df: (df.index.total_seconds() * 1000).round().astype(int))
        .pipe(_convert_m_to_cm)
        .dropna()
        .reset_index(drop=True)
    )

    assert len(recording) > 10, "replay is too short"

    return recording


def convert(dataset_path):
    for recording_file in tqdm(list(dataset_path.glob("*/*/pose.csv"))):
        recording = load_and_convert_recording(recording_file)
        game, recording_name = recording_file.parts[-3:-1]
        recording["session"] = game
        recording["user"] = recording_name.split(" ")[0]

        yield recording, (game, recording_name)


def convert_and_store(dataset_path, output_path, format="csv"):
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    for recording, (game, recording_name) in convert(dataset_path):
        output_file_path = output_path / f"{game}_{recording_name}"

        output_file_path.parents[0].mkdir(exist_ok=True, parents=True)

        match format.lower():
            case "csv":
                recording.round(3).to_csv(output_file_path.with_suffix(".csv"), index=False)
            case "parquet":
                recording.to_parquet(output_file_path.with_suffix(".parquet"))
            case _:
                raise Exception("unkown output format, aborting")


if __name__ == "__main__":
    dataset_path = "raw_datasets/vr_net"
    output_path = "converted_datasets/vr_net"

    convert_and_store(dataset_path, output_path, format="parquet")
