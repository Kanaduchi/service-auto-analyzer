#  Copyright 2023 EPAM Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
import json
import pika
from app.commons import launch_objects

logger = logging.getLogger("analyzerApp.amqpHandler")


def prepare_launches(launches):
    """Function for deserializing array of launches"""
    return [launch_objects.Launch(**launch) for launch in launches]


def prepare_suggest_info_list(suggest_info_list):
    """Function for deserializing array of suggest info results"""
    return [launch_objects.SuggestAnalysisResult(**res) for res in suggest_info_list]


def prepare_search_logs(search_data):
    """Function for deserializing search logs object"""
    return launch_objects.SearchLogs(**search_data)


def prepare_launch_info(launch_info):
    """Function for deserializing search logs object"""
    return launch_objects.LaunchInfoForClustering(**launch_info)


def prepare_clean_index(clean_index):
    """Function for deserializing clean index object"""
    return launch_objects.CleanIndex(**clean_index)


def prepare_delete_index(body):
    """Function for deserializing index id object"""
    return int(body)


def prepare_test_item_info(test_item_info):
    """Function for deserializing test item info for suggestions"""
    return launch_objects.TestItemInfo(**test_item_info)


def prepare_search_response_data(response):
    """Function for serializing response from search request"""
    return json.dumps(response)


def prepare_analyze_response_data(response):
    """Function for serializing response from analyze request"""
    return json.dumps([resp.dict() for resp in response])


def prepare_index_response_data(response):
    """Function for serializing response from index request
    and other objects, which are pydantic objects"""
    return response.json()


def output_result(response):
    """Function for serializing int object"""
    return str(response)


def handle_amqp_request(channel, method, props, body,
                        request_handler, prepare_data_func=prepare_launches,
                        prepare_response_data=prepare_search_response_data,
                        publish_result=True):
    """Function for handling amqp reuqest: index, search and analyze"""
    logger.debug("Started processing %s method %s props", method, props)
    logger.debug("Started processing data %s", body)
    try:
        launches = json.loads(body, strict=False)
    except Exception as err:
        logger.error("Failed to load json from body")
        logger.error(err)
        return False
    try:
        launches = prepare_data_func(launches)
    except Exception as err:
        logger.error("Failed to transform body into objects")
        logger.error(err)
        return False
    try:
        response = request_handler(launches)
    except Exception as err:
        logger.error("Failed to process launches")
        logger.error(err)
        return False

    try:
        response_body = prepare_response_data(response)
    except Exception as err:
        logger.error("Failed to dump launches result")
        logger.error(err)
        return False
    if publish_result:
        try:
            if props.reply_to:
                channel.basic_publish(exchange='',
                                      routing_key=props.reply_to,
                                      properties=pika.BasicProperties(
                                          correlation_id=props.correlation_id,
                                          content_type="application/json"),
                                      mandatory=False,
                                      body=response_body)
        except Exception as err:
            logger.error("Failed to publish result")
            logger.error(err)
    logger.debug("Finished processing %s method", method)
    return True


def handle_inner_amqp_request(channel, method, props, body, request_handler):
    """Function for handling inner amqp reuqests"""
    logger.debug("Started processing %s method %s props", method, props)
    logger.debug("Started processing data %s", body)
    try:
        stats_info = json.loads(body, strict=False)
    except Exception as err:
        logger.error("Failed to load json from body")
        logger.error(err)
        return False
    try:
        request_handler(stats_info)
    except Exception as err:
        logger.error("Failed to process stats info")
        logger.error(err)
        return False
    logger.debug("Finished processing %s method", method)
    return True
