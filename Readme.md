# XR Motion Dataset Conversion Tool

Welcome to our XR Motion Dataset Conversion repository. This tool is designed for researchers and developers
working with XR motion datasets, providing a unified and standardized approach to handling these datasets as proposed in
our [paper](#TODO). Furthermore, this tool is designed to perform the required pre-processing of the datasets so that they can be 
visualized with our [XR Motion Player](#TODO) in order to get visual insights from the dataset.

## About This Repository

This repository contains Python scripts capable of converting various XR motion datasets into our proposed standardized format. The
aim is to streamline data handling and analysis processes in XR research by promoting a consistent format across
different datasets.

## Specifications

1. **Coordinate System**<br>
   Understanding the coordinate system used in a dataset is essential for accurately interpreting spatial data. If it is
   unclear how the X, Y, and Z coordinates correspond to axes like up, forward, and left/right, spatial relationships
   cannot be properly reconstructed. For example, the same motion will suddenly look very unrealistic if ‘X’ gets
   interpreted as ‘up’ instead of ‘Y’ – not only because positions are flipped, but also because rotations will be
   misinterpreted. The datasets analyzed for this work all use two similar coordinate systems, which only slightly
   differ: one is left-handed, so Z points ‘right’, the other right-handed, so Z points ‘left’. Even though this
   difference is relatively subtle, assuming the wrong coordinate system will result in highly corrupted motions and
   will lead to incorrect conclusions.
2. **Units of Measurement**<br>
   The units of measurement used in a dataset, whether meters, centimeters, custom units, etc., are fundamental for
   accurately assessing and comparing spatial data. For example, assuming centimeters instead of meters would lead to
   peripherals appearing a 100 times closer and motions 100 times slower.
3. **Representation of Rotations**<br>
   Misinterpreting rotations (e.g., Euler angles, quaternions, or transformation matrices) leads to incorrect
   reconstructions of motions. For instance, Euler notation seems straightforward at first glance, as it defines
   rotations around the X, Y, and Z axes. Yet, to apply it correctly, one needs to know whether the rotations are
   intrinsic (rotating about the axes of the moving coordinate system) or extrinsic (rotating about the axes of the
   fixed coordinate system), as well as the order of applying rotations along each axis. Like before, wrong assumptions
   regarding this are easy to miss, but will lead to incorrectly reconstructed motions.
4. **Time Encoding**<br>
   Accurate timing information is crucial for understanding the sequence of frames and duration of movements in motion
   data. This can be represented through timestamps or a fixed framerate. Without clear timing data, the dynamics of
   motion cannot be accurately analyzed. Assuming the wrong timing of frames will effectively lead to reconstructed
   motions to be too fast or too slow.
5. **Structure**<br>
   The structure of a dataset, particularly how recordings are organized, significantly impacts data accessibility. A
   poorly structured dataset can lead to confusion about which files correspond to specific sessions or participants.
   For example, if a dataset combines multiple recordings into a single file without clear demarcation, it becomes
   challenging to isolate and analyze individual recordings. Conversely, if every motion sequence is saved as a separate
   file without a systematic naming convention or indexing, researchers might struggle to locate and aggregate relevant
   data for their studies. This issue is even more relevant in large datasets, where the sheer volume of recordings
   necessitates a well-defined organizational scheme to facilitate easy access and selection. Efficient data retrieval
   and analysis depend on a logical, well-documented structure that aligns with the research objectives.
6. **File Format**<br>
   The file format is vital in determining how recordings can be loaded and attributes correctly labeled. An
   unsuitable or poorly documented file format can lead to misunderstandings. This affects the integrity of the
   research, as conclusions drawn from improperly interpreted data are likely to be erroneous.

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

## Usage Example

To convert a dataset, simply run the appropriate `convert.py` script. For example:
python convert.py --input /path/to/dataset --output /path/to/standardized/dataset

## Dataset Overview

Below is a list of datasets currently supported by our [XR Motion Dataset Catalogue](https://huggingface.co/datasets/cschell/xr-motion-dataset-catalogue). Each dataset has its specific `convert.py` script:

| No. | Dataset Name       | Description                                                                                                                                                                         | Link                                   |
|-----|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|
| 1   | LiebersLabStudy21  | This dataset focuses on users performing specific bowling and archery motions.                                                                                                      | [More Info](link to dataset or script) |
| 2   | LiebersHand22      | This dataset focuses on users performing interactions with various interface elements, such as buttons and sliders, in AR and VR environments for motion-based user identification. | [More Info](link to dataset or script) |
| 3   | RMillerBall22      | This dataset focuses on capturing the motions of users performing ball throwing actions in VR.                                                                                      | [More Info](link to dataset or script) |
| 4   | Who-Is-Alyx        | This dataset focuses on capturing the motions of users playing the game 'Half-<Life: Alyx' in VR.                                                                                   | [More Info](link to dataset or script) |
| 5   | BOXRR Beatsaber    | This dataset focuses on users playing the game Beatsaber in VR and aims to provide a large-scale human motion dataset for researchers and studies.                                  | [More Info](link to dataset or script) |
| 6   | BOXRR Tiltbrush    | This dataset focuses on users playing the game Tiltbrush in VR and aims to provide a large-scale human motion dataset for researchers and studies.                                  | [More Info](link to dataset or script) |
| 7   | LiebersBeatSaber23 | This dataset focuses on users playing the game Beatsaber and is aimed at user identification through motion.                                                                        | [More Info](link to dataset or script) |
| 8   | MooreCrossDomain23 | This dataset focuses on users performing assembly tasks in VR and is also intended for user identification research.                                                                | [More Info](link to dataset or script) |
| 9   | VR.net             | This dataset focuses on users playing various VR games and was designed for cybersickness research.                                                                                 | [More Info](link to dataset or script) |

## License

This project is licensed under Creative Commons. Please see the LICENSE file for more details.