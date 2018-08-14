# Pleiades Datasets Checklist

Steps for producing an archive-ready version of pleiades-datasets

## 1. Update all constituent components

### CSV

```bash
./scripts/get_csv.sh
```

### HTML

```bash
curl https://pleiades.stoa.org/credits.html > html/credits.html
```

### JSON

```bash
python scripts/get_json.py
```

### RDF

```bash
./scripts/get_ttl.sh
```

## 2. add and commit all changes and push to master at github

(Change datestamp on second command!)

```bash
git add csv html json rdf
git commit -m "yyyymmdd updates"
git push origin master
```



