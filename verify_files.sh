#!/bin/bash
# This script uses rhash to verify a set of files that have been listed by rhash.

if (($# != 3))
then
  echo "Please enter a directory path to the files you would like to verify, where the rhash file output is stored and the directory where the verification output files should be saved."
  exit 1
fi

DIRECTORY_PATH="$1"
RHASH_FILE_DIRECTORY="$2"
OUTPUT_DIRECTORY="$3"

TIME_PATH="/usr/bin/time"

cd "${DIRECTORY_PATH}"

# Loop through the folders in the top directory and check the rhash is correct. Output the results and list where there are errors.
for directory in *; do
    if [[ -d "$directory" ]]; then
        echo "Verifying $directory"
        RHASH_VERIFICATION_OUTPUT_FILENAME="${OUTPUT_DIRECTORY}/${directory}_sha1sum_verification_output.txt"
        RHASH_VERIFICATION_LOG_FILENAME="${OUTPUT_DIRECTORY}/${directory}_verification_log.txt"
        TIME_LOG_FILENAME="${OUTPUT_DIRECTORY}/${directory}_verification_time_log.txt"
        VERIFICATION_ERRORS_FILENAME="${OUTPUT_DIRECTORY}/verification_errors.txt"
        "${TIME_PATH}" -a -o "$TIME_LOG_FILENAME" rhash -c "${RHASH_FILE_DIRECTORY}/${directory}_sha1sum_output.txt" --output="${RHASH_VERIFICATION_OUTPUT_FILENAME}" --log="${RHASH_VERIFICATION_LOG_FILENAME}"
        RETURN_VALUE="$?"
        if [ $RETURN_VALUE -ne 0 ]; then 
            echo "$directory has an error"
            grep 'ERR$' $RHASH_VERIFICATION_OUTPUT_FILENAME >> $VERIFICATION_ERRORS_FILENAME  
        fi
    fi
done
