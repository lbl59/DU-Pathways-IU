#!/bin/bash

# Enable debugging if needed
# set -x

# Set epsilon values, data, runtime, and output directories
#epsilon="0.025,0.02,10.0,0.05,0.05"
epsilon="0.01,0.1,10.0,0.1,0.1"
setDir="./nondominated_base"
runtimeDir="$setDir"
metricDir="$setDir"
refFile="$setDir/refset_base_nondominated_truncated_test.ref"

# Set the path to the CLI executable
MOEAFramework5Path="MOEAFramework-5.0"
cliPath="$MOEAFramework5Path/cli"

# Set MOEAFramework download info
MOEAFrameworkURL="https://github.com/MOEAFramework/MOEAFramework/releases/download/v5.0/MOEAFramework-5.0.tar.gz"
MOEAFrameworkTar="MOEAFramework-5.0.tar.gz"

# Check if MOEAFramework directory exists
if [ ! -d "$MOEAFramework5Path" ]; then
    echo "MOEAFramework-5.0 not found. Downloading..."

    # Download using curl or wget
    curl -L -o "$MOEAFrameworkTar" "$MOEAFrameworkURL"

    # Extract using tar
    tar -xzf "$MOEAFrameworkTar" -C ../../

    # Clean up
    rm "$MOEAFrameworkTar"
fi

# Check the permission is given
if [ ! -x "$cliPath" ]; then
    echo "Error: CLI at $cliPath is not executable. Run:"
    echo "chmod +x $cliPath"
    exit 1
fi

# Create metrics directory if it doesn't exist
mkdir -p "$metricDir"

# Step 1: Merge all .set files in the data directory
fileList=()
for f in "$setDir"/*.set; do
    fileList+=("$f")
done

echo "Running ResultFileMerger"
"$cliPath" ResultFileMerger --problem SedentoValleySimulation --epsilon "$epsilon" --output "$refFile" "${fileList[@]}" 