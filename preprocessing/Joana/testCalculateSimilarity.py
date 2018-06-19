from preprocessing.dataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs

str1 = "about architecture deployment about deployment about releasenotes about architecture deployment"
str2 = "about development cms development upgrade upgrade upgrade installation upgrade"
str3 = "how-do-i installation tutorial best-practices configuration development how-do-i relevance tutorial development tutorial tutorial"
str4 = "configuration how-do-i integration security configuration how-do-i integration security configuration development how-do-i"

similarities = cs.similarity_results([str1], [str2, str3, str4])