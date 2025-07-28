#!/bin/bash
echo "Running pre-commit check..."
pre-commit run --all-files || exit 1
