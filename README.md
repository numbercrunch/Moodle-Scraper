# Moodle Scraper 🔮

## Web scraper for downloading files from TUM moodle plattform
### **Searches through your course directories and downloads their respective files.**

### HOWTO:

To install on Mac or Linux open `Terminal` and navigate to the directory where you want to save the application e.g.:

```bash
cd Documents

git install https://github.com/Moritz-M/moodle_scraper.git
```

This may take a long time as embedded in the source code is a headless browser (PhantomJS webkit).

```bash
cd moodle_scraper

open SETTINGS
```

This will open the `SETTINGS` file:
**IMPORTANT **: edit only in the following way:

USERNAME

PASSWORD

SEMESTER

as well as the courses seperated by new lines at the end of the file.

```bash
source bin/activate

python3 moodle_scraper
```
**Hopefully all files will be downloaded, enjoy!**


## TODO:
- [x] implement course selection through code ID
- [x] implement file structure organization in directories: pre or postdownload?
- [ ] create installer file for `setuptools.py`
- [ ] checking if file downloaded completed successfully by using a log file: filename added to log after all chunks have been downloaded