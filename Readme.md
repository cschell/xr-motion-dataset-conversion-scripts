# XR Motion Dataset Conversion Tool

Welcome to our XR Motion Dataset Conversion repository. This tool is designed for researchers and developers
working with XR motion datasets, providing a unified and standardized approach to handling these datasets as proposed in
our [paper](https://cschell.github.io/kinematic-maze).

## About This Repository

This repository contains Python scripts capable of converting various XR motion datasets into our proposed standardized
format. The aim is to streamline data handling and analysis processes in XR research by promoting a consistent format across
different datasets.

## Standardized Format

Our `convert.py` scripts transform each XR motion dataset into a uniform format following our proposed
specifications, which includes:

1. **Coordinate System:** X: Right, Y: Up, Z: Forward (RUF)
2. **Units of Measurement**: Centimeters
3. **Representation of Rotation:** Quaternions
4. **Time Encoding**: Column with relative time in milliseconds
5. **File Structure**: Column mapping:
    - `delta_time_ms`
    - `head_pos_x`
    - `head_pos_y`
    - `head_pos_z`
    - `head_rot_x`
    - `head_rot_y`
    - `head_rot_z`
    - `head_rot_w`
    - `left_hand_pos_x`
    - `left_hand_pos_y`
    - `left_hand_pos_z`
    - `left_hand_rot_x`
    - `left_hand_rot_y`
    - `left_hand_rot_z`
    - `left_hand_rot_w`
    - `right_hand_pos_x`
    - `right_hand_pos_y`
    - `right_hand_pos_z`
    - `right_hand_rot_x`
    - `right_hand_rot_y`
    - `right_hand_rot_z`
    - `right_hand_rot_w`
6. **File Format:** CSV

## Setup Instructions

Before you can use these scripts, you need to set up your environment:

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

For each dataset, there is one module with a conversion script. To do the conversion yourself, create a
script, and import the respective module. For example, to convert the Who Is Alyx? dataset, you can follow
these steps:

1. download the dataset (see links in the table below).
2. create a Python script in this directory
3. import and use the conversion script:
```python
import who_is_alyx

converter = who_is_alyx.convert(dataset_path="path/to/the/downloaded/dataset")

# the returned tuple returned by `converter` differs for each dataset, please check
# the source code of `convert` for details
for recording, (user, session) in converter:
   print(f"loaded session {session} of user {user}")

   recording # this is your pandas DataFrame with the loaded recording
```
4. if you want to convert and store the whole dataset, you can use `convert_and_store`:
```python
import who_is_alyx

who_is_alyx.convert_and_store(
        dataset_path="path/to/the/downloaded/dataset",
        output_path="path/to/converted/dataset",
        format="csv" # or "parquet"
    )
```

You can check out [xr_motion_dataset_catalogue_conversion.py] as an example – this is the script we used to
convert each dataset for the [XR Motion Dataset Catalogue](https://huggingface.co/datasets/cschell/xr-motion-dataset-catalogue).

## Dataset Overview

This repository provides conversion scripts for the datasets in the table below. Follow the source links
to download desired datasets. We have also uploaded most of theese datasets into our
[XR Motion Dataset Catalogue](https://huggingface.co/datasets/cschell/xr-motion-dataset-catalogue),
so you can go there for quick and easy access of already converted and aligned datasets.

| Dataset Name       | Description                                                                                                                                                 |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LiebersLabStudy21  | Users performing specific bowling and archery motions.                                                                                                      | [source](https://www.hci.wiwi.uni-due.de/en/publikationen/understanding-user-identification-in-virtual-reality-through-behavioral-biometrics-and-the-effect-of-body-normalization/) |
| LiebersHand22      | Users performing interactions with various interface elements, such as buttons and sliders, in AR and VR environments for motion-based user identification. | [source](https://www.hci.wiwi.uni-due.de/en/publications/identifying-users-by-their-hand-tracking-data-in-augmented-and-virtual-reality)                                            |
| RMillerBall22      | Users performing ball throwing actions in VR.                                                                                                               | [source](https://github.com/Terascale-All-sensing-Research-Studio/VR-Biometric-Authentication)                                                                                      |
| Who-Is-Alyx        | Users playing the game 'Half-Life: Alyx' in VR.                                                                                                             | [source](https://github.com/cschell/who-is-alyx)                                                                                                                                    |
| BOXRR              | Users playing the game Beat Saber and Tilt Brush in VR.                                                                                                     | [source](https://rdi.berkeley.edu/metaverse/boxrr-23/)                                                                                                                              |
| LiebersBeatSaber23 | Users playing the game Beat Saber.                                                                                                                          | [source](https://www.hci.wiwi.uni-due.de/en/publikationen/exploring-the-stability-of-behavioral-biometrics-in-virtual-reality-in-a-remote-field-study/)                             |
| MooreCrossDomain23 | Users performing assembly tasks in VR.                                                                                                                      | [source](https://github.com/tapiralec/Identifying_Virtual_Reality_Users_Across_Domain_Specific_Tasks)                                                                               |
| VR.net             | Users playing various VR games, designed for cybersickness research.                                                                                        | [source](https://vrnet.ahlab.org)                                                                                                                                                   |

## License

This project is licensed under Creative Commons. Please see the LICENSE file for more details.