#!/usr/bin/env python3
"""Upload a local folder to a Hugging Face dataset repo using HF_TOKEN.

Usage:
  HF_TOKEN=... python scripts/upload_to_hf.py --folder ./checkpoints --repo doughnut23/emollama
"""
import os
import argparse
from huggingface_hub import login, upload_folder


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--folder', '-f', required=True, help='Local folder to upload')
    p.add_argument('--repo', '-r', required=True, help='Hugging Face repo id (e.g. user/repo)')
    p.add_argument('--repo-type', default='dataset', choices=['dataset', 'dataset', 'space', 'model'], help='Repo type')
    p.add_argument('--ignore', nargs='*', default=['*.pyc', '__pycache__'], help='Ignore patterns')
    p.add_argument('--token', help='HF token (optional, can use HF_TOKEN env var)')
    args = p.parse_args()

    token = args.token or os.environ.get('HF_TOKEN')
    if not token:
        print('ERROR: HF_TOKEN not set. Export HF_TOKEN or pass --token')
        raise SystemExit(1)

    folder = os.path.abspath(args.folder)
    if not os.path.exists(folder):
        print(f'ERROR: folder not found: {folder}')
        raise SystemExit(1)

    print('Logging in to Hugging Face...')
    login(token=token)

    print(f'Uploading {folder} to {args.repo} (type={args.repo_type}) ...')
    try:
        upload_folder(
            folder_path=folder,
            repo_id=args.repo,
            repo_type=args.repo_type,
            ignore_patterns=args.ignore,
        )
        print('Upload finished')
    except Exception as e:
        print('Upload failed:', e)
        raise


if __name__ == '__main__':
    main()
