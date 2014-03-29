MinecraftServerQueryPythonTCP
=============================

A quick and dirty class file for python to query Minecraft servers in TCP like Minecraft client does.

Usage
=============================

    >>> from minecraft_query import *
    >>> query = MinecraftQuery("urmcserver.net", 25565)
    >>> print(query.getResult())
    {'MaxPlayers': '50', 'MOTD': 'A Minecraft Server', 'Version': '1.7.2', 'OnlinePlayers': '20'}
    
    >>> query = MinecraftQuery("domaindoesnotexists.net", 25565)
    >>> print(query.getResult())
    {'MaxPlayers': 0, 'MOTD': '', 'Version': '', 'OnlinePlayers': 0, 'Error': "gaierror(-2, 'Name or service not known')"}

    >>> query = MinecraftQuery("serverisdown.net", 25565)
    >>> print(query.getResult())
    {'MaxPlayers': 0, 'MOTD': '', 'Version': '', 'OnlinePlayers': 0, 'Error': "timeout('timed out',)"}
