import hashlib
import os
import PIL.Image


allowed_extensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"]


def downsample(
    image: PIL.Image.Image,
) -> PIL.Image.Image:
    k = 8
    return image.resize((image.width // k, image.height // k), PIL.Image.LANCZOS)


def upsample(
    image: PIL.Image.Image,
) -> PIL.Image.Image:
    k = 7
    return image.resize((image.width * k, image.height * k), PIL.Image.NEAREST)


def downsample_dir(
    source_dir: str,
    output_dir: str,
    skip_existing: bool,
) -> None:
    """
    Downsamples all images in a directory by a factor of 8
    :param source_dir: The directory containing the images to downsample
    :param output_dir: The directory to output the downsampled images
    """
    assert os.path.exists(source_dir), f"{source_dir} does not exist"
    assert os.path.exists(output_dir), f"{output_dir} does not exist"
    for filename in os.listdir(source_dir):
        try:
            hashed_filename = hashlib.md5(filename.encode()).hexdigest()
            hashed_filename = hashed_filename[:8]
            input_path = f"{source_dir}/{filename}"
            output_path = f"{output_dir}/{hashed_filename}.png"
            if skip_existing and os.path.exists(output_path):
                print(f"Skipping {filename} as it has already been downsampled")
                continue
            image = PIL.Image.open(input_path)
            image = image.convert("RGB")
            image = downsample(image)
            image = upsample(image)
            image.save(output_path)
        except Exception as e:
            print(f"Failed to downsample {filename}: {e}")
            continue


def main() -> None:
    source_dir = os.environ.get("NIGHTGARDENAI_SOURCE_DIR")
    assert source_dir is not None, "NIGHTGARDENAI_SOURCE_DIR must be set"
    output_dir = "images"
    downsample_dir(
        source_dir,
        output_dir,
        skip_existing=False,
    )


if __name__ == "__main__":
    main()
