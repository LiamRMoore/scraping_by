
# Run webscraper

```bash
python scrapers/pcs/api.py
```

# How the data model/schema was generated

Get a sample of the JSON output from the API (contract notices, in OCDS format):

```bash
curl --location --request GET 'https://api.publiccontractsscotland.gov.uk/v1/Notices?noticeType=2&outputType=0' > release_packages.json
```

Normalise the releases (consolidating all the "diffs" from the release json into a latest version for each unique contract) using [OCDSKit](https://github.com/open-contracting/ocdskit):

```bash
cat release_packages.json | ocdskit --encoding iso-8859-1 compile > compiled_releases.json
```

Construct the pydantic model (assuming [datamodel](https://pydantic-docs.helpmanual.io/datamodel_code_generator/) is installed) from the JSON returned from the API.

```bash
datamodel-codegen  --input release_packages.json --input-file-type json --output model.py
```