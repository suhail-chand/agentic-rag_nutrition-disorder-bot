import os
from dotenv import load_dotenv
from huggingface_hub import HfApi


load_dotenv()


if __name__ == "__main__":
    print("Deploying to Hugging Face Space...")
    api =  HfApi(
        token=os.environ["HF_TOKEN"]
    )

    # HF space repo id
    HF_repo_id = os.environ["HF_REPO_ID"]

    print("  Uploading requirements.txt...", end="")
    api.upload_file(
        path_or_fileobj="requirements.txt",
        path_in_repo="requirements.txt",
        repo_id=HF_repo_id,
        repo_type="space",
    )
    print("  Done.")

    print("  Uploading source code...", end="")
    api.upload_folder(
        folder_path="src",
        path_in_repo="src",
        repo_id=HF_repo_id,
        repo_type="space",
        ignore_patterns="__pycache__"
    )
    print("  Done.")

    print("  Uploading data...", end="")
    api.upload_folder(
        folder_path="data/store/nutritional_db",
        path_in_repo="data/store/nutritional_db",
        repo_id=HF_repo_id,
        repo_type="space",
    )
    print("  Done.")

    print("  Uploading Dockerfile...", end="")
    api.upload_file(
        path_or_fileobj="Dockerfile",
        path_in_repo="Dockerfile",
        repo_id= HF_repo_id,
        repo_type="space"
    )
    print("  Done.")

    print("  Uploading README.md...", end="")
    api.upload_file(
        path_or_fileobj="README.md",
        path_in_repo="README.md",
        repo_id= HF_repo_id,
        repo_type="space"
    )
    print("  Done.")

    print("Deployment complete!")
