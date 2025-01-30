# mitmproxy-logger
A simple mitmproxy logger that will log all request to the filesystem.

# Run

```bash
mitmproxy -s mitmproxy-logger.py
```

# Configure proxy

I use [Proxy SwitchyOmega](https://addons.mozilla.org/en-US/firefox/addon/switchyomega/) for Firefox.

You just have to create a new HTTP profile and set the proxy to `localhost:8080`.
