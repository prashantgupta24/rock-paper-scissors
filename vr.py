from __future__ import print_function

import json

from ibm_watson import ApiException, VisualRecognitionV3

# If service instance provides IAM API key authentication
service = VisualRecognitionV3('2018-03-19')

# classifiers = service.list_classifiers().get_result()
# print(json.dumps(classifiers, indent=2))


def classifyImage(image_file, threshold='0.6'):
    with open(image_file, 'rb') as image_file:
        results = service.classify(
            images_file=image_file,
            threshold=threshold,
            classifier_ids=['DefaultCustomModel_981890366']).get_result()
        #print(json.dumps(results, indent=2))
        classes = results["images"][0]["classifiers"][0]["classes"]
        return classes
