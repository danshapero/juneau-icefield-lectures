# Jupyter servers

The JIRP laptops might not have the software you need on them.
This is a constant aggravation and limits what kinds of demonstrations teaching faculty can do.
For example, if you want to use the Python NetCDF4 package to analyze some climate model output and one of the laptops doesn't have that package, you're out of luck -- there's no internet to fetch and install it.
However, if you do have it on your own laptop, there is a solution: you can start up a Jupyter server on your own machine and connect to that server from the JIRP laptops.
The students can then run code from the JIRP laptops which then executes on your computer.
Here's how.
I recommend you test this out with your laptop and a friend's before coming to the icefield.
You do not want to be asking for help via inreach.

## Create an ad hoc wireless network

There is no internet at JIRP, much less wifi.
You can still create a wireless network from your computer and other devices can then connect to that network.
It won't have internet access of course -- it's just a way for other machines to talk to yours, despite the fact that none of you can talk to the outside world.
This is referred to as creating an *ad hoc* wireless network.
The students using the JIRP laptops will have to connect to this network so you'll want to make the network name and password easy to give out.

#### MacOS and Linux

You can do this from the wifi graphical interface.
Click the wifi icon in your system tray, select "Create new wireless network" and pick a name.
On Linux you have the option of setting a password but on MacOS you can only create an unsecured network.
This is not a problem because there is no one else around unless something has gone horribly wrong.
Once you've set up the ad hoc network, right click the wifi icon and select "Connection information".
Make a note of what the IP address is; you'll need it later.

#### Windows

You can only set up an ad hoc network on Windows through PowerShell; see [this SO question](https://superuser.com/questions/1658424/how-do-i-create-a-wireless-ad-hoc-network-in-windows-10).

## Spin up a Jupyter server

You may already be familiar with using Jupyter notebooks by running the command `jupyter notebook` or `jupyter lab` at a terminal.
This will do a bunch of opaque nonsense and what you usually care about is that it'll open up a web browser for you to code in.
What this is really doing is starting a web server, and your browser becomes a client that connects to that server.
It's easy for your browser to connect to this server because they both reside on the same physical machine -- it doesn't need to resolve some web address through the internet.
What we're going to do here is add a few extra commands that will enable other machines on the same local network to connect to this server as well.

The command that you want to use is:
```shell
jupyter lab \
    --ServerApp.allow_remote_access=True \
    --ServerApp.token=<your special token> \
    --ip=<your IP address on the ad hoc network>
```
Let's break down what this is doing piece by piece.
First, we have to tell the server explicitly that we want to allow remote access.
You have to enable remote access explicitly because generally you do not want total strangers to be able to run code (read: mine shitcoins) on your computer.
Next, you have to pick an access token, which is basically a password.
Ordinarily, this is done for your and when you fire up a Jupyter server, the token is automatically entered in the web address, so you never see this step.
Again, this is a security thing.
Even if you want to allow remote access, you generally want to only grant it to people you know and not (again) a stranger mining shitcoin.
You'll have to manually enter this token on the JIRP laptops so I usually make it something short like `abcd`.
Finally, you have to tell the Jupyter server what IP address the server will listen on.
By default, it will listen to connections on your machine only (localhost); you have to tell it explicitly to listen on another address.

## Connect to the Jupyter server

Now on the JIRP or other laptop, connect to the wireless network you created in the first step.
Open up a browser and navigate to this address:
```
http://<your IP address on the ad hoc network>/lab?token=<your special token>
```
using the IP address and token you chose in the previous step.
This should allow the JIRP laptop to talk to the Jupyter server and create and run notebooks.

Note that this allows students to see files on the server machine, but only if they're in a subdirectory of where you started the server from.
So if you want them to have access to, say, some remote sensing data, you'll need to put it in a directory on your machine where they can see it.
Likewise, if they create a file, for example a figure, they might need to get it off of your machine.
The students are basically using the JIRP machine like a dumb terminal to talk to yours; your machine can't access the file system of the JIRP laptop.
