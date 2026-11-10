"""Shared publication inventory and path policy for validation and packaging."""
from pathlib import Path
import subprocess


# These paths are local or generated state, never release inputs. Keep tracked
# entries visible so both the gate and packager can reject them explicitly.
RESERVED_PARTS = frozenset({".git", ".scratch", ".venv", "__pycache__", "dist"})
SCAN_IGNORED_PARTS = RESERVED_PARTS


class PublicationInventory:
    def __init__(self, is_git, release_files, scan_files):
        self.is_git = is_git
        self.release_files = tuple(release_files)
        self.scan_files = tuple(scan_files)


def _git(root, *args):
    try:
        return subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=False)
    except OSError as exc:
        raise RuntimeError("Cannot run Git: " + str(exc))


def is_git_checkout(root):
    """Detect this directory's own checkout, never a containing repository."""
    root = Path(root).resolve()
    marker = root / ".git"
    try:
        result = _git(root, "rev-parse", "--show-toplevel")
    except RuntimeError:
        if marker.exists():
            raise
        return False
    if result.returncode:
        if marker.exists():
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise RuntimeError("Cannot inspect Git checkout: " + detail)
        return False
    top = Path(result.stdout.decode("utf-8", "replace").strip()).resolve()
    if top == root:
        return True
    if marker.exists():
        raise RuntimeError("Git metadata exists, but Git reports a different checkout root")
    return False


def _paths(result, description):
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError("Cannot read Git " + description + ": " + detail)
    return sorted(name for name in result.stdout.decode("utf-8", "surrogateescape").split("\0") if name)


def tracked_files(root):
    return _paths(_git(root, "ls-files", "-z"), "index")


def untracked_files(root):
    # Include ignored files so secret and binary scans retain their former reach.
    # The caller omits only the known local/generated directory trees.
    names = _paths(_git(root, "ls-files", "--others", "-z"), "untracked file list")
    return [name for name in names if not any(part in SCAN_IGNORED_PARTS for part in Path(name).parts)]


def unpacked_files(root):
    """Files in an extracted kit without its own Git checkout."""
    found = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SCAN_IGNORED_PARTS for part in relative.parts):
            continue
        if path.is_file() or path.is_symlink():
            found.append(relative.as_posix())
    return sorted(found)


def inventory(root):
    """Build release and scan paths once for this validation/package operation."""
    root = Path(root).resolve()
    if is_git_checkout(root):
        release = tracked_files(root)
        untracked = untracked_files(root)
        return PublicationInventory(True, release, sorted(set(release) | set(untracked)))
    unpacked = unpacked_files(root)
    return PublicationInventory(False, unpacked, unpacked)


def is_reserved(name):
    path = Path(name)
    for part in path.parts:
        if part in RESERVED_PARTS:
            return True
        if part == ".env" or (part.startswith(".env.") and part != ".env.example"):
            return True
    return path.suffix.lower() in {".pyc", ".pyo"}


def path_is_symlink(root, name):
    return (Path(root) / name).is_symlink()


def working_tree_changes(root):
    result = _git(root, "status", "--porcelain")
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError("Cannot check Git working tree: " + detail)
    return result.stdout
