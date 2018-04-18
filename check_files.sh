#!/bin/bash 
# This script uses rhash to calculate the sha1sum of files within the directory. 

if (($# != 2))
then
  echo "Please enter a directory path of the files you would like to check and the directory where the output file should be saved."
  exit 1
fi

OUTPUT_DIRECTORY="$2"

# Find the absolute directory for OUTPUT_DIRECTORY
if [ "${OUTPUT_DIRECTORY:0:1}" != "/" ]
then
        OUTPUT_DIRECTORY="$(pwd)/$OUTPUT_DIRECTORY"
fi

DIRECTORY_PATH="$1"

TIME_PATH="/usr/bin/time"

cd "${DIRECTORY_PATH}"
TOPDIR="$(basename ${DIRECTORY_PATH})"

# loop through the folders within the top directory and run rhash on each of these, outputting the files in the required directory.
for subdir in *; do
    if [[ -d "$subdir" ]]; then
        echo "Processing $TOPDIR/$subdir"
        RHASH_OUTPUT_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}_${subdir}_sha1sum_output.txt"
        RHASH_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}_${subdir}_sha1sum_log.txt"
	TIME_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}_${subdir}_rhash_time_log.txt"
        "${TIME_PATH}" -a -o "$TIME_LOG_FILENAME" rhash --sha1 -r --percents --output="${RHASH_OUTPUT_FILENAME}" --log="${RHASH_LOG_FILENAME}" "${subdir}"
    fi
done
