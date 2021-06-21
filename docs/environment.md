> Copyright 2021 Ball Aerospace & Technologies Corp.
>
> All Rights Reserved.
>
> This program is free software; you can modify and/or redistribute it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; version 3 with attribution addendums as found in the LICENSE.txt

## Environment Variables

### COSMOS_VERSION

Updated from v0 to v1 for the ballcosmos libaray. In v1 the libary is expacting a version. If you are using Cosmos v4 you MUST set the environment variable `COSMOS_VERSION` to equal 4. If this is not set the api endpoint and authentication will be incorrect.

```python
import os

try:
    os.environ["COSMOS_VERSION"]
except KeyError:
    os.environ["COSMOS_VERSION"] = "4"
```

### COSMOS_HOSTNAME

Updated from v0 to v1 for the ballcosmos libaray. In v1 you CAN set the hostname for all Cosmos v4 scripts. In v0 of ballcosmos it would default to 127.0.0.1. The hostname can now be set via an environment variable `COSMOS_HOSTNAME` to network address of the computer running Cosmos.

```python
import os

try:
    os.environ["COSMOS_HOSTNAME"]
except KeyError:
    os.environ["COSMOS_HOSTNAME"] = "127.0.0.1"
```

### COSMOS_PORT

Updated from v0 to v1 for the ballcosmos libaray. In v1 you MUST set the port for all cosmos v4 scripts. In v0 of ballcosmos the port was hard coded and would default to 7777 for Cosmos v4. In v1 the port can be set via an environment variable  `COSMOS_PORT` to the network port of the computer running Cosmos. Note the new port for Cosmos v5 is 2900

```python
import os

try:
    os.environ["COSMOS_PORT"]
except KeyError:
    os.environ["COSMOS_PORT"] = "7777"
```

### COSMOS_DEBUG

Updated from v0 to v1 for the ballcosmos libaray. In v1 the libary can log much more of what is happening in the libary. If you wish to enable this you MUST set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this is not set you will not get log messages if this is an incorrect log level you will get a ValueError.

```python
import os

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = ""
```
