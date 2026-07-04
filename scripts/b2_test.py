from app.core.storage_b2 import B2Storage


def main():
    storage = B2Storage()

    object_key = "dev/smoke-test/hello.txt"
    original_data = b"hello from ChunkVault"

    print("Uploading object...")
    storage.upload_bytes(object_key, original_data)

    print("Checking object exists...")
    assert storage.object_exists(object_key) is True

    print("Downloading object...")
    downloaded_data = storage.download_bytes(object_key)

    assert downloaded_data == original_data

    print("Deleting object...")
    storage.delete_object(object_key)

    print("Checking object was deleted...")
    assert storage.object_exists(object_key) is False

    print("B2 smoke test passed.")


if __name__ == "__main__":
    main()