# BuddhaSpider

BuddhaSpider is a Scrapy project for fetching [91Porn](http://91porn.com/index.php) videos. This is a New Year's gift for everyone. You know what I mean.😜

# Extracted data

This project extracts videos and their information.The extracted data is 
stored in the sqlite.You can fetch all the videos data from the `buddha.sqlite3` file.

# Running the spiders

Or you can run the spider using the `python start.py` command, such as:

```shell
$ python start.py
```

Note: Maybe you need breakthrough the GFW. Then I will recommend [Lantern](https://getlantern.org/zh_CN/). And if so, you need to check the `PROXY` in `settings.py`.

# Requirements

Maybe you need the following dependencies:

- scrapy
- pandas
- base64
- re
- logging
- sqlite3

Run `pip install -r requirements.txt` to install them. Maybe you need `sudo`.

You can enjoy the vidoes or study Scrapy through BuddhaSpider project. Please feel free to let me know if you have any questions.

# License
MIT. See the `LICENSE.md` file.