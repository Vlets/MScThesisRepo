from segmentation.visitorSegmentation.pipelineSteps import VisitorSegmentationPipeline

jsonTools = VisitorSegmentationPipeline()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"

# THE ONE FUNCTION TO RULE THEM ALL IS pipeline(filePath)

clusters = jsonTools.segmentation_pipeline(bigData, 26)

