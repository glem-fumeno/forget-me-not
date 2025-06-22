#!/usr/bin/env bash

uv sync
exit_code=1
while [[ $exit_code -ne 0 ]]; do
    sleep 1
    uv run main.py
    exit_code=$?
done

