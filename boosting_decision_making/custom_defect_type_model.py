"""
* Copyright 2019 EPAM Systems
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""

from boosting_decision_making.defect_type_model import DefectTypeModel
from commons.object_saving.object_saver import ObjectSaver
import os


class CustomDefectTypeModel(DefectTypeModel):

    def __init__(self, app_config, project_id, folder=""):
        self.project_id = project_id
        self.object_saver = ObjectSaver(app_config)
        super(CustomDefectTypeModel, self).__init__(folder=folder)
        self.is_global = False

    def load_model(self, folder):
        self.count_vectorizer_models = self.object_saver.get_project_object(
            self.project_id, os.path.join(folder, "count_vectorizer_models"),
            using_json=False)
        self.models = self.object_saver.get_project_object(
            self.project_id, os.path.join(folder, "models"),
            using_json=False)

    def save_model(self, folder):
        self.object_saver.put_project_object(
            self.count_vectorizer_models,
            self.project_id, os.path.join(folder, "count_vectorizer_models"),
            using_json=False)
        self.object_saver.put_project_object(
            self.models,
            self.project_id, os.path.join(folder, "models"),
            using_json=False)

    def delete_old_model(self):
        all_folders = self.object_saver.get_folder_objects(
            self.project_id, "defect_type_model/")
        old_model_folder = None
        for folder in all_folders:
            if os.path.basename(
                    folder.strip("/").strip("\\")).startswith("defect_type_model"):
                old_model_folder = folder
        if old_model_folder is not None:
            self.object_saver.remove_folder_objects(self.project_id, old_model_folder)
