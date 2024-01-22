from cx_Freeze import setup, Executable

setup(
    name="My Project",
    version="0.1",
    description="My Project Description",
    executables=[Executable("src/main.py")]
)
