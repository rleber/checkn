#!/usr/bin/env python3

# Set up template

# TODO Rename this library as setup-pip
# TODO Fix library so it handles module names including "-"
# TODO Integrate with ruby gem setup
# TODO Create a gem exists shortcut like pip exists

import argparse
from git import Repo
import logging
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile


PROJECT_ROOT = "~/projects/python"
TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "template"


def main(args = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="psetup",
        description="Set up a Python module"
    )
    parser.add_argument(
        "module", help="Module name"
    )
    parsed_args = parser.parse_args(args)

    module = parsed_args.module
    root = Path(PROJECT_ROOT).expanduser().resolve()
    project_dir = root / module


    with tempfile.TemporaryDirectory() as temp_dirname:
        temp_dir = Path(temp_dirname)
        if project_dir.exists():
            start_logging(project_dir)
            check_project_directory(project_dir)
            existing_files = save_existing_files(project_dir, temp_dir=temp_dir)
            ensure_git(project_dir)
        else:
            existing_files = None
            # TODO allow a glob parameter specifying which files to move in?
            initialize_project_dir(project_dir)

        build_project_dir(project_dir, module=module, existing_files=existing_files)
        edit_files(project_dir, module=module)
        make_file_executable(project_dir / "src" / module / (module + ".py"))



        # TODO Check in other files in git
        # TODO Create a develop branch    

        print_user_prompt(project_dir, module=module)


def start_logging(project_dir: Path):
    logging.basicConfig(filename=str(project_dir / "setup.log"), level=logging.INFO)
    

def check_project_directory(project_dir: Path):
    if not project_dir.is_dir():
        print(f"Cannot use {project_dir}: It exists, but is not a directory")
        exit(1)


EXCLUDED_SAVE_FILES = [".git", "__pycache__"]


def save_existing_files(project_dir: Path, temp_dir: Path) -> Path:
    for file in project_dir.iterdir():
        if file.name not in EXCLUDED_SAVE_FILES:
            move_file(file, temp_dir / file.name)
    return temp_dir


def ensure_git(project_dir: Path) -> None:
    if not (project_dir / ".git").exists():
        init_git(project_dir)


def init_git(project_dir: Path) -> Repo:
    try:
        repo = Repo.init(str(project_dir))
        logging.info(f"Initialize git in {project_dir}")
    except Exception as e:
        print(f"An error occurred while trying to initialize Git in {project_dir}: {e}")
        exit(1)
    return repo


def initialize_project_dir(project_dir: Path) -> None:
    project_dir.mkdir(parents=True)
    start_logging(project_dir)
    logging.info(f"Create {project_dir}")
    init_git(project_dir)

GITIGNORE_SOURCE = Path("~/projects/other/gitignore/Python.gitignore").expanduser().resolve()

EXCLUDED_COPY_FILES = [
    Path(__file__).name,
    "tests",
    "src",
    "module.py",
    ".git",
    ".gitignore",
]

def build_project_dir(project_dir: Path, module: str, existing_files: Path | None) -> None:
    src_dir = project_dir / "src" / module
    src_dir.mkdir(parents=True)
    logging.info(f"Create {src_dir}")
    tests_dir = project_dir / "tests"
    tests_dir.mkdir()
    logging.info(f"Create {tests_dir}")
    data_dir = project_dir / "data"
    data_dir.mkdir()
    logging.info(f"Create {data_dir}")

    copy_file(
        TEMPLATE_DIR / "src" / "module" / "__init__.py",
        project_dir / "src" / module / "__init__.py"
    )
    copy_file(
        TEMPLATE_DIR / "src" / "module" / "module.py",
        project_dir / "src" / module / (module + ".py")
    )

    if existing_files is not None:
        for file in existing_files.iterdir():
            if file.suffix in [".sh", ".c", ".cpp", ".py", ".rb", ""]:
                dest_dir = src_dir
            elif file.name.startswith("test"):
                dest_dir = tests_dir
            else:
                dest_dir = data_dir
            dest = dest_dir / file.name
            move_file(file, dest)

    for file in TEMPLATE_DIR.iterdir():
        if file.name not in EXCLUDED_COPY_FILES:
            dest = project_dir / file.name
            copy_file(file, dest)

    copy_file(GITIGNORE_SOURCE, project_dir / ".gitignore")

    direnv_enable(project_dir)

EDIT_FILES = [
    "pyproject.toml", 
    "README.md", 
    ".envrc",
]


def edit_files(project_dir: Path, module: str):
    files_to_edit = EDIT_FILES.copy()
    files_to_edit.append(f"src/{module}/__init__.py")
    files_to_edit.append(f"src/{module}/{module}.py")
    for file in files_to_edit:
        target_file = project_dir / file
        edit_file(target_file, r"\bmodule\b", module)


def move_file(src: Path, dest: Path):
    shutil.move(src, dest)
    logging.info(f"Move {src} to {dest}")


def copy_file(src: Path, dest: Path):
    if src.is_dir():
        shutil.copytree(src, dest)
        logging.info(f"Copy {src} directory to {dest}")
    else:
        shutil.copy(src, dest)
        logging.info(f"Copy {src} to {dest}")


def direnv_enable(project_dir: Path) -> None:
    res = subprocess.run(["direnv", "allow"], 
        cwd = str(project_dir),
        capture_output=True,
        text = True,
        )
    if res.returncode != 0:
        print("Error encountered in direnv allow")
        exit(1)


def edit_file(file: Path, find_regex: str, replace: str):
    compiled_regex = re.compile(find_regex)
    with file.open("r") as f:
        text = f.read()
    revised_text = compiled_regex.sub(replace, text)
    with file.open("w") as f:
        f.write(revised_text)
    logging.info(f"Edited {file}")


def make_file_executable(file: Path) -> None:
    current_mode = os.stat(str(file)).st_mode
    # Add execute permissions for Owner, Group, and Others (equivalent to +x)
    new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(str(file), new_mode)
    logging.info(f"Made {file} executable")




def print_user_prompt(project_dir: Path, module: str) -> None:
    print(f"Completed creation of project {module}")
    print(f"  Created in {project_dir}")
    print(f"  Check log in {project_dir / 'setup.log' }")
    print(f"  Check contents of all files, especially:")
    print(f"    - pyproject.toml")
    print(f"    - README.md")    
    print(f"  .envrc has been added and direnv is enabled")    
    print(f"  Git repo has been intialized. You should:")
    print(f"    - Check in changes")
    print(f"    - Create an upstream repository")
    print(f"    - Create a 'develop' branch")                                            
    print(f"    - Push changes upstream")    


if __name__ == "__main__":
    main()                                            