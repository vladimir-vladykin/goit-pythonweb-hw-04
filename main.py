import sys
import asyncio
from aiofile import async_open
from aiopath import AsyncPath


async def main(source_dir_path: str, output_dir_path: str):
    apath = AsyncPath(source_dir_path)
    is_source_exists = await apath.exists()
    if is_source_exists == False:
        print(f"Source directory ${source_dir_path} does not exist")
        return

    dir_data = {}
    await build_dir_data(apath, dir_data)

    print(dir_data)


async def build_dir_data(path: AsyncPath, dict: dict):
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

            # fixme actually should be path, to use for copy later
            files_with_this_suffix.append(file.name)


class ArgumentParser:
    def parse_dir_paths(self, argv):
        # first arg after script name is source dir, and second one is output dir
        if len(argv) > 2:
            source_dir_path = argv[1]
            output_dir_path = argv[2]
            return source_dir_path, output_dir_path
        else:
            raise Exception()


if __name__ == "__main__":
    try:
        source_dir_path, output_dir_path = ArgumentParser().parse_dir_paths(sys.argv)
    except:
        print(
            "Invalid parameters. Make sure to put path to source directory as first parameter of this script, and path to target directory as the second one"
        )

    asyncio.run(main(source_dir_path, output_dir_path))
