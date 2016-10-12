# scidb-restful-tornado
SciDB RESTful api via tornado

Tornado seems to be like Mongoose for Python. So this project is like an exploratory project for finding Shim alternatives. 

Instead of a query language, we want to make a REST API like

```
/get_variants
/insert_variant_file
/get_samples
```

We wrote a very basic demo. One option was to extend shim, but we opted for this Python Tornado thing (extremely easy to get going).

 - It's a bit hacky as it just calls `iquery` `save` right now and it returns the whole output as TSV. It doesnt have an advanced kind of `read_lines` thing. 
 - Solution depends on whether someone needs `read_lines` or if they expect it all to be simple stuff. 
 - There's also no "cancellation" at the moment.

The SSL is important so that username and password are passed encrypted over the network.

So this has 3 entry points:

```
/               # <-- run any query, using iquerytxt=...
/get_variants   #  <-- returns a set of variants from selected locations
/list_arrays    #  <-- just the list of the arrays
```
Example:

```
$ curl -k --data "username=root&password=Paradigm4&chromosome=7&start=123456&end=234567&limit=10" https://chandra1.eastus.cloudapp.azure.com:8890/get_variants
7    73841    A    <CN2>    DUP_gs_CNV_7_73841_134997    AC=7;AF=0.00139776;AN=5008;CS=DUP_gs;END=134997;NS=2504;SVTYPE=DUP
7    78321    A    <CN2>    DUP_uwash_chr7_78320_231876    AC=2;AF=0.000399361;AN=5008;CS=DUP_uwash;END=231876;NS=2504;SVTYPE=DUP
7    109065    G    <CN2>    DUP_uwash_chr7_109064_180542    AC=6;AF=0.00119808;AN=5008;CS=DUP_uwash;END=180542;NS=2504;SVTYPE=DUP
7    116566    G    <CN0>    UW_VH_15505    AC=1;AF=0.000199681;AN=5008;CIEND=0,175;CIPOS=-171,0;CS=DEL_union;END=124516;NS=2504;SVLEN=8123;SVTYPE=DEL
7    123456    T    G    rs189684716    AC=1;AF=0.000199681;AN=5008;NS=2504
7    123470    A    G    rs4458821    AC=1446;AF=0.288738;AN=5008;NS=2504
7    123481    C    G    rs114417607    AC=31;AF=0.0061901;AN=5008;NS=2504
7    123485    C    T    .    AC=1;AF=0.000199681;AN=5008;NS=2504
7    123494    C    T    rs148957509    AC=16;AF=0.00319489;AN=5008;NS=2504
7    123495    G    A    .    AC=2;AF=0.000399361;AN=5008;NS=2504
```

The `server.crt` and `server.key` are SSL things you have to generate with a weirdo set of commands - you can regenerate your own if you like. Included just for an example. Note the app sets the paths to these filenames.
See https://devcenter.heroku.com/articles/ssl-certificate-self

Start the server with

```
$ python ssl_query_server.py
```
