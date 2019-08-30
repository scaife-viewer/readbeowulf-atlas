#!/bin/bash

isort -rc readbeowulf_atlas
black readbeowulf_atlas
flake8 readbeowulf_atlas
