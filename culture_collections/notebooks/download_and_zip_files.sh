c=1
while read f; do
    mc cp -q -r "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/$f" "/scratch/hellgoth/planexm_zips"
    echo "Downloaded: $f"
    zip -q -r "/scratch/hellgoth/planexm_zips/$f.zip" "/scratch/hellgoth/planexm_zips/$f"
    echo "Zipped: $f"
    rm -rf "/scratch/hellgoth/planexm_zips/$f"
    echo "Removed: $f"
    echo "Done: $c / 1186"
    c=$((c + 1))
done < ./culture_collections/notebooks/all_files.txt