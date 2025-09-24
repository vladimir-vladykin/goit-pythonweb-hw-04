import sys
import asyncio
from aiofile import async_open
from aiopath import AsyncPath


async def main(source_dir_path: str, output_dir_path: str):
    apath = AsyncPath(source_dir_path)
    print(f"Checking is ${source_dir_path} exists...")
    print(await apath.exists())


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
        asyncio.run(main(source_dir_path, output_dir_path))
    except:
        print(
            "Invalid parameters. Make sure to put path to source directory as first parameter of this script, and path to target directory as the second one"
        )
