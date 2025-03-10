#!/bin/bash

# Recursively find and delete all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} +
echo 'Deleted all __pycache__ directories'
