Build: <br />
````docker build -t app .````

Run: <br />
args:
- path to local sample file which will mount into container
- path to sample file in container

````docker run -v /path/to/local/sample.txt:/app/sample.txt test --path=/app/sample.txt````
