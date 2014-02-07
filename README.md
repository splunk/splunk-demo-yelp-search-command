splunk-demo-yelp-search-command
===============================

A custom search command for querying yelp's API. This demonstrates how to use the Python SDK's `GeneratingCommand` to query an external API and pipe results into Splunk. You can use the patterns here basically for talking to any API.

# What is it?

This is a custom search command implemented using Python SDK which uses Yelp's API. It allows issuing adhoc queries realtime against Yelp data which is then pulled into Splunk.

# Pre-requisites.

* An instance of Splunk where you can install the command.
* An valid set of API credentials for Yelp's API. Sign up [here] (http://www.yelp.com/developers/getting_started) for an account and register for an API key.

# Setup

* Copy this application to a new folder in your `$SPLUNK_HOME$\etc\apps\` folder.
* Change to the bin folder of your app and rename the config.template file to config.json.
* Edit the config.json with your favorite text editor replace the values with the corresponding values from the [Yelp API management portal] (http://www.yelp.com/developers/getting_started/api_access).
* Restart your splunk instance so the the app is loaded.

# Yelp Command 101

Using the Yelp command is very easy, open your Splunk portal and go to the Yelp Search app. Now you can use the "yelp" command. Below are a few simple examples of syntax.

Finding sushi and italian restaurants in San Francisco
```
| yelp location="San Franciso" term=sushi,italian
```

Finding sports shops in New York

```
| yelp location="New York" term="Sporting Goods"
```

Finding all skydiving places in New Zealand

```
| yelp location="Auckland, New Zealand" term="Sky diving"
```

Finding all museums in London

```
| yelp location="London" term=museums
```

# Parameters

The following is the list of parameters. Any values that contain spaces, must be within double quotes.

* location - [required] Location to search for businesses
* term - [optional] Type of business to search for.
* category - [optional] Delimitted list of categories. See [here] (http://www.yelp.com/developers/documentation/category_list) for the supported list.
* sort - [optional] 0=Best matched, 1=Distance (default), 2=Highest Rated
* limit [optional] Number of records to return. (max=20).
* offset [optional] Offset the list of returned business results by this amount.

# Running outside of Splunk.

For testing you can actually run the command outside of Splunk. Below are the steps.

* Go to the bin folder underneath the app.
* Use the following command template:

```
python yelp.py __EXECUTE__ location=[location] term=[term] < empty.csv
```

This will run the command and dump the results to your console. For example...

```
python yelp.py __EXECUTE__ location=NY term=italian < empty.csv
```

If the paramter has spaces, surround the full parameter and value in single quotes and use double quotes for the value i.e.

```
python yelp.py __EXECUTE__ 'location="San Francisco"' term=korean < empty.csv
```


# License

Apache 2.0







