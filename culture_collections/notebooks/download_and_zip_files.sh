c=1
cat ./culture_collections/notebooks/all_files.txt | while read file; do
    if [ -e "/mnt/embl/scratch/hellgoth/planexm_zips/$file.zip" ]; then
        echo "File already exists: $file.zip"
        echo "Done: $c / 1186"
        c=$((c + 1))
    else
        # mc cp -q -r "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/$file" "/scratch/hellgoth/planexm_zips"
        # echo "Downloaded: $file"
        # zip -q -r "/scratch/hellgoth/planexm_zips/$file.zip" "/scratch/hellgoth/planexm_zips/$file"
        # echo "Zipped: $file"
        # rm -rf "/scratch/hellgoth/planexm_zips/$f"
        # echo "Removed: $file"
        echo "Downloading and zipping: $file"
        echo "Done: $c / 1186"
        c=$((c + 1))
    fi
done

# file=rcc6324_pfa_nhs-tub-npc-dna_20231121_fm_04.ome.zarr
# echo "/mnt/embl/scratch/hellgoth/planexm_zips/$file.zip"
# if [ -e "/mnt/embl/scratch/hellgoth/planexm_zips/$file.zip" ]; then
#     echo "File already exists: $file.zip"
# else
#     echo "Downloading and zipping: $file"
#     echo "Done: 1 / 1"
# fi