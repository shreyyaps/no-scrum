# Python Imports, Modules, And Packages

Think of Python imports as finding and loading Python files, then giving you
access to the objects inside them.

## A `.py` File Is A Module

If you have:

```text
math_utils.py
```

Python sees that file as a module named:

```py
math_utils
```

Inside:

```py
# math_utils.py
def add(a, b):
    return a + b

PI = 3.14
```

You can import the module:

```py
import math_utils

math_utils.add(1, 2)
math_utils.PI
```

Or import objects from it:

```py
from math_utils import add, PI

add(1, 2)
PI
```

So:

```py
import math_utils
```

imports the file/module.

```py
from math_utils import add
```

imports a name/object from inside that file.

## A Folder Can Be A Package

A package is basically a folder that contains Python modules.

```text
api/
├── router.py
└── users.py
```

Python can treat `api` as a package. Then:

```py
from api.router import api_router
```

means:

```text
look inside api/
look for router.py
from that file, import api_router
```

So this:

```py
from api.router import api_router
```

maps to:

```text
api/router.py
```

and then finds:

```py
api_router = APIRouter()
```

inside that file.

## Dots Mean Go Deeper

Python import dots are not filesystem slashes, but they map closely to
folders/files.

```py
from api.v1.users import router
```

means:

```text
api/
└── v1/
    └── users.py
```

and inside `users.py`, find:

```py
router = ...
```

So mentally:

```py
api.v1.users
```

roughly means:

```text
api/v1/users.py
```

Then:

```py
from api.v1.users import router
```

means:

```text
from api/v1/users.py import router
```

## Importing A Module vs Importing Something From A Module

These are different:

```py
from api.v1 import users
```

This imports the whole `users.py` module.

Then you access things with:

```py
users.router
users.create_user
```

But this:

```py
from api.v1.users import router
```

imports only the `router` object from inside `users.py`.

Then you use:

```py
router
```

not:

```py
users.router
```

Example:

```py
from api.v1 import users

api_router.include_router(users.router)
```

versus:

```py
from api.v1.users import router

api_router.include_router(router)
```

Both can work. The first keeps it clearer where `router` came from.

## Current Backend Example

The backend has:

```text
backend/app/
├── main.py
└── api/
    ├── router.py
    └── v1/
        ├── users.py
        ├── roles.py
        ├── health.py
        └── organizations.py
```

In `main.py`:

```py
from api.router import api_router
```

means:

```text
from backend/app/api/router.py import api_router
```

In `api/router.py`:

```py
from api.v1 import health, organizations, roles, users
```

means:

```text
import backend/app/api/v1/health.py as health
import backend/app/api/v1/organizations.py as organizations
import backend/app/api/v1/roles.py as roles
import backend/app/api/v1/users.py as users
```

Then:

```py
api_router.include_router(users.router, prefix="/users")
```

means:

```text
take the router variable from users.py
mount it under /users
```

## How Python Knows Where To Start Looking

This is the most important intuition.

Python searches for imports in a list called:

```py
sys.path
```

You can think of `sys.path` as Python's list of import roots.

When you run the backend from:

```sh
cd backend/app
uv run fastapi dev main.py
```

Python puts this folder on the import path:

```text
backend/app
```

So this works:

```py
from api.router import api_router
```

because Python looks inside:

```text
backend/app/api/router.py
```

But this would not match the project convention:

```py
from backend.app.api.router import api_router
```

because that assumes the import root is the folder above `backend`, not
`backend/app`.

## Absolute Imports

This is an absolute import:

```py
from api.v1.users import router
```

It starts from an import root, like `backend/app`.

It does not mean absolute filesystem path like:

```text
/Users/shreydwiv/projects/no-scrum/backend/app/api/v1/users.py
```

It means absolute from Python's import root.

In this backend, these are absolute imports:

```py
from api.router import api_router
from core.config import settings
from db.session import get_db
from services import user_service
from models.user import User
```

All start from `backend/app`.

## Relative Imports

Relative imports use dots at the start:

```py
from .users import router
from ..db.session import get_db
```

A single dot means "same package".

```py
from . import users
```

Inside `api/v1/router.py`, that would mean:

```text
from api/v1 import users
```

Two dots mean "parent package".

```py
from ..router import api_router
```

Means go up one package.

This project intentionally avoids relative imports and uses bare absolute
imports like:

```py
from api.v1 import users
```

That is usually easier to read in small/medium backends.

## What About `__init__.py`?

Older Python required this:

```text
api/
└── __init__.py
```

to make `api` a package.

Modern Python also supports namespace packages, where folders can be importable
without `__init__.py`.

The backend rules say:

```text
No __init__.py files anywhere in backend/app/
```

So this project relies on namespace packages.

That is why this works even without `api/__init__.py`:

```py
from api.v1 import users
```

Python sees `api/` and `v1/` as namespace packages.

## Mental Model

Use this mapping:

```py
from api.v1.users import router
```

Read it as:

```text
Starting from an import root:
  find api/
  then v1/
  then users.py
  then get the name router from inside users.py
```

And:

```py
from api.v1 import users
```

Read it as:

```text
Starting from an import root:
  find api/
  then v1/
  then import users.py as a module object
```

That is the key difference.

In this code:

```py
from api.v1 import health, organizations, roles, users
```

you are importing four module objects.

Then:

```py
users.router
```

accesses a variable inside the `users.py` module.
