@echo off
CALL venv/scripts/activate
pyinstaller -F -i ./aname.ico ./aname.py
