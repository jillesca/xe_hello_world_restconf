# IOS XE hello world using Restconf

Simple hello world in IOS XE using Restconf.

The script prints the status of the hostname and version of IOS XE.

For real use, consider using environment variables rather than hardcoding credentials for your iosxe instance.

For demo purposes, the script connects to the [iosxe always-On sandbox](https://developer.cisco.com/site/sandbox/), so you can test it right away.

Below are the restconf paths used to get the data.

```javascript
/restconf/data/Cisco-IOS-XE-native:native/version
/restconf/data/Cisco-IOS-XE-native:native/hostname
```

### How to use it

Install dependencies

```bash
pip install -r requirements.txt
```

To run the script do:

```bash
python hello_world.py
```

Output printed

```bash
❯ python hello_world.py
Reviewed 10.10.20.175
Hostname found: dist-rtr01
IOS XE Version found: 17.6
❯
```
