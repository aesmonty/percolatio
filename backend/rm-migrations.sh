#!/usr/bin/env bash

# This script hard resets the migrations of the app. Use carefully.
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.env/*" -delete
find . -path "*/migrations/*.pyc" -not -path "./.env/*" -delete
rm db.sqlite3