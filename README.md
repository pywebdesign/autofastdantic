# AutoFastDantic

AutoFastDantic is a opinionated framework on top of fastapi that leverage pydantic and nosql to enable very fast draft project and quick time to market for small scale project. It is not ready nor even usable right now. It still contains a lot of unmaintainable shortcuts that are planned to be addressed.

The main goal is to explore the pydantic model soft typing system to infere and low code our way into persisting data and getting a RESTful interface. It is motivated by the fact that most fastapi project has repeated inbformation on models and on patterns, we see repeated type definition between pydantic model and sql migrations and we also see a lot of repeated pattern in the CRUD code over each model.

We would like a more declarative layer on top where you would say, here's my model, here's my rules, do the rest.

# Declarative is low code

Declaring requirements is low code for me, the more high level declaration you can make the lower the amount of code. When LLM are taking high level declarationa and aiming to produce working code sometimes, here we create a wrapper specialized in normal frequent repeating crud code over fastapi and aim to produce working project with as little code as possible, where still letting the user access to underlying fastapi level api.


# Rules and decorator based

We explore 2 approach to express intent to the system in a declarative way, first we explore rules based

## Rules
For example in a model you can limit the crud scope by setting auxiliary class that the framework will detect and use. Here's the model Artist that contains a _Access subclass with a rule that whitelist Listing of the resources in the resulting api.

```python
from typing import List

import datetime

from autofastdantic.basemodel import BaseModel
from autofastdantic.utils.utc_datetime import utc_datetime

class Artist(BaseModel):
    class _Access:
        List=True
    name: str
    nationality: str
    location: str
    since: datetime.date
    biography: str
```

## Decorator

We plan to use decorator to wrap rulesset together on a subject and also allow complex parametrisation of the ruleset. Here we have a very minimal Loggable decorator that enable to specify a class a logguable. right now we only set the field to use to retreive the record before verifying the login status. The aim would be to be able to defined multiple rulesets to choose from and parametrize them in a way to support the user in adding a loging system. those rulset could be plugin to the framework like rails specific gems to rails.

```python

@traits.Loggable("email")
class User(BaseModel):

        
    email: str = Field(..., indexed=True)
    password: SecretStr = Field(..., exclude=True)
    password_hash: str = Field(None, exclude=True)
    password_repeat: SecretStr = Field(..., exclude=True)

    @validator("password_hash", always=True)
    def password_matches(cls, v, values):
        hashed = bcrypt.hashpw(
                 base64.b64encode(hashlib.sha256(values["password"]).digest()),
                 bcrypt.gensalt()
        )
        return hashed
    

    @validator("password_repeat")
    def passord_matches(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return None

```


# TODO

- current pg nosql ish json record design usage will not scale well. We should have an interface layer so we could wrap and reuse pydantic orm style OSS projects.
- current Loggable / login is not usable and we need to wrap battletested auth framework and not bake our own
- Resources relationship is not implemented. we need a way to express relationship better like an Activerecord or django ORM or massonite.
- Tests for autofastdantic, and probably a set of tests mock an utils for making TTD good for autofastdantic


# Further exploration

- Can we hook into import system and have models comes from url and are dynamicall loaded
- Could we infer pydantic classes from the pg table definition instead of nosql
- How can we ensure coupling is minimal if we stich all declarations mainly in the models. What does not belongs to models? Do we need considering ultimately that very high level declaration can only couple together underlying requirements. For example when I say make me a crud api with the MVC pattern, it does couple all the MVC layers together in the high level requirements. 