import random

from flask import jsonify, request
from flask_cors import cross_origin
from app import app
from app.algorithm.ml import ml
from app.info import features, questions, answers, questionWithComplete

@app.route('/api/questions/', methods = ['POST'])
@cross_origin()
def getQuestions():
    availableFeatures = features[:]
    characterMatch = None

    if 'alreadyFeatures' in request.json:
        availableFeatures = set(availableFeatures) - set(request.json['alreadyFeatures'])
        availableFeatures = list(availableFeatures)

        featuresThatCharacterIsTrue = []

        characterMatch = ml(request.json['alreadyFeatures'], request.json['params'], request.json['answers'])
        characterMatch = characterMatch.to_dict()

        characterMatchId = 0
        for id in characterMatch['name']:
            characterMatchId = id

        for i in range(len(availableFeatures)):
            availableFeature = availableFeatures[i]
            if(characterMatch[availableFeature][characterMatchId]):
                featuresThatCharacterIsTrue.append(availableFeature)
        
        if(len(featuresThatCharacterIsTrue)):
            availableFeatures = featuresThatCharacterIsTrue

        characterMatch = {
          "name": characterMatch['name'][characterMatchId],
          "image": characterMatch['image'][characterMatchId],
        }

    if(not len(availableFeatures)):
        return jsonify(
            characterMatch = characterMatch
        )

    feature = random.choice(availableFeatures)
    param = feature
    question = questions[feature]

    return jsonify(
      feature = feature,
      param = param,
      question = question,
      answers = answers[feature],
      characterMatch = characterMatch
    )