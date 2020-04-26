# edgar-collect
Download an centralize the edgar submissions for a particular company

# Source
[List of all company submissions by quarter](https://www.sec.gov/dera/data/financial-statement-data-sets.html)

# To Test
Macys's EDGAR ID `0000794367`


# To Parse Using zipgrep

```
 for file in *.zip; do zipgrep  0000794367 "$file"| grep num.txt >> ../macys.txt ; done
 ```

# To download

```
python main.py -y 2010 -d filings
```
