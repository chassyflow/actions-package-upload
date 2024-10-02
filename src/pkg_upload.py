import sys
import glob

# Function to easily write to github output.
def write_to_github_output(key, value):
    """
    This function takes key and value to output to github actions workflow.
    
    Args:
        key (str): The key of the output. This must match the string in output section of actions.yml
        valu (str): The value to assign to the string
    """    
    # Get the path of the $GITHUB_OUTPUT environment variable
    github_output = os.getenv('GITHUB_OUTPUT')
    
    if github_output:
        # Open the file in append mode and write the key=value pair
        with open(github_output, 'a') as output_file:
            output_file.write(f"{key}={value}\n")
        print(f"Successfully wrote {key}={value} to $GITHUB_OUTPUT")
    else:
        print("Error: $GITHUB_OUTPUT is not set in the environment")



def find_file(file_pattern):
    """
    This function takes a file name, a directory pattern, or a file prefix with wildcards.
    It searches for the file and returns the full file path.
    
    Args:
        file_pattern (str): The name of the file, or a pattern with wildcards, or the parent directory pattern.
        
    Returns:
        str: The full path to the found file, or None if no file is found.
    """
    
    # Use glob to search for the file pattern
    # The '**' pattern in glob searches recursively in subdirectories.
    files_found = glob.glob(file_pattern, recursive=True)
    
    if files_found:
        # If files are found, return the absolute path of the first one found
        return os.path.abspath(files_found[0])
    else:
        # If no files are found, return None
        return None


def main():
    # Check if the correct number of arguments are passed
    if len(sys.argv) != 5:
        print("Usage: python pkg_upload.py <inputs.artifact> <inputs.type> <inputs.architecture> <inputs.osID> <inputs.osVersion>")
        sys.exit(1)

    # Store arguments in variables
    artifact = sys.argv[1]
    type = sys.argv[2]
    architecture = sys.argv[3]
    osID = sys.argv[4]
    osVersion = sys.argv[5]

    # Print the variables (optional)
    print(f"artifact: {artifact}")
    print(f"type: {type}")
    print(f"architecture: {architecture}")
    print(f"osID: {osID}")
    print(f"osVersion: {osVersion}")

    artifact_path = find_file(artifact)

    # output to github the setatus
    write_to_github_output("status", artifact_path)


if __name__ == "__main__":
    main()
