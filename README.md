# scidb-tornado

## Get started
Start the server with

```
$ python ssl_query_server.py
```

# Documentation

SciDB variant warehouse RESTful api via Python tornado

The following API are exposed:

```
/list_arrays    #  <-- just the list of the arrays
/get_genotype_by_snp_id                 #  Find the genotypes of `${Reference_SNP}` in all individuals    
/get_genotype_by_sample_and_position    #  <-- returns a set of variants from 
                                        #selected locations and selected samples
/               # <-- run any query, using additional argument "iquerytxt":"<QUERY>"...
/test_swagger   # <-- (work in progress) to test swagger docs
```

We wrote a very basic demo. One option was to extend shim, but we opted for this Python Tornado thing (extremely easy to get going).

 - It's a bit hacky as it just calls `iquery` `save` right now and it returns the whole output as TSV. It doesnt have an advanced kind of `read_lines` thing. 
 - Solution depends on whether someone needs `read_lines` or if they expect it all to be simple stuff. 
 - There's also no "cancellation" at the moment.

The SSL is important so that username and password are passed encrypted over the network.

## Example (`list_arrays`):

```
curl -k -X POST -H "Content-Type: application/json" -d '{
	"username":"root",
	"password":"Paradigm4"
}' "https://chandra1.eastus.cloudapp.azure.com:8888/list_arrays"
```
## Example (`get_genotype_by_snp_id`):

Find the genotypes of `${Reference_SNP}` in all individuals    

```
curl -k -X POST -H "Content-Type: application/json" -d '{
	"username":"root",
	"password":"Paradigm4",
	"snp_id": "snp_10_100155642"
}' "https://chandra1.eastus.cloudapp.azure.com:8888/get_genotype_by_snp_id"
```
## Example (`get_genotype_by_sample_and_position`):

Query 2 of genomics benchmark:
 
 - Find genotypes of all mutations in `${chromosome_nr}` between chromosomal coordinates
     `${position_X}` and `${position_Y}` in individuals `${list_of_n_individuals}`

 The elements in the queries that can vary, are reported as variables. They are:

 - `${chromosome_nr}`=chromosome number
 - `${position_X},${position_Y}`=start/end positions as integers
 - `${list_of_n_individuals}`=list containing n individual ids (e.g. [HG01572, HG01577, HG01578])

```
curl -k -X POST -H "Content-Type: application/json" -d '{
    "username":"root",
    "password":"Paradigm4",
    "chromosome_nr": "9",
    "position_X": "61334",
    "position_Y": "61334",
    "list_of_n_individuals": ["HG00096", "HG00100", "HG00101", "HG00102"],
    "limit": "10000"
}' "https://chandra1.eastus.cloudapp.azure.com:8888/get_genotype_by_sample_and_position"
```

Output:

```
false	false	true	0|0:-0.01,-1.66,-5.00:0.000:.:.	61334	HG00096
false	false	true	0|0:-0.06,-0.88,-5.00:0.000:.:.	61334	HG00100
false	false	true	0|0:-0.02,-1.27,-5.00:0.000:.:.	61334	HG00101
false	false	true	0|0:-0.00,-2.06,-5.00:0.000:.:.	61334	HG00102```
```

## Example (`/`):

```
curl -k -H "Content-Type: application/json" --data '{"username":"root","password":"Paradigm4", "iquerytxt":"list()"}'  https://chandra1.eastus.cloudapp.azure.com:8888/
```

# Notes

The `server.crt` and `server.key` are SSL things you have to generate with a weirdo set of commands - you can regenerate your own if you like. Included just for an example. Note the app sets the paths to these filenames.

See https://devcenter.heroku.com/articles/ssl-certificate-self
