"""Defensive ZIP extraction: no symlinks, traversal, or unbounded output."""
import argparse
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile

class UnsafeArchive(ValueError):
    pass

def extract(archive, destination, max_files=1000, max_total=100_000_000, max_file=20_000_000):
    destination = Path(destination).resolve()
    if destination.exists() and not destination.is_dir():
        raise UnsafeArchive("destination must be a directory")
    with zipfile.ZipFile(archive) as zf:
        members = zf.infolist()
        if len(members) > max_files:
            raise UnsafeArchive("too many entries")
        seen = set()
        planned = []
        total = 0
        for member in members:
            name = member.filename
            path = PurePosixPath(name)
            if (not name or "\\" in name or path.is_absolute() or
                any(part in ("..", ".") for part in name.split("/")) or
                any(":" in part for part in path.parts)):
                raise UnsafeArchive(f"unsafe path: {name!r}")
            mode = member.external_attr >> 16
            if stat.S_IFMT(mode) == stat.S_IFLNK:
                raise UnsafeArchive("symlinks are forbidden")
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise UnsafeArchive("special files are forbidden")
            relative = Path(*path.parts)
            target = destination / relative
            if target in seen:
                raise UnsafeArchive("duplicate path")
            seen.add(target)
            if not member.is_dir():
                if member.file_size > max_file:
                    raise UnsafeArchive("file exceeds size budget")
                total += member.file_size
                if total > max_total:
                    raise UnsafeArchive("archive exceeds total size budget")
            planned.append((member, target))
        files = {target for member, target in planned if not member.is_dir()}
        if any(parent in files for _, target in planned for parent in target.parents if parent != target):
            raise UnsafeArchive("file/directory path collision")
        # Do not follow preexisting symlinks inside the destination.
        for _, target in planned:
            for parent in (target, *target.parents):
                if parent == destination.parent:
                    break
                if parent.is_symlink():
                    raise UnsafeArchive("destination contains a symlink")
        destination.mkdir(parents=True, exist_ok=True)
        written = []
        for member, target in planned:
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                raise UnsafeArchive(f"refusing to overwrite {target}")
            with zf.open(member) as src, target.open("xb") as dst:
                copied = 0
                while True:
                    block = src.read(65536)
                    if not block:
                        break
                    copied += len(block)
                    if copied > max_file:
                        raise UnsafeArchive("decompressed data exceeds budget")
                    dst.write(block)
            written.append(str(target.relative_to(destination)))
        return written

def main():
    parser = argparse.ArgumentParser(description="Extract a trusted-size ZIP safely")
    parser.add_argument("archive")
    parser.add_argument("destination")
    args = parser.parse_args()
    for path in extract(args.archive, args.destination):
        print(path)

if __name__ == "__main__":
    main()
