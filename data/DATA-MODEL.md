# Data Model
We keep the data in two seperate files: 
+ the ./data/stats_latest.json, containing only the latest Stats
+ the ./data/stats_history.json, containing only the history Stats

The stats_latest json is structured like this:

````json5
{
    "world_wide": {
          "incidence": 123.456,
          "active": 123,
          "deaths": 123,
          "cured": 123,
          "time_checked": "time stamp"
    }
}
````

and the history stats is structured like this:

````json5
{
    "world_wide": [
        {
            "incidence": 123.456,
            "active": 123,
            "deaths": 123,
            "cured": 123,
            "time": "time stamp"
        }
    ]
}
````

but then for all locations. The location keys are:

+ **world_wide**
+ **germany**
+ **oberhausen**
+ **kleve**
+ **hannover**

