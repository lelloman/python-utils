from PIL import Image
from os.path import exists, isdir, join as join_path, split
from os import mkdir

suffixes = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
factors = [1.0, 1.5, 2.0, 3.0, 4.0]


def get_source_image(path):
    if not exists(path):
        print("Source path <{}> does not exist".format(path))
        exit(1)

    if isdir(path):
        print("Source path <{}> is a directory...!".format(path))
        exit(1)

    image = Image.open(open(path, "rb"))
    print("Source image opened, size is {}x{}".format(image.width, image.height))
    return image


def make_dir(path):
    if exists(path) and isdir(path):
        return True

    try:
        mkdir(path)
        return True
    except Exception as e:
        print(e)
        return False


def ensure_destination_dir(path):
    if exists(path) and not isdir(path):
        print("destination path <{}> exists but is not a directory...!".format(path))
        exit(1)

    if not exists(path):
        if not make_dir(path):
            print("Could not create destination dir <{}>".format(path))
            exit(1)


def make_size(image_size, factor):
    k = factor / 4.0
    return int(image_size[0] * k), int(image_size[1] * k)


def resize_image(source_image_path, destination_dir_path):
    image = get_source_image(source_image_path)
    image_file_name = split(source_image_path)[-1]
    ensure_destination_dir(destination_dir_path)

    image_size = image.width, image.height
    target_sizes = [make_size(image_size, factor) for factor in factors]

    for i, size in enumerate(target_sizes):
        suffix = suffixes[i]
        if suffix == suffixes[-1]:
            resized_image = image
        else:
            resized_image = image.resize(size, Image.LANCZOS)

        dst_path = join_path(destination_dir_path, "drawable-" + suffix)
        make_dir(dst_path)
        resized_image.save(join_path(dst_path, image_file_name))
        print("target size for {}: {}x{}".format(suffixes[i], size[0], size[1]))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resize xxxhdpi image to all android sizes")
    parser.add_argument("-s", "--source", required=True, help="Path to the xxxhdpi source image")
    parser.add_argument("-d", "--destination", required=True,
                        help="Path to the directory where all drawable-{suffix} directories will be generated")
    args = parser.parse_args()
    source_file = args.source
    destination_dir = args.destination

    resize_image(source_file, destination_dir)
