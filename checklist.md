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

## 3. Release at Github

In the normal way. Use 3-part semantic versioning, so if we change the data fields we're including in any sub-component, or if we add/alter other components, then we need to do a major number increment. Otherwise, we just increment the middle number. We would only increment minor number if we were issuing a corrected version.

## 4. Fix up Zenodo release

Zenodo should automatically create a new entry for the release from Github, but the project-level metadata isn't carried over. You'll need to copy/paste/modify as appropriate from the prior one. We should look into whether/how to automate this aspect.

NB: The Zenodo master record DOI is <a href="https://doi.org/10.5281/zenodo.1193921"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1193921.svg" alt="DOI 10.5281/zenodo.1193921" /></a>, which will always redirect to the most recent record.

## 5. Release a copy via NYU FDA

Visit archive.nyu.edu, login, navigate to the appropriate collection, point-and-click to happiness. You may have to copy metadata from an earlier version. Once the submission is complete and a Handle URI assigned, go back to Zenodo and enter that handle as an alternate identifier for the dataset.

## 6. Announce it to the world

Promulgate on Pleiades social media.
Time for a blog post at pleiades.stoa.org.



