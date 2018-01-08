# coding: utf-8

from __future__ import unicode_literals

from autobahn.twisted.wamp import Application

import socket
import uuid

# Just like for flask, the app object
# is what's bind all elements together.
# We give it a name, here "demo".
app = Application("demo")
# While the app is going to start
# a server for us, the app is a CLIENT
# of the WAMP server. The server is
# started automatically as a courtesy
# for dev purpose. In production, we
# would use crossbar.

# Just a container to store the IP
app._data = {}

# We ask for this function to be called when the
# app is connected to the WAMP server. This allow
# us to run caode right after the app.run() call
# you can see at the bottom of the file. '_' is
# a convention in Python meaning "this name has
# no importance, it's disposable code that we'll
# use only once"
@app.signal("onjoined")
def _():
    # We get our IP address on the local network.
    # It's a trick requiring an external IP to
    # be reachable, so you need an internet connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # We store the local IP address in a container
    # that will be accessible anywhere else.
    app._data["LOCAL_IP"] = s.getsockname()[0]
    s.close()

# We declare that the "ip()" function is callable using
# RPC. It means any WAMP client caan get thre result
# of this function. So we will be able to call it
# from our browser. Since our app is named "demo" and
# our funciton is named "ip", a client will be able
# to call it using "demo.ip"
@app.register()
def ip():
    # We just return the store local IP. Nothing crazy.
    return app._data["LOCAL_IP"]

# I wanted to call this distant function "uuid", but that
# would shadow the uuid Python module. This is not a good
# id. Intead, I'll call it "get_uuid", but I'll declare
# manually the full namespace in register(). A WAMP client
# will be able to call it using "demo.uuid".
# Please note the namespace should be written foo.bar.stuff,
# not foo:bar, foo/bar or foo.BAR. Syntax is significant.
@app.register("demo.uuid")
def get_uuid():
    # Return the UUID without dashes.
    # E.G: b27f7e9360c04efabfae5ac21a8f4e3c
    return str(uuid.uuid4()).replace('-', '')

# We run the application. This will start the
# server then the client. You can disable the
# dev server in prod.
if __name__ == "__main__":
    app.run(url="ws://127.0.0.1:8081/")
    # You can't put anything here. You need to
    # put code in @app.signal('onjoined') if you
    # want to run it after the app has started.