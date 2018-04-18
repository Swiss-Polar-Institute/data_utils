#!/usr/bin/python3

# This scrpit has been created to compare two large areas of data storage and find which files are missing in the main data are, but are present in the backup and therefore need to be copied over still.

# This script will compare lists of files (which have a directory path and a check sum) and produce the following output lists: 
# - files that occur in both lists
# - files that are missing in directory a but are in directory b
# - files that are missing in directory b but are in directory a

# We will think of directory a as being the principal copy of the data, i.e. ALL the files should exist here. Directory b is the backup and generally has various copies of the data that should be in directory a. 

# Import packages
import csv
import os

def how_to_do_file_comparison(possible_storage_locations, possible_directories)
    """This funciton takes an input from the user who decides how the file comparison is going to work. It outputs a string which then decides how the rest of the script runs."""

    method = str(input("Would you like to compare the files by directory (eg. ace_data vs. ace_data_end_of_leg4) or by storage location (eg. spinas1 vs. spinas1-migr)? Enter directory or storage location.  "))

    if method like "directory":
        get_directories_to_compare(possible_directories)
    elif method like "storage location":
        get_storage_locations_to_compare(possible_storage_locations)
    else:
        print("Your input was invalid. It should be directory or storage location. This script will now exit. Please retry.")
        exit

    return method


def get_storage_locations_to_compare(possible_storage_locations):
    """This function will ask the user for the storage locations to compare and output them in a tuple."""

    storage_location1 = None
    storage_location2 = None

    while storage_location1 not in possible_storage_locations:
        storage_location1 = str(input("Type the name of the first storage location that you would like to compare.  "
        if storage_location1 in possible_storage_locations: 
            print("Going to compare ", storage_location1)
        else:
            print("That storage location does not exist. Please type another storage location.  ")

    while storage_location2 not in possible_storage_locations:
        storage_location2 = str(input("Type the name of the second storage location that you would like to compare.  ")
        if storage_location2 in possible_storage_locations:
            print("Going to compare ", storage_location2)
        else:
            print("That storage location does not exist. Please type another storage location.  ")

    storage_locations = (storage_location1, storage_location2)

    return storage_locations


def get_directories_to_compare(possible_directory_locations):
    """This function will ask the user for the two directories to output them in a tuple."""

    directory1 = None
    directory2 = None

    while directory1 not in possible_directories:
        directory1 = str(input("Type the name of the first directory that you would like to compare.  "
        if directory1 in possible_directories:
            print("Going to compare ", directory1)
        else:
            print("That directory does not exist. Please type another directory.  ")

    while directory2 not in possible_directories:
        directory2 = str(input("Type the name of the second directory that you would like to compare.  ")
        if directory2 in possible_directories:
            print("Going to compare ", directory2)
        else:
            print("That directory does not exist. Please type another directory.  ")

    directories = (directory1, directory2)

    return directories


def dict_files_in_storage_location(storage_location, dir_path_to_files):
    """Create a dictionary of all of the files in a storage location with the directory as the key and the storage location and filename in a tuple."""

    filename_appendix = "sha1sum_output.txt"
    dir_name_appendix = "compiled_output"

    os.chdir(dir_path_to_files+"/"+storage_location+"_"+dir_name_appendix)

    file_list = os.listdir()

    dict_files = {}

    for file in file_list:
        directory = get_directory_from_filename(file)
        dict_files_location = {directory: (storage_location, file)}
        dict_files.update(dict_files_location)

    return dict_files 
        

def compare_dictionaries_on_key(key, dictionary1, dictionary2):
    """Compare two dictionaries on a key that is defined. Output matching results in a list of lists."""

    comparison_files = []

    for key in dictionary1.keys():
        compare_these_pairs = [] 
        if key in dictionary2.keys():
            compare_these_pairs = [dictionary1[key][1], dictionary2[key][1]]
    comparison_files.append(compare_these_pairs)


    





        
def get_filename(filepath):
    """Get the filename from a full filepath."""

    filename = os.path.basename(file)

    return filename


def split_filename(filename):
    """Get the different parts of the filename."""

    filename_split = filename.split("_")

    return filename_split


def get_storage_location_from_filename(filename)
    """Get the storage location from the split filename (tuple) and output as string."""

    storage_location = split_filename(filename)[0]

    return storage_location


def get_directory_from_filename(filename)
    """Get the directory from the split filename (tuple) and output as string."""

    storage_location = get_storage_location_from_filename(filename)
    remainder = filename.split(storage_location)
    directory = remainder.split(filename_appendix).strip("_")

    return directory
   

def create_list_from_file(input_file):
    """Read a file into a list of lists where the nested list is split on whitespace."""
    
    file_list = []

    with open(input_file) as inputfile:
        for line in inputfile:
            file_list.append(line.strip().split('  ', 1)) # the check sum and file name are separated by a double whitespace

#    print(file_list)
    return file_list


def check_length_list(input_file, file_list, file_type):
    """Check that the length of an input file is the same as the list from reading it in. Puts the file type in the printed output for clarity."""

    count_file_length = len(open(input_file).readlines())
    count_file_list = len(file_list)

    if count_file_length != count_file_list:
        print(file_type, "file length: ", count_file_length)
        print(file_type, "file list: ", count_file_list)
    else: 
        print(file_type, " file length is the same as the list of files: all of the files have been read in. Number of files: ", count_file_list)


def nested_lists_to_sets(nested_lists):
    """Convert a list of lists (nested lists) into a list of tuples then convert this to a set."""

    list_of_tuples = [tuple(l) for l in nested_lists]
    output_set = set(list_of_tuples)

    return output_set


def difference_between_sets(set_a, set_b):
    """Find elements that are in set b but not in set a."""

    missing_elements = set_b - set_a

    print("There are ", missing_elements, " missing elements.")

    return missing_elements


def write_set_to_file(set_name, output_file):
    """Read through a set and output the elements to a file."""

    try: 
        output = open(output_file, 'w')
    except IOError:
        print("Not able to open outfile: ", output_file)
        exit(1)
    else:
        with output:
            writer = csv.writer(output, lineterminator='\n')
            for element in set_name:
                writer.writerows([element])
                print(element, " written to file")

###########################
# The following details are specific to comparing the ace data.

possible_storage_locations = ['spinas1', 'spinas2', 'spinas1-migr', 'spinas2-migr', 'testspinas1', 'testspinas2', 'testspinas1-migr', 'testspinas2-migr']
possible_directories = ['ace_data', 'data_admin', 'work_leg1', 'work_leg4']


###########################

# Ask the user how to deal with the file comparison.
method_of_file_comparison = how_to_do_file_comparison(possible_storage_locations, possible_directories)

## ASSUMING THAT WE CHOOSE STORAGE LOCATIONS FOR NOW
# Get a tuple of the storage locations that the user wants to compare: 
storage_locations = get_storage_locations_to_compare(possible_storage_locations)

# Create a dictionary of the files to compare. 
files_storage_location1 = dict_files_in_storage_location(storage_location1, dir_path_to_files) 
files_storage_location2 = dict_files_in_storage_location(storage_location2, dir_path_to_files) 

# Compare the dictionaries of files on the key (directory) and output a list of pairs of files (in lists) to compare.
files_to_compare = compare_dictionaries_on_key(files_storage_location1, files_storage_location2)

# Run through the pairs, doing the comparison.
for pairs in files_to_compare: 
    master_file = pairs[0]
    backup_file = pairs[1]

# ALL OF THE THINGS BELOW NEED INTEGRATING INTO THE FOR LOOP ABOVE. WOULD THIS BE BETTER IN A CLASS MAYBE? 



# Read the master file list into a list of lists, where the nested lists are the checksum and filename of the files being queried.
master_file = '/home/jen/projects/ace_data_management/wip/checking_nas/test_files_spinas1/spinas1_work_leg1_sha1sum_output.txt'
master_file_list = create_list_from_file(master_file)

# Check that list length is the same length as the number of rows in the file that is being read in.
file_type = 'master'
check_length_list(master_file, master_file_list, file_type)

# Read the backup file list into a list of lists, where the nested lists are the checksum and filename of the files being queried.
backup_file = '/home/jen/projects/ace_data_management/wip/checking_nas/test_files_spinas2/spinas2_work_leg1_sha1sum_output.txt'
backup_file_list = create_list_from_file(backup_file)

# Check that list length is the same length as the number of rows in the file that is being read in.
file_type = 'backup'
check_length_list(backup_file, backup_file_list, file_type)

# Convert the lists to sets.
master_file_set = nested_lists_to_sets(master_file_list)
backup_file_set = nested_lists_to_sets(backup_file_list)

# Compare the sets.
missing_backup_files = difference_between_sets(master_file_set, backup_file_set)

# Output the missing files (those in backup and not in master) to a file.
output_file = '/home/jen/projects/ace_data_management/wip/checking_nas/test_missing_files.csv'
write_set_to_file(missing_backup_files, output_file)

# Check that the number of missing elements is the same as the number of lines written to the output file.
file_type = 'missing'
check_length_list(output_file, missing_backup_files, file_type)
