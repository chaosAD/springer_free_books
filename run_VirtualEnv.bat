::-- Setup the virtual environment
call setup_env.bat

::-- Run main program at virtual environment
python main.py

::-- Deactivate virtual environment
call .venv\Scripts\deactivate.bat

pause
