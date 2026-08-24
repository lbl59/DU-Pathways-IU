#!/bin/bash
sleep 1

# Loop over every file in the metrics/ directory.
for file in refsets/*; do
  # Check if it's a regular file.
  if [[ -f "$file" ]]; then
    # Process the file and write output to a temporary file.
    tmpfile=$(mktemp)
    awk '{
      if ($NF == 0) {
        for (i = 1; i < NF; i++) {
          printf("%s%s", $i, (i == NF - 1 ? "\n" : OFS))
        }
      } else {
        print
      }
    }' "$file" > "$tmpfile"
    # Replace the original file with the modified file.
    mv "$tmpfile" "$file"
    echo "Processed: $file"
  fi
done