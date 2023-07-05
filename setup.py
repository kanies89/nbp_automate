from cx_Freeze import setup, Executable

# List of additional files to include
additional_files = ['connect.py', 'f_mastercard.py', 'f_visa.py', 'test_main.py', 'variables.py']

# Create a list of executables
executables = [Executable("main.py")]

setup(
    name="NBP_Report",
    version="1.0",
    description="NBP Report Automation",
    executables=executables,
    options={
        'build_exe': {
            'include_files': additional_files
        }
    }
)
