# UMU-Protonfixes

This project acts as a stopgap for fixing games that don't work out of the box on Proton. It implements game-specific patches, such as installing Winetricks verbs.

It is the heart of `UMU-Proton` and `GE-Proton`.

## Start parameter fixes

The [default fix file for Steam](gamefixes-steam/default.py) implements a feature to install Winetricks / Protontricks verbs via startup parameters. Just add `-pf_tricks=<verb>` to it. You can install multiple verbs by adding the parameter more than once.

```bash
-pf_tricks=xliveless -pf_tricks=d3dcompiler_47
```

You can also set [dxvk options](https://github.com/doitsujin/dxvk/wiki/Configuration).

```bash
-pf_dxvk_set=dxgi.maxFrameRate=40 -pf_dxvk_set=d3d9.maxFrameRate=40 
```

The order is not important and the arguments are not passed on to the game.

## Local fixes

The easiest way to implement a new fix or modify an existing one, is to use local fixes.

### Game fixes

First of all, you should find the Steam-ID of the game (right click the game in your Steam library -> 'Properties...' -> 'Updates' -> 'App ID:') and use it as the filename, with a `.py` extension.

Example `Day of Defeat: Source` (AppID 300):

> ~/.config/protonfixes/localfixes/300.py

Another type of fix is one that runs before each game. This allows you to set defaults for all games.

> ~/.config/protonfixes/localfixes/default.py

Note that local fixes override the included "global" fixes. So using an existing fix might be a good starting point for modifications, as they will not be executed.

For example, overriding the default fix will disable [the parameter parsing for Steam games](#start-parameter-fixes). This can be restored by copying [the global default file](gamefixes-steam/default.py) and applying your changes accordingly.

### Verbs

You can also add local Winetricks verbs, just like the ones implemented [here](verbs).

This also allows you to override existing Protontricks and Winetricks verbs, for example if a URL or file hash has changed.

> ~/.config/protonfixes/localfixes/<verb_name>.verb

To call them, just use the default function:

```python
util.protontricks('<verb_name>')
```

## Non-Steam games

As we support platforms other than Steam, these fixes can also be used by other launchers, such as Lutris, Heroic, Legendary or Bottles.

The current implementation requires entries in a special database that looks up the `UMU-ID`, which consists of the prefix `umu-` and in most cases the SteamID (if the game exists on that platform).

https://github.com/Open-Wine-Components/umu-database

## Config file

There is a config file located at:

> ~/.config/protonfixes/config.ini

It's not widely used at the moment, but you can configure some aspects.

### Defaults

```toml
[main]
enable_checks = true
enable_global_fixes = true

[path]
cache_dir = ~/.cache/protonfixes
```

### Variables

`enable_checks`: De-/activate checks that are run on every startup. Currently only a check if esync might cause problems.

`enable_global_fixes`: De-/activate global fixes, which are the built-in files in the `gamefix-*` folders. Only [local fixes](#local-fixes) will be executed.

`cache_dir`: Used when something needs to be unpacked or similar.

### Values 

Valid "enable" values are: `yes`, `y`, `true`, `1`

Any other value is interpreted as disabled.

## Building binaries

UMU-Protonfixes ships some binaries - used by some fixes - that need to be built.

**You probably do not need to build them to contribute.**

These binaries are not included in this repository, but are built from git-submodules in the [subprojects folder](subprojects/). To get the submodules, run the following command:

```bash
git submodule update --init --recursive
```

To actually build the binaries, simply run:

```bash
make
```

## Contributing

We do enforce some linting and testing that can and should be done locally - before you open a pull request.

### Linting

To install the necessary tools, just run:

```bash
python -m pip install --upgrade pip
pip install ruff
```

On Arch / Manjaro, you should run this instead:

```bash
sudo pacman -Sy ruff
```

To run a check, just execute:

```bash
ruff check .
```

You are good to go when you see the message `All checks passed!`.

If not, try letting `ruff` (the linter we use) fix it automatically:

```bash
ruff format .
```

### Testing

The filenames of the fixes are checked against the Steam and GOG APIs. All symbolic links are also checked. This is not mandatory to run locally, as you should have a working game fix to begin with, and it will be done automatically by Github's CI.

You can still run it though:

```bash
cd .github/scripts
python check_gamefixes.py
```

You need the following prerequisites:

```bash
python -m pip install --upgrade pip
pip install ijson
```

On Arch / Manjaro:

```bash
sudo pacman -Sy python-ijson
```
