> Copyright 2021 Ball Aerospace & Technologies Corp.
>
> All Rights Reserved.
>
> This program is free software; you can modify and/or redistribute it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; version 3 with attribution addendums as found in the LICENSE.txt

## Environment Variables


### COSMOS_DEBUG

Updated from v0 to v1 for the ballcosmos libaray. In v1 the libary can log much more of what is happening in the libary. If you wish to enable this you MUST set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this is not set you will not get log messages if this is an incorrect log level you will get a ValueError.

```python
import os

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = ""
```

#### COSMOS_X_CSRF_TOKEN

Updated from v0 to v1 for the ballcosmos libaray. In Cosmos v4.5.0 we added a password to the api this can be changes in the setting of Cosmos v4. If you need to use a different password you can set the environment variable `COSMOS_X_CSRF_TOKEN` to the password on your Cosmos v4 instance. If this is not set the password will default to SuperSecret the same default as Cosmos v4.

```python
import os

try:
    os.environ["COSMOS_X_CSRF_TOKEN"]
except KeyError:
    os.environ["COSMOS_X_CSRF_TOKEN"] = ""
```


