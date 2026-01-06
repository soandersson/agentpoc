#!/bin/bash
# Convenience script to run the agent with the correct Python environment

cd /workspaces/agentpoc
source .venv/bin/activate
python "$@"
