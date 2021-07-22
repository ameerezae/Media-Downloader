# Media Downloader

#### under construction ...


## Description
<img src="https://img.shields.io/static/v1?message=Python&logo=python&labelColor=306998&color=ffd43b&logoColor=white&label=%20&style=flat-square" alt="python"> <img src="https://img.shields.io/static/v1?message=Docker&logo=docker&labelColor=384d54&color=0db7ed&logoColor=white&label=%20&style=flat-square" alt="docker"> <img src="https://img.shields.io/static/v1?message=Python&logo=prometheus&labelColor=ce3f3c&color=white&logoColor=white&label=%20&style=flat-square" alt="prometheus">

A **Multi-Thread** Media downloader for small size files like image.

## Getting Started

### Dependencies

Dependencies are listed in `requirements.txt` file and automatically installed by `Docker`.

### Executing

run downloader by following command:

```sudo docker-compose up```

after successfully run this command logs should be like this:
\
<img src="./console.png" alt="console">

`Prometheus Metrics` are accessible in `localhost:5000`\
Metrics like:
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


### Authors
Amir Rezaei [@ameerezae](https://github.com/ameerezae)
