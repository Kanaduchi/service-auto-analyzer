# Auto-analysis service for ReportPortal

[![Tests](https://github.com/reportportal/service-auto-analyzer/actions/workflows/tests.yml/badge.svg)](https://github.com/reportportal/service-auto-analyzer/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/reportportal/service-auto-analyzer/branch/master/graph/badge.svg?token=Y3llbuAYLr)](https://codecov.io/github/reportportal/service-auto-analyzer)
[![Join Slack chat!](https://slack.epmrpp.reportportal.io/badge.svg)](https://slack.epmrpp.reportportal.io/)
[![stackoverflow](https://img.shields.io/badge/reportportal-stackoverflow-orange.svg?style=flat)](http://stackoverflow.com/questions/tagged/reportportal)
[![Build with Love](https://img.shields.io/badge/build%20with-❤%EF%B8%8F%E2%80%8D-lightgrey.svg)](http://reportportal.io?style=flat)

## Environment variables for configuration

| **Property name**               | **Type** | **Default value**          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 
|---------------------------------|----------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ES_HOSTS                        | string   | http\://elasticsearch:9200 | Elasticsearch host (can be either like this "http://elasticsearch:9200", or with login and password delimited by : and separated from the host name by @)                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ES_USER                         | string   |                            | Elasticsearch host login, set up here the username for elasticsearch, if you choose setup username here, in the **ES_HOSTS** you should leave only url without login and password                                                                                                                                                                                                                                                                                                                                                                                                      |
| ES_PASSWORD                     | string   |                            | Elasticsearch host password, set up here the password for elasticsearch, if you choose setup the password here, in the **ES_HOSTS** you should leave only url without login and password                                                                                                                                                                                                                                                                                                                                                                                               |
| LOGGING_LEVEL                   | string   | DEBUG                      | logging level for the whole module, can be DEBUG, INFO, ERROR, CRITICAL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| AMQP_URL                        | string   |                            | an url to the rabbitmq instance                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| AMQP_EXCHANGE_NAME              | string   | analyzer                   | Exchange name for the module communication for this module                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ANALYZER_PRIORITY               | integer  | 1                          | priority for this analyzer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ANALYZER_INDEX                  | boolean  | true                       | the parameter for rabbitmq exchange params, where the analyzer supports indexing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ANALYZER_LOG_SEARCH             | boolean  | true                       | the parameter for rabbitmq exchange params, where the analyzer supports searching logs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ANALYZER_SUGGEST                | boolean  | true                       | the parameter for rabbitmq exchange params, where the analyzer supports suggesting                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ANALYZER_CLUSTER                | boolean  | true                       | the parameter for rabbitmq exchange params, where the analyzer supports clustering                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ES_VERIFY_CERTS                 | boolean  | false                      | turn on SSL certificates verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ES_USE_SSL                      | boolean  | false                      | turn on SSL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ES_SSL_SHOW_WARN                | boolean  | false                      | show warning on SSL certificates verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ES_CA_CERT                      | string   |                            | provide a path to CA certs on disk                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ES_CLIENT_CERT                  | string   |                            | PEM formatted SSL client certificate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ES_CLIENT_KEY                   | string   |                            | EM formatted SSL client key                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ES_TURN_OFF_SSL_VERIFICATION    | boolean  | false                      | Turn off ssl verification via using RequestsHttpConnection class instead of Urllib3HttpConnection class.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ANALYZER_BINSTORE_TYPE          | enum     | filesystem                 | Possible values: "minio", "filesystem". Strategy where to store information, connected with the analyzer                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| MINIO_SHORT_HOST                | string   | minio:9000                 | you need to set short host and port to the minio service. This property is used in case `ANALYZER_BINARYSTORE_TYPE` is set to `minio`.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| MINIO_ACCESS_KEY                | string   | minio                      | you need to set a minio access key here                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| MINIO_SECRET_KEY                | string   | minio123                   | you need to set a minio secret key here                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ANALYZER_BINSTORE_BUCKETPREFIX  | string   | prj-                       | the prefix for buckets which are added to each project filepath.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ANALYZER_BINSTORE_MINIO_REGION  | string   |                            | the region which you can specify for saving in AWS S3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| INSTANCE_TASK_TYPE              | string   |                            | if you want to run a standard analyzer instance, leave it as blank. If you want to run an instance for training, set "train" here.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| FILESYSTEM_DEFAULT_PATH         | string   | storage                    | the path where will be stored all the information connected with analyzer, if `ANALYZER_BINARYSTORE_TYPE` is set to `filesystem`. If you want to mount this folder to some folder on your machine, you can use this instruction in the docker compose:<br/><code>volumes:<br/>&nbsp;&nbsp;- ./data/analyzer:/backend/storage</code>                                                                                                                                                                                                                                                    |
| ES_CHUNK_NUMBER                 | integer  | 1000                       | the number of objects which is sent to ES while bulk indexing. **NOTE**: AWS Elasticsearch has restrictions for sent data size either 10Mb or 100Mb, so when 10Mb is chosen, make sure you don't get the error "TransportError(413, '{"Message": "Request size exceeded 10485760 bytes"}')" while generating index or indexing the data. If you get this error, please, decrease ES_CHUNK_NUMBER until you stop getting this error.                                                                                                                                                    |
| ES_CHUNK_NUMBER_UPDATE_CLUSTERS | integer  | 500                        | the number of objects which is sent to ES while bulk updating clusters. **NOTE**: AWS Elasticsearch has restrictions for sent data size either 10Mb or 100Mb, so when 10Mb is chosen, make sure you don't get the error "TransportError(413, '{"Message": "Request size exceeded 10485760 bytes"}')" while generating index or indexing the data. If you get this error, please, decrease ES_CHUNK_NUMBER_UPDATE_CLUSTERS until you stop getting this error.                                                                                                                           |
| ES_PROJECT_INDEX_PREFIX         | string   |                            | the prefix which is added to the created for each project indices. Our index name is the project id, so if it is 34, then the index "34" will be created. If you set ES_PROJECT_INDEX_PREFIX="rp_", then "rp_34" index will be created. We create several other indices which are sharable between projects, and this prefix won't influence them: rp_aa_stats, rp_stats, rp_model_train_stats, rp_done_tasks, rp_suggestions_info_metrics. **NOTE**: if you change an environmental variable, you'll need to generate index, so that a nex index is created and filled appropriately. |
| AUTO_ANALYSIS_TIMEOUT           | integer  | 300                        | which sets timeout in seconds for auto-analysis operations to return results after this timeout, so if the request to the analyzer will be running out of time, the analyzer stops processing and returns results to the backend.                                                                                                                                                                                                                                                                                                                                                      |
| ANALYZER_MAX_ITEMS_TO_PROCESS   | integer  | 4000                       | How many test items can be processed for one request, so if analyzer processes more than 4000 items, the analyzer stops processing and returns results to the backend.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ANALYZER_HTTP_PORT              | integer  | 5001                       | the http port for checking status of the analyzer. It is used when you run the analyzer without Docker and uwsgi. If you use Docker, you will use the port 5001 and remap it to the port you want. If you use wsqgi for running the analyzer, you can remap the port with --http :5000 parameter in cmd or app.ini.                                                                                                                                                                                                                                                                    | 
| ANALYZER_FILE_LOGGING_PATH      | string   | /tmp/config.log            | the file for logging what's happening with the analyzer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

## Environmental variables for constants, used by algorithms

| **Property name**               | **Type** | **Default value** | **Description**                                                                                                                                                                                                                                                                                                                       | 
|---------------------------------|----------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ES_MIN_SHOULD_MATCH             | string   | 80%               | the global default min should match value for auto-analysis, but it is used only when the project settings are not set up.                                                                                                                                                                                                            |
| ES_BOOST_AA                     | float    | -8.0              | the value to boost auto-analyzed items while querying for Auto-analysis                                                                                                                                                                                                                                                               |
| ES_BOOST_LAUNCH                 | float    | 4.0               | the value to boost items with the same launch while querying for Auto-analysis                                                                                                                                                                                                                                                        |
| ES_BOOST_TEST_CASE_HASH         | float    | 8.0               | the value to boost items with the same test case hash while querying for Auto-analysis                                                                                                                                                                                                                                                |
| ES_MAX_QUERY_TERMS              | integer  | 50                | the value to use in more like this query while querying for Auto-analysis                                                                                                                                                                                                                                                             |
| ES_MIN_WORD_LENGTH              | integer  | 2                 | the value to use in more like this query while querying for Auto-analysis                                                                                                                                                                                                                                                             |
| PATTERN_LABEL_MIN_PERCENT       | float    | 0.9               | the value of minimum percent of the same issue type for pattern to be suggested as a pattern with a label                                                                                                                                                                                                                             |
| PATTERN_LABEL_MIN_COUNT         | integer  | 5                 | the value of minimum count of pattern occurrence to be suggested as a pattern with a label                                                                                                                                                                                                                                            |
| PATTERN_MIN_COUNT               | integer  | 10                | the value of minimum count of pattern occurrence to be suggested as a pattern without a label                                                                                                                                                                                                                                         |
| MAX_LOGS_FOR_DEFECT_TYPE_MODEL  | integer  | 10000             | the value of maximum count of logs per defect type to add into defect type model training. Default value is chosen in cosideration of having space for analyzer_train docker image setuo of 1GB, if you can give more GB you can linearly allow more logs to be considered.                                                           |
| PROB_CUSTOM_MODEL_SUGGESTIONS   | float    | 0.7               | the probability of custom retrained model to be used for running when suggestions are requested. The maximum value is 0.8, because we want at least 20% of requests to process with a global model not to overfit for project too much. The bigger the value of this env varibale the more often custom retrained model will be used. |
| PROB_CUSTOM_MODEL_AUTO_ANALYSIS | float    | 0.5               | the probability of custom retrained model to be used for running when auto-analysis is performed. The maximum value is 1.0. The bigger the value of this env varibale the more often custom retrained model will be used.                                                                                                             | 
| MAX_SUGGESTIONS_NUMBER          | integer  | 3                 | the maximum number of suggestions shown in the ML suggestions area in the defect type editor.                                                                                                                                                                                                                                         |

## Instructions for analyzer setup without Docker

Install python with the version 3.7.4. (it is the version on which the service was developed, but it should work on the versions starting from 3.6).

Perform next steps inside source directory of the analyzer.

### For Linux:

#### Analyzer

1. Create a virtual environment with any name (in the example **/venv**)
```bash
  python -m venv /analyzer
```
2. Install python libraries
```bash
  /analyzer/bin/pip install --no-cache-dir -r requirements.txt
```
3. Activate the virtual environment
```bash
  /analyzer/bin/activate
```
4. Install stopwords package from the nltk library
```bash
  /analyzer/bin/python3 -m nltk.downloader -d /usr/share/nltk_data stopwords
```
5. Start the uwsgi server, you can change properties, such as the workers quantity for running the analyzer in the several processes
```bash
  /analyzer/bin/uwsgi --ini res/analyzer.ini
```
 
#### Analyzer Train

1. Create a virtual environment with any name (in the example **/venv**)
```bash
  python -m venv /analyzer-train
```
2. Install python libraries
```bash
  /analyzer-train/bin/pip install --no-cache-dir -r requirements.txt
```
3. Activate the virtual environment
```bash
  source /analyzer-train/bin/activate
```
4. Install stopwords package from the nltk library
```bash
  /analyzer-train/bin/python3 -m nltk.downloader -d /usr/share/nltk_data stopwords
```
5. Start the uwsgi server, you can change properties, such as the workers quantity for running the analyzer train in the several processes
```bash
  /analyzer-train/bin/uwsgi --ini res/analyzer-train.ini
```

### For Windows:
1. Create a virtual environment with any name (in the example **env**)
```
python -m venv env
```
2. Activate the virtual environment
```
call env\Scripts\activate.bat
```
3. Install python libraries
```
python -m pip install -r requirements_windows.txt
```
4. Install stopwords package from the nltk library
```
python -m nltk.downloader stopwords
```
5. Start the program.
```
python app/app.py
```
