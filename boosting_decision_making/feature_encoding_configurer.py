from boosting_decision_making import feature_encoder


class FeatureEncodingConfigurer:

    def __init__(self):
        self.feature_dict_with_encodings = {}

    def initialize_encoders_from_config(self, config_str):
        self.feature_dict_with_encodings = {}
        for str_part in config_str.split(";"):
            if not str_part.strip():
                continue
            config_parts = str_part.split("|")
            feature_name = int(config_parts[0])
            field_name = config_parts[1]
            encoding_type = config_parts[2]
            max_features = int(config_parts[3])
            ngram_max = int(config_parts[4])
            self.feature_dict_with_encodings[feature_name] = feature_encoder.FeatureEncoder(
                field_name=field_name, encoding_type=encoding_type,
                max_features=max_features, ngram_max=ngram_max)

    def initialize_encoders_from_objects(self, feature_info):
        self.feature_dict_with_encodings = {}
        for feature in feature_info:
            _feature_encoder = feature_encoder.FeatureEncoder()
            self.feature_dict_with_encodings[feature_info] = _feature_encoder.load_from_feature_info(
                feature_info[feature])

    def prepare_encoders(self, data):
        for feature in self.feature_dict_with_encodings:
            self.feature_dict_with_encodings[feature].fit(data)
