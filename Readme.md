## Custom Caching InMemory Server

#### Here I wrote a custom Caching InMemory Server using python which act like a redis. It listens on port 6379 and accept the connection from host 127.0.0.1.

#### To use this server
- python `custom-caching-server.py`
- Open another terminal
- Type `telnet 127.0.0.1 6379`
- Type command `TEST` and press Enter Key
- Above command should print `OK TESTED`
- You can test much more commands like: `SET`, `GET`, `DEL` etc...
- To set value of a key type `SET <key> <val>`
- To get value of a key type `GET <key> <val>` and so..on.