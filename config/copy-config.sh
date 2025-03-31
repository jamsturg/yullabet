#!/bin/bash

# Shell script to copy the chat configuration to the .mcpchat/chats directory

# Get the current timestamp in milliseconds since epoch
timestamp=$(date +%s)000

# Get the highest chat ID from existing files
chats_dir="$HOME/.mcpchat/chats"
highest_id=0

for chat_file in "$chats_dir"/chat-*.json; do
    if [ -f "$chat_file" ]; then
        # Extract the ID from the filename (chat-ID-timestamp.json)
        filename=$(basename "$chat_file")
        id=$(echo "$filename" | sed -E 's/chat-([0-9]+)-.*/\1/')
        
        # Update highest_id if this id is greater
        if [ "$id" -gt "$highest_id" ]; then
            highest_id=$id
        fi
    fi
done

# Use the next available ID
new_id=$((highest_id + 1))

# Create the new filename
new_filename="chat-$new_id-$timestamp.json"
target_path="$chats_dir/$new_filename"

# Copy the configuration file
source_path="$(dirname "$0")/chat-config.json"
cp "$source_path" "$target_path"

echo "Configuration copied to $target_path"
echo "Chat ID: $new_id"
echo "You can now use mcp-chat to select this configuration"