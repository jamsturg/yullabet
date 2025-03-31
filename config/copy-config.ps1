# PowerShell script to copy the chat configuration to the .mcpchat/chats directory

# Get the current timestamp in milliseconds since epoch
$timestamp = [Math]::Floor([decimal](Get-Date(Get-Date).ToUniversalTime()-UFormat "%s")) * 1000

# Get the highest chat ID from existing files
$chatsDir = Join-Path $env:USERPROFILE ".mcpchat\chats"
$existingChats = Get-ChildItem -Path $chatsDir -Filter "chat-*.json"
$highestId = 0

foreach ($chat in $existingChats) {
    $match = $chat.Name -match "chat-(\d+)-"
    if ($match) {
        $id = [int]$Matches[1]
        if ($id -gt $highestId) {
            $highestId = $id
        }
    }
}

# Use the next available ID
$newId = $highestId + 1

# Create the new filename
$newFilename = "chat-$newId-$timestamp.json"
$targetPath = Join-Path $chatsDir $newFilename

# Copy the configuration file
$sourcePath = Join-Path $PSScriptRoot "chat-config.json"
Copy-Item -Path $sourcePath -Destination $targetPath

Write-Host "Configuration copied to $targetPath"
Write-Host "Chat ID: $newId"
Write-Host "You can now use mcp-chat to select this configuration"