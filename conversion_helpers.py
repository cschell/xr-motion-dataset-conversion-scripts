from scipy.spatial.transform import Rotation as R

JOINTS = ["head", "left_hand", "right_hand"]


def _convert_m_to_cm(df):
    df = df.copy()

    for c in df.columns:
        if "_pos_" in c:
            df[c] *= 100

    return df


def _convert_coord_system_from_RUB_to_RUF(df):
    df = df.copy()

    for c in df.columns:
        if c.endswith("_z") or c.endswith("_w"):
            df[c] *= -1

    return df


def _euler_to_quat(df):
    df = df.copy()
    for joint in JOINTS:
        quat_columns = [f"{joint}_rot_{xyz}" for xyz in "xyzw"]
        euler_columns = [f"{joint}_rot_{xyz}" for xyz in "xyz"]
        df[quat_columns] = R.from_euler("xyz", df[euler_columns], degrees=True).as_quat(canonical=True)
    return df
