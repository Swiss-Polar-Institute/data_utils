#!/bin/bash -e
# This script uses rhash to calculate the sha1sum of files within the directory. 

if (($# == 3))
then
  DIRECTORY_PATH="${1}"
  OUTPUT_DIRECTORY="$2"
  SUB_DIRECTORY="${3}" # can be .

  if [[ ${SUB_DIRECTORY} == '.' ]]
  then
    FILE_EXTRA=""
  else
    FILE_EXTRA="_${SUB_DIRECTORY}"
  fi

  TOPDIR="$(basename ${1})"
else
  echo "Please enter a directory path of the files you would like to check and the directory where the output file should be saved."
  exit 1
fi

# Find the absolute directory for OUTPUT_DIRECTORY
if [ "${OUTPUT_DIRECTORY:0:1}" != "/" ]
then
        OUTPUT_DIRECTORY="$(pwd)/$OUTPUT_DIRECTORY"
fi

TIME_PATH="/usr/bin/time"

cd "${DIRECTORY_PATH}"
RHASH_OUTPUT_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${FILE_EXTRA}_sha1sum_output.txt"
RHASH_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${FILE_EXTRA}_sha1sum_log.txt"
TIME_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${FILE_EXTRA}_rhash_time_log.txt"
"${TIME_PATH}" -a -o "$TIME_LOG_FILENAME" rhash --sha1 -r --percents --output="${RHASH_OUTPUT_FILENAME}" --log="${RHASH_LOG_FILENAME}" ${SUB_DIRECTORY}

## loop through the folders within the top directory and run rhash on each of these, outputting the files in the required directory.
#for subdir in *; do
#    if [[ -d "$subdir" ]]; then
#        echo "Processing $TOPDIR/$subdir"
#        RHASH_OUTPUT_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${EXTRA}_${subdir}_sha1sum_output.txt"
#        RHASH_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${EXTRA}_${subdir}_sha1sum_log.txt"
#	TIME_LOG_FILENAME="${OUTPUT_DIRECTORY}/${TOPDIR}${EXTRA}_${subdir}_rhash_time_log.txt"
#        "${TIME_PATH}" -a -o "$TIME_LOG_FILENAME" rhash --sha1 -r --percents --output="${RHASH_OUTPUT_FILENAME}" --log="${RHASH_LOG_FILENAME}" "${subdir}"
#    fi
#done
