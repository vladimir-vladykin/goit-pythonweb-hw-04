import sys
import asyncio
from typing import Dict
from aiofile import async_open
from aiopath import AsyncPath
from aioshutil import copyfile


async def main(source_dir_path: str, output_dir_path: str):
    apath = AsyncPath(source_dir_path)
    is_source_exists = await apath.exists()
    if is_source_exists == False:
        print(f"Source directory ${source_dir_path} does not exist")
        return

    dir_data: Dict[str, AsyncPath] = {}
    await build_dir_data(apath, dir_data)

    copy_files_manager = CopyFilesManager()
    await copy_files_manager.copy_files(dir_data, output_dir_path)


async def build_dir_data(path: AsyncPath, dict: Dict[str, AsyncPath]):
    async for file in path.iterdir():
        if await file.is_dir():
            await build_dir_data(file, dict)
        else:
            file_suffix = file.suffix
            if file_suffix == "":
                file_suffix = "other"

            files_with_this_suffix = dict.get(file_suffix)

            if files_with_this_suffix == None:
                files_with_this_suffix = []
                dict[file_suffix] = files_with_this_suffix

            files_with_this_suffix.append(file)


class ArgumentParser:
    def parse_dir_paths(self, argv):
        # first arg after script name is source dir, and second one is output dir
        if len(argv) > 2:
            source_dir_path = argv[1]
            output_dir_path = argv[2]
            return source_dir_path, output_dir_path
        else:
            raise Exception()


class CopyFilesManager:
    async def copy_files(self, files_data: Dict[str, AsyncPath], output_dir_path: str):
        print(f"Moving files into directory /{output_dir_path}...")
        async_output_path = AsyncPath(output_dir_path)
        if await async_output_path.exists() == False:
            await async_output_path.mkdir()

        for ext in files_data:
            async_ext_path = AsyncPath(output_dir_path + "/" + ext)
            print(f"Moving files into sub-directory {async_ext_path}")
            if await async_ext_path.exists() == False:
                await async_ext_path.mkdir()

            file_paths = files_data[ext]
            for file in file_paths:
                await copyfile(file, async_ext_path / file.name)


if __name__ == "__main__":
    try:
        source_dir_path, output_dir_path = ArgumentParser().parse_dir_paths(sys.argv)
    except:
        print(
            "Invalid parameters. Make sure to put path to source directory as first parameter of this script, and path to target directory as the second one"
        )

    asyncio.run(main(source_dir_path, output_dir_path))
