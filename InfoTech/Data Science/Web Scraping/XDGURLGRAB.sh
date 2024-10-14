#!/bin/bash
# Default values
ROOT_DIR=""
BUSINESS=""
ASSET_TYPE=""
ASSET_VALUE=""

# Parse command line arguments
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --root_dir)
    ROOT_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    --business)
    BUSINESS="$2"
    shift # past argument
    shift # past value
    ;;
    --asset_type)
    ASSET_TYPE="$2"
    shift # past argument
    shift # past value
    ;;
    --asset_value)
    ASSET_VALUE="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $1"
    exit 1
    ;;
esac
done

# Check if required arguments are provided
if [ -z "$ROOT_DIR" ] || [ -z "$BUSINESS" ] || [ -z "$ASSET_TYPE" ] || [ -z "$ASSET_VALUE" ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 --root_dir <dir> --business <name> --asset_type <type> --asset_value <value>"
    exit 1
fi

# Construct the file path
file_path="${ROOT_DIR}/${BUSINESS}/${ASSET_TYPE}/${ASSET_VALUE}/${ASSET_VALUE}.txt"

# Check if the file exists
if [ ! -f "$file_path" ]; then
    echo "Error: File $file_path not found"
    exit 1
fi

# Function to close 10 tabs
close_tabs() {
    echo "Closing 10 tabs..."
    for i in {1..10}; do
        xdotool key ctrl+w
        sleep 0.5
    done
}

# Counter for URLs
counter=0
batch_counter=0

# Read URLs from file and open with xdg-open
while IFS= read -r url
do
    if [ -z "$url" ]; then
        echo "Skipping empty line"
        continue
    fi
    
    # Add https:// if not present
    if [[ ! $url =~ ^https?:// ]]; then
        url="https://$url"
    fi
    
    echo "Opening URL: $url"
    xdg-open "$url" || echo "Error opening $url"
    
    counter=$((counter + 1))
    batch_counter=$((batch_counter + 1))
    
    echo "Sleeping for 5 seconds (URL $counter, Batch URL $batch_counter)"
    sleep 5
    
    # After opening 10 URLs, wait and then close tabs
    if [ $batch_counter -eq 10 ]; then
        echo "Batch of 10 URLs completed. Waiting 20 seconds before closing tabs..."
        sleep 20
        close_tabs
        batch_counter=0
        echo "Tabs closed. Continuing to next batch..."
    fi
done < "$file_path"

# Handle any remaining open tabs
if [ $batch_counter -ne 0 ]; then
    echo "Final batch of $batch_counter URLs completed. Waiting 20 seconds before closing tabs..."
    sleep 20
    close_tabs
fi

echo "Finished opening $counter URLs"
