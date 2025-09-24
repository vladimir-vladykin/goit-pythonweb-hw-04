import sys


def main(source_dir_path: str, output_dir_path: str):
    print(source_dir_path, output_dir_path)


if __name__ == "__main__":
    # first arg after script name is source dir, and second one is output dir
    if len(sys.argv) > 2:
        source_dir_path = sys.argv[1]
        output_dir_path = sys.argv[2]
        main(source_dir_path, output_dir_path)
    else:
        print(
            "Invalid parameters. Make sure to put path to source directory as first parameter of this script, and path to target directory as the second one"
        )
