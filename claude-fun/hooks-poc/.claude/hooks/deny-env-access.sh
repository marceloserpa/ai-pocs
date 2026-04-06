#!/bin/bash
input=$(cat)
file_path=$(echo "${input}" | jq -r '.tool_input.file_path // empty')
if [[ "${file_path}" =~ \.env$ ]]; then
  echo "Access to .env files is blocked by hook policy." >&2
  exit 2
fi