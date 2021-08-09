# Media Downloader
<img src="https://img.shields.io/static/v1?message=Python&logo=python&labelColor=306998&color=ffd43b&logoColor=white&label=%20&style=flat-square" alt="python"> <img src="https://img.shields.io/static/v1?message=Docker&logo=docker&labelColor=384d54&color=0db7ed&logoColor=white&label=%20&style=flat-square" alt="docker"> <img src="https://img.shields.io/static/v1?message=Prometheus&logo=prometheus&labelColor=ce3f3c&color=ce3f3c&logoColor=white&label=%20&style=flat-square" alt="prometheus"> <img src="https://img.shields.io/static/v1?message=Grafana&logo=Grafana&labelColor=F05A28&color=F05A28&logoColor=white&label=%20&style=flat-square" alt="grafana">
[![asciicast](https://asciinema.org/a/v3uJFSjjkOsEIbJcuaechlvDN.svg)](https://asciinema.org/a/v3uJFSjjkOsEIbJcuaechlvDN)
<a href="https://asciinema.org/a/v3uJFSjjkOsEIbJcuaechlvDN" target="_blank"><img src="https://asciinema.org/a/v3uJFSjjkOsEIbJcuaechlvDN.svg" /></a>


## Description

A **Multi-Thread** Media downloader for small size files like image.

## Getting Started

### Dependencies

Dependencies are listed in `requirements.txt` file and automatically installed by `Docker`.

### Executing
Environment Variables can set/change in `docker-compose.yml`
```yaml
environment:
      DOWNLOADER_MODE: "VPN"
      DOWNLOADER_THREAD_NO: "40"
      REQUEST_TIMEOUT: "30"
      CONNECTION_ESTABLISHMENT_TIMEOUT: "1"
      DOWNLOADING_PATH: "media"
      DOWNLOADER_MAX_RETRY: "1"
```

run downloader by following command:

```sudo docker-compose up```

after successfully run this command logs should be like this:

<img src="./console.png" alt="console">

`Prometheus Metrics` are accessible in `localhost:5000`

Metrics are:
1. `File_Average_Size`
1. `Total` count
1. `Faild` count
1. `Success` count
1. `Permissoin_Denied` errors count
1. `Not_Found` errors count
1. `Internal_Server` errors count
1. `Timeout` errors count   
1. `Not_Valid` errors count   
1. `File_Average_Time` count
1. `Average_Rate` of downloading files
1. `File_Per_Second` count


### Result
All downloaded file saved with a unique `uuid` in  `DOWNLOADING_PATH` folder specified name in environment variable in `docker-compose.yml`.

You can clone `prometheus` from [here](https://github.com/vegasbrianc/prometheus) and track live data reporting by 
`Gragana` panel running on `localhost:3000`

**Notice**: you should change `targets` in `prometheus/prometheus/prometheus.yml` to:
```yaml
scrape_configs:
  - job_name: my-service
    static_configs:
      - targets:
        - {YOUR-SYSTEM-IP-ADDRESS}:5000
```

**Grafana** panel should be something like this:

<img src="./grafana.png" alt="grafana">

### Authors
Amir Rezaei [@ameerezae](https://github.com/ameerezae)
