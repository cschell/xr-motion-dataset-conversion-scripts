import warnings
from pathlib import Path
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[1]))
from conversion_helpers import _convert_coord_system_from_RUB_to_RUF, _convert_m_to_cm

column_mapping = {
    "Head_pos_x": "head_pos_x",
    "Head_pos_y": "head_pos_y",
    "Head_pos_z": "head_pos_z",
    "Head_rot_x": "head_rot_x",
    "Head_rot_y": "head_rot_y",
    "Head_rot_z": "head_rot_z",
    "Head_rot_w": "head_rot_w",
    "Left_pos_x": "left_hand_pos_x",
    "Left_pos_y": "left_hand_pos_y",
    "Left_pos_z": "left_hand_pos_z",
    "Left_rot_x": "left_hand_rot_x",
    "Left_rot_y": "left_hand_rot_y",
    "Left_rot_z": "left_hand_rot_z",
    "Left_rot_w": "left_hand_rot_w",
    "Right_pos_x": "right_hand_pos_x",
    "Right_pos_y": "right_hand_pos_y",
    "Right_pos_z": "right_hand_pos_z",
    "Right_rot_x": "right_hand_rot_x",
    "Right_rot_y": "right_hand_rot_y",
    "Right_rot_z": "right_hand_rot_z",
    "Right_rot_w": "right_hand_rot_w",
}


def load_recordings(dataset_path, system, user, session):
    all_recordings_by_joint = []

    for joint in ["Head", "Left", "Right"]:
        file_name = dataset_path / f"{system}_{user}_{session}_{joint}.csv"
        column_names = [f"{joint}_pos_{xyz}" for xyz in "xyz"] + [f"{joint}_rot_{xyz}" for xyz in "wxyz"] + ["trigger"]

        # for some files read_csv throws warnings
        # as it has problems dealing with the seperator lines "****..."
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw_recording = pd.read_csv(
                file_name,
                names=column_names,
                index_col=False,
            )

        joint_recordings = [
            df.dropna() for _, df in raw_recording.groupby(raw_recording.isna().any(axis=1).cumsum()) if len(df) > 1
        ]

        all_recordings_by_joint.append(joint_recordings)

    all_recordings = []
    for rs in zip(*all_recordings_by_joint):
        all_recordings.append(pd.concat(rs, axis=1).rename(columns=column_mapping)[column_mapping.values()].astype("float"))

    return all_recordings


def convert_recording(recording):
    fps = len(recording) // 3
    converted_recording = (
        recording.pipe(_convert_m_to_cm)
        .pipe(_convert_coord_system_from_RUB_to_RUF)
        .assign(delta_time_ms=lambda df: np.arange(len(df)) * (1000 / fps))
    )

    return converted_recording


def convert(dataset_path: str):
    dataset_path = Path(dataset_path) / "VR Motions"

    data_overview = (
        pd.DataFrame(
            [f.stem.split("_") for f in dataset_path.glob("*.csv")],
            columns=["system", "user", "session", "device"],
        )[["system", "user", "session"]]
        .drop_duplicates()
        .sort_values(["user", "system", "session"])
        .reset_index(drop=True)
    )

    for _idx, row in tqdm(data_overview.iterrows(), total=len(data_overview)):
        system, user, session = row
        recordings = load_recordings(dataset_path, system, user, session)
        converted_recordings = [convert_recording(rec) for rec in recordings]

        for repetition, recording in enumerate(converted_recordings):
            yield recording, (system, user, session, repetition)


def convert_and_store(dataset_path, output_path, format="csv"):
    output_path = Path(output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    for recording, (system, user, session, repetition) in convert(dataset_path):
        output_file_path = output_path / f"{system}_{user}_{session}_{repetition}"

        recording = recording.assign(
            system=system,
            user=user,
            session=session,
            repetition=repetition,
        )

        match format.lower():
            case "csv":
                recording.round(3).to_csv(output_file_path.with_suffix(".csv"), index=False)
            case "parquet":
                recording.to_parquet(output_file_path.with_suffix(".parquet"))
            case _:
                raise Exception("unkown output format, aborting")


if __name__ == "__main__":
    dataset_path = "raw_datasets/rmiller_ball22/VR Motions"
    output_path = "converted_datasets/rmiller_ball22"

    convert_and_store(dataset_path=dataset_path, output_path=output_path)
