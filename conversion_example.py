import boxrr23, liebers_beat_saber23, liebers_hand22, liebers_lab_study21, moore_cross_domain23, rmiller_ball22, vr_net, who_is_alyx

for dset in [
    liebers_beat_saber23,
    boxrr23,
    liebers_hand22,
    liebers_lab_study21,
    moore_cross_domain23,
    rmiller_ball22,
    vr_net,
    who_is_alyx,
]:
    dset_name = dset.__name__
    print(f"starting conversion of {dset_name}")
    dset.convert_and_store(
        dataset_path=f"original_datasets/{dset_name}", output_path=f"converted_datasets/{dset_name}", format="parquet"
    )
