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

from typing import List
from pydantic import BaseModel
from datetime import datetime


class AnalyzerConf(BaseModel):
    """Analyzer config object"""
    analyzerMode: str = "ALL"
    minShouldMatch: int = 0
    numberOfLogLines: int = -1
    isAutoAnalyzerEnabled: bool = True
    indexingRunning: bool = True
    allMessagesShouldMatch: bool = False
    searchLogsMinShouldMatch: int = 95
    uniqueErrorsMinShouldMatch: int = 95


class SearchLogInfo(BaseModel):
    """Search log info"""
    logId: int
    testItemId: int
    matchScore: float


class Log(BaseModel):
    """Log object"""
    logId: int
    logLevel: int = 0
    logTime: List[int] = list(datetime.now().timetuple())[:7]
    message: str
    clusterId: int = 0
    clusterMessage: str = ""


class TestItem(BaseModel):
    """Test item object"""
    testItemId: int
    uniqueId: str
    isAutoAnalyzed: bool
    issueType: str = ""
    originalIssueType: str = ""
    startTime: List[int] = list(datetime.now().timetuple())[:7]
    testCaseHash: int = 0
    testItemName: str = ""
    logs: List[Log] = []


class TestItemInfo(BaseModel):
    """Test item info object"""
    testItemId: int = 0
    uniqueId: str = ""
    testCaseHash: int = 0
    clusterId: int = 0
    launchId: int
    launchName: str = ""
    testItemName: str = ""
    project: int
    analyzerConfig: AnalyzerConf = AnalyzerConf()
    logs: List[Log] = []


class Launch(BaseModel):
    """Launch object"""
    launchId: int
    project: int
    launchName: str = ""
    launchStartTime: List[int] = list(datetime.now().timetuple())[:7]
    analyzerConfig: AnalyzerConf = AnalyzerConf()
    testItems: List[TestItem] = []
    clusters: dict = {}


class LaunchInfoForClustering(BaseModel):
    launch: Launch
    project: int
    forUpdate: bool = False
    numberOfLogLines: int
    cleanNumbers: bool = False


class AnalysisResult(BaseModel):
    """Analysis result object"""
    testItem: int
    issueType: str
    relevantItem: int


class ClusterInfo(BaseModel):
    clusterId: int
    clusterMessage: str
    logIds: List[int]
    itemIds: List[int]


class ClusterResult(BaseModel):
    """Analysis result object"""
    project: int
    launchId: int
    clusters: List[ClusterInfo]


class SuggestAnalysisResult(BaseModel):
    """Analysis result object"""
    project: int
    testItem: int
    testItemLogId: int
    launchId: int
    launchName: str
    issueType: str
    relevantItem: int
    relevantLogId: int
    isMergedLog: bool = False
    matchScore: float
    resultPosition: int
    esScore: float
    esPosition: int
    modelFeatureNames: str
    modelFeatureValues: str
    modelInfo: str
    usedLogLines: int
    minShouldMatch: int
    processedTime: float
    userChoice: int = 0
    methodName: str
    clusterId: int = 0


class CleanIndex(BaseModel):
    """Clean index object"""
    ids: List[int]
    project: int


class CleanIndexStrIds(BaseModel):
    """Clean index object that supports string ids"""
    ids: List[str]
    project: int


class SearchLogs(BaseModel):
    """Search logs object"""
    launchId: int
    launchName: str
    itemId: int
    projectId: int
    filteredLaunchIds: List[int]
    logMessages: List[str]
    analyzerConfig: AnalyzerConf = AnalyzerConf()
    logLines: int


class Response(BaseModel):
    """Response object"""
    acknowledged: bool = False
    error: str = ""
    status: int = 0


class LogExceptionResult(BaseModel):
    """Log object with exceptions"""
    logId: int
    foundExceptions: List[str] = []


class BulkResponse(BaseModel):
    """Bulk response object"""
    took: int
    errors: bool
    items: List[str] = []
    logResults: List[LogExceptionResult] = []
    status: int = 0


class SuggestPatternLabel(BaseModel):
    """Suggested pattern with labels"""
    pattern: str
    totalCount: int
    percentTestItemsWithLabel: float = 0.0
    label: str = ""


class SuggestPattern(BaseModel):
    """Suggest pattern object with 2 lists of suggestions"""
    suggestionsWithLabels: List[SuggestPatternLabel] = []
    suggestionsWithoutLabels: List[SuggestPatternLabel] = []


class BatchLogInfo(BaseModel):
    analyzerConfig: AnalyzerConf
    testItemId: int
    log_info: dict
    query_type: str
    project: int
    launchId: int
    launchName: str


class AnalysisCandidate(BaseModel):
    analyzerConfig: AnalyzerConf
    testItemId: int
    timeProcessed: float
    candidates: List[tuple]
    candidatesWithNoDefect: List[tuple]
    project: int
    launchId: int
    launchName: str
