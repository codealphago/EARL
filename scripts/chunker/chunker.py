from chunker_models.data_utils import CoNLLDataset
from chunker_models.ner_model import NERModel
from chunker_models.config import Config
"""
class for annnotating NP and VPs
"""
class Annotator:

    def __init__(self):
	config = Config()
    	self.model = NERModel(config)
    	self.model.build()
    	self.model.restore_session(config.dir_model)

    def get_chunks(self,sentence):
	words_raw = sentence.strip().split(" ")
	preds = self.model.predict(words_raw)

	return zip(words_raw, preds)

	
	
	
