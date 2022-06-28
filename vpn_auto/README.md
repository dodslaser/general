# VPN Auto-connect

The following instructions will allow automatic login to a Cisco AnyConnect VPN on macOS using the built-in keyring. While this is probly not less secure than eg. copy pasting from a password manager it should be noted that the official client purposely doesn't allow this and thus you will end up on Santa's naughty list for doing this.

Copy `vpn-auto.sh` to something like `~/scripts/vpn-auto.sh`. Ensure it is executable (`chmod +x`).

Add a generic password for a VPN user to the keychain. The default service used is "VPN". Replace `${USER}` if your VPN username is not the same as your local user.

```shell
security add-generic-password -s "VPN" -a "${USER}" -w "$(read -s -p "Password: " i; echo $i)"
```

Change/add the environment variables in `com.vpn-auto.startup.plist` and script path if necessary. At the very least `VPN_HOST` must be specified (Replace `example_vpn_host` in `com.vpn-auto.startup.plist`).

The following environemnt variables are used:

  - `VPN_HOST` VPN server to connect to **(Required)**
  - `VPN_USERNAME` Username for the VPN connection. (Default: your local username)
  - `VPN_KEYCHAIN_SERVICE` Keychain service where the VPN password is stored. Must match the service you specified when storing the password in the keychain (Default: `VPN`)

Copy `com.vpn-auto.startup.plist` to `~/Library/LaunchAgents/` and enable the LaunchAgent.

```shell
launchctl load -w ~/Library/LaunchAgents/com.vpn-auto.startup.plist
```

The path must not be quoted (or `launchctl` will gine an input/output error).

## Todo
  - Adapt for Linux (Windows?)