import os
import tempfile
import shutil
from distutils.core import setup
from Cython.Build.Dependencies import cythonize
from multiprocessing import pool


def run_distutils(args):
    base_dir, ext_modules = args
    script_args = ['build_ext', '-i']
    cwd = os.getcwd()
    temp_dir = None
    try:
        if base_dir:
            os.chdir(base_dir)
            temp_dir = tempfile.mkdtemp(dir=base_dir)
            script_args.extend(['--build-temp', temp_dir])
            setup(
                script_name='setup.py',
                script_args=script_args,
                ext_modules=ext_modules,
            )
    finally:
        if base_dir:
            os.chdir(cwd)
            if temp_dir and os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)


def run_files(ext_paths):
    cython_exts = cythonize(ext_paths,
                            nthreads=1,
                            compiler_directives={
                                "always_allow_keywords": False,
                            })
    try:
        process_pool = pool.Pool()
        process_pool.map_async(run_distutils, [(".", [ext]) for ext in cython_exts])
    except:
        if process_pool is not None:
            process_pool.terminate()
        raise
    finally:
        if process_pool is not None:
            process_pool.close()
            process_pool.join()

if __name__ == "__main__":
    for dir_path, dir_names, file_names in os.walk("."): 
        if dir_path == ".": 
            continue 
        for file_name in file_names: 
            name, extension = os.path.splitext(file_name) 
            if extension == '.py' and name != '__init__':
                file_path = os.path.join(dir_path, file_name) 
                ext_paths = [file_path]
                run_files(ext_paths)
                os.remove(file_path)