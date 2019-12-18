# Gitlab Client for Intellij

## Build and install

1. Fire `./build.sh`. It will pack application into executable `gitlab-client.pyz`.
1. Configure client in `~/.gitlab-client.json` (example format in `example.gitlab-client.json`)
1. (optional) Add helper script (below)  

### Helper script

It's possible to add helper script to your shell. Simply add following to your `.bashrc` / `.zshrc`:

```bash
. /path/to/gitlab-client/helper.sh
```

Usage: `project {gitlab instance, eg. unity} {optional search}`

eg: `project unity tools`