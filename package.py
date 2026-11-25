"""Apply minimal ad hoc entitlements and package a built SimpleX.app."""

import pathlib
import plistlib
import shutil
import subprocess
import sys


TEAM = "5NN7GUYB6T"  # Team in the upstream Xcode project.
APP_ID = "chat.simplex.app"
APP_GROUP = "group.chat.simplex.app"


def bundle_id(path: pathlib.Path) -> str:
    return plistlib.loads((path / "Info.plist").read_bytes())["CFBundleIdentifier"]


def sign(path: pathlib.Path, entitlements: pathlib.Path | None = None) -> None:
    command = ["codesign", "--force", "--sign", "-"]
    if entitlements:
        command += ["--entitlements", str(entitlements)]
    command.append(str(path))
    subprocess.run(command, check=True)
    subprocess.run(["codesign", "--verify", "--strict", str(path)], check=True)


def write_entitlements(path: pathlib.Path, output: pathlib.Path) -> pathlib.Path:
    identifier = bundle_id(path)
    assert identifier == APP_ID or identifier.startswith(APP_ID + "."), identifier
    entitlements = {
        "application-identifier": f"{TEAM}.{identifier}",
        "com.apple.developer.team-identifier": TEAM,
        "com.apple.security.application-groups": [APP_GROUP],
        "keychain-access-groups": [f"{TEAM}.{APP_ID}"],
    }
    target = output / f"{path.name}.entitlements"
    target.write_bytes(plistlib.dumps(entitlements))
    return target


def main() -> None:
    app = pathlib.Path(sys.argv[1]).resolve()
    output = pathlib.Path(sys.argv[2]).resolve()
    assert app.is_dir() and app.name == "SimpleX.app", app
    assert bundle_id(app) == APP_ID
    output.mkdir(parents=True, exist_ok=True)
    signing_dir = output / "signing"
    signing_dir.mkdir(exist_ok=True)

    for framework in sorted(app.rglob("*.framework"), key=lambda p: len(p.parts), reverse=True):
        sign(framework)
    for dylib in sorted(app.rglob("*.dylib")):
        sign(dylib)
    for extension in sorted((app / "PlugIns").glob("*.appex")):
        sign(extension, write_entitlements(extension, signing_dir))
    sign(app, write_entitlements(app, signing_dir))

    payload = output / "Payload"
    payload.mkdir(exist_ok=True)
    shutil.copytree(app, payload / app.name, symlinks=True)
    ipa = output / "SimpleX-v7.1.4.ipa"
    subprocess.run(["zip", "-qry", str(ipa), "Payload"], cwd=output, check=True)
    print(f"IPA: {ipa}")
    print(f"Bundle: {bundle_id(app)}")
    print(f"Version: {plistlib.loads((app / 'Info.plist').read_bytes())['CFBundleShortVersionString']}")


if __name__ == "__main__":
    main()
