while read f; do
    # mc cp -r "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/$f" "/scratch/hellgoth/planexm_zips"
    echo "Downloaded: $f"
    zip -q -r "/scratch/hellgoth/planexm_zips/$f.zip" "/scratch/hellgoth/planexm_zips/$f"
    echo "Zipped: $f"
done < ./culture_collections/notebooks/all_files.txt