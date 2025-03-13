import subprocess

# Function to check vulnerability using curl and grep
def check_vulnerability(target_file, vulnerable_file):
    # Set to keep track of checked URLs to avoid duplicates
    checked_urls = set()

    # Open the vulnerable_website.txt file in append mode
    with open(vulnerable_file, 'a') as vulnerable_output:
        # Open and read the target file
        with open(target_file, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace

                # Replace everything after the first "=" with "cute</>"
                if '=' in line:
                    modified_url = line.split('=')[0] + '=cute</>'

                    # Skip if the URL has already been checked
                    if modified_url in checked_urls:
                        continue

                    # Mark the URL as checked
                    checked_urls.add(modified_url)

                    try:
                        # Use curl -sk to fetch the URL and grep to search for "cute</>"
                        result = subprocess.run(
                            ["curl", "-sk", modified_url], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True
                        )
                        
                        # Check if "cute</>" is in the curl response
                        if "cute</>" in result.stdout:
                            # Print the vulnerable URL to the screen
                            print(f"Vulnerable website found: {modified_url}")
                            
                            # Write the vulnerable URL to the vulnerable_website.txt file
                            vulnerable_output.write(modified_url + '\n')
                        
                        elif result.returncode != 0:
                            print(f"Error fetching {modified_url}: {result.stderr}")

                    except Exception as e:
                        print(f"Unexpected error with {modified_url}: {e}")

# Main function to prompt user for file names
def main():
    # Ask the user to input the target file and vulnerable file names
    target_file = input("Enter the name of the target file (e.g., targets.txt): ")
    vulnerable_file = input("Enter the name of the output file for vulnerable URLs (e.g., vulnerable_website.txt): ")

    # Call the vulnerability check function with the provided file names
    check_vulnerability(target_file, vulnerable_file)

if __name__ == "__main__":
    main()
