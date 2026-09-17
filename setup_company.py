"""Create blank private setup worksheets. No network, secrets or app configuration."""

import argparse
import os
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent
WORKSHEETS = (
    "company-profile.md",
    "process-map.md",
    "discovery-notes.md",
    "setup-progress.md",
    "connection-plan.md",
    "pilot-acceptance.md",
)


def initialize(directory, repository=REPOSITORY):
    """Return created/preserved names; never overwrite an existing worksheet."""
    repository = Path(repository).resolve()
    requested = Path(directory).expanduser()
    if requested.is_symlink():
        raise ValueError("Choose a real private directory, not a symbolic link.")
    destination = requested.resolve()
    private_root = repository / ".company"
    if destination == repository or repository in destination.parents:
        if destination != private_root and private_root not in destination.parents:
            raise ValueError("Inside this checkout, setup records must stay under .company/.")
    # Read every source before writing so a missing template creates no partial set.
    contents = {
        name: (repository / "templates" / name).read_text(encoding="utf-8")
        for name in WORKSHEETS
    }
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    created, preserved = [], []
    for name, content in contents.items():
        try:
            descriptor = os.open(destination / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            preserved.append(name)
            continue
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as worksheet:
            worksheet.write(content)
        created.append(name)
    return destination, created, preserved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=REPOSITORY / ".company",
        help="Approved private folder; default: this checkout's ignored .company/.",
    )
    args = parser.parse_args()
    try:
        destination, created, preserved = initialize(args.directory)
    except (OSError, ValueError) as error:
        parser.exit(1, "Setup worksheets could not be initialized: " + str(error) + "\n")
    print("Setup worksheets: " + str(destination))
    print("Created: " + (", ".join(created) or "none"))
    print("Preserved existing files: " + (", ".join(preserved) or "none"))
    print("Blank planning files only. No APIs connected, cloud deployed or readiness verified.")
    print("Use approved private storage. Git exclusion is not access control; store no secrets here.")
    print("Next: ask your assistant to read SETUP.md and start or resume the discovery interview.")


if __name__ == "__main__":
    main()
