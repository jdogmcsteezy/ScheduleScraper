from BCScheduleCreator import ConvertMilitaryToStd, PrintClass, DoesClassMeet, CreateClassesList
import json

#print(type(data))

print(CreateClassesList('MC', 'Spring 2018', 'Main Campus', 'subjectsIn_MC.txt'))

# with open('testJSON.json') as file:
#     data = json.loads(file.read())



# ------ Here is an example of how to grab info from web and dump it into a json file ------
# with open('subjectsIn_MC.txt') as file:
#     subjectsMC = [subject.strip() for subject in file.readlines()]
#     classes = []
# for subject in subjectsMC:
#     print(subject)
#     data = GrabClassData('Spring 2018', 'Main Campus', subject)
#     ParseHTMLtoJSON(data, classes, 'MC')

# with open('testJSON.json','w') as file:
#     json.dump(classes, file)
