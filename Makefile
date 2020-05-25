.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train-nlu"
	@echo "        train LUNA's nlu models"

train-nlu:
	python3 -m rasa_nlu.train -c config.yml --data data/nlu -o models --fixed_model_name main_nlu --project luna --verbose