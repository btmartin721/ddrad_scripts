#!/usr/bin/env python3

import argparse
import os
import shutil
import sys


def main():

    arguments = Get_Arguments()

    locidir = arguments.dir
    blacklist_dir = arguments.blacklist_dir

    # Validate that input file exists.
    check_code = check_if_file_exists(arguments.log)
    if check_code == 1:
        return 1 # Die if input file doesn't exist.

    # Get filenames for bad loci from IQ-TREE log file.
    blacklist = list()
    blacklist = get_bad_files(arguments.log)

    # Abort if there were no uninformative/invariant sites.
    if not blacklist:
        print("No blacklisted loci were found in log file. Aborting program.")
        return 1

    print("\n\nSearching for log file in parent directory: " + \
            os.path.abspath(os.path.join(locidir, os.pardir)) + "\n")

    print("Directory containing loci files (must be located within parent "
            "directory): " + locidir  + "\n")

    check_code = move_blacklisted(blacklist, locidir, blacklist_dir)
    if check_code == 1:
        return 1

    return 0

################################################################################

def dir_path(string):
# Checks if directory exists or raises exception.
# Arguments:
#       string: Name of directory
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def move_blacklisted(list_of_files, dir, b_dir):
# Creates blacklist directory and moves blacklisted files to it.
# Arguments:
#       list of blacklisted filenames
#       parent directory path
#       blacklist directory name; goes in parent directory
# Returns:
#       int: 0 if no errors, 1 if error occurred.

    parent_dir = os.getcwd() # Get path to parent directory

    # Creates blacklist DIR; Aborts if blacklist directory already exists
    if not os.path.exists(b_dir):
        try:
            os.mkdir(b_dir)
        except OSError:
            print("Creation of the directory '%s' failed." % b_dir)
        else:
            print("Successfully created the blacklist directory\n")
    else:
        print("Error: Blacklist directory '%s' already exists." % b_dir)
        return 1

    print("Changing into loci directory", end="...")
    os.chdir(dir) # Changes directory to argument passed for '--dir'
    print("DONE!\n")

    blist_dir = parent_dir + "/" + b_dir + "/"

    print("Moving blacklisted loci files to " + parent_dir + "/" + b_dir, end="...\n")

    # Moves the files in list_of_files to blacklist DIR
    for file in list_of_files:
        try:
            shutil.move(file, blist_dir)
        except (OSError, IOError, Error) as e:
            print("Error moving {} to {}: {}".format(file, blist_dir, e))
            return 1

    print("DONE!!!\n")
    print("Moved {} loci files to {} directory\n".format(str(len(list_of_files)), b_dir))
    remaining_file_count = len([name for name in os.listdir('.') if os.path.isfile(name)])
    print("{} loci files remain in {}\n".format(remaining_file_count, dir))
    return 0

def get_bad_files(file):
# Get bad loci from IQ-TREE log file.
# The bad filenames are the last element of the split method when the
# line starts with "WARNING: No ")
# Arguments:
#       filename of IQ-TREE log file.
# Returns:
#       list: list of blacklisted file names.
    result_list = list()
    with open(file, "r") as fin:
        for line in fin:
            if line.startswith("WARNING: No "):
                line = line.rstrip()
                result = line.split()[-1]
                result_list.append(result)
    return result_list


def check_if_file_exists(filename):
    # Check if file exists
    # Arguments:
    #       Name of input file
    # Returns:
    #   int: 0 if successful, 1 if errors.
    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist or cannot be "
                "read.\n")
        return 1
    finally:
        file.close()

    return 0

def Get_Arguments():
    # Parse command-line arguments using argparse.
    # Returns:
    #       Object containing command-line arguments.
    parser = argparse.ArgumentParser(description="Gets phylogenetically  "
                                    "uninformative loci listed in "
                                    "IQ-TREE log file.",
                                    add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")


    required_args.add_argument("-l", "--log",
                                type=str,
                                required=True,
                                help="Input IQ-TREE log file")

    required_args.add_argument("-d", "--dir",
                                type=dir_path,
                                required=True,
                                help="Path to directory containing files for all"
                                "loci")

    optional_args.add_argument("-b", "--blacklist_dir",
                                type=str,
                                required=False,
                                default="blacklist",
                                help="Specify name of blacklist directory; "
                                    "default = 'blacklist'")

    optional_args.add_argument("-h", "--help", action="help",
                        help="Displays this help menu")


    args = parser.parse_args()

    return args

################################################################################

if __name__ == '__main__':
    rtrn_code = main()
    print("Program finished with exit status " + str(rtrn_code) + "\n")
    sys.exit(rtrn_code)
