from MasterProject.SimilarityAlgorithms.CalculateSimilarity import CalculateSimilarity as cs

str1 = "about architecture deployment about deployment about releasenotes about architecture deployment"
str2 = "about development cms development upgrade upgrade upgrade installation upgrade"
str3 = "how-do-i installation tutorial best-practices configuration development how-do-i relevance tutorial development tutorial tutorial"
str4 = "configuration how-do-i integration security configuration how-do-i integration security configuration development how-do-i"

web_page_categories1 = "deployment development installation respository"
web_page_categories2 = "cms components configuration deployment"
web_page_categories3 = "components development"
web_page_categories4 = "development deployment components"
web_page_categories5 = "configuration development how-do-i"
web_page_categories6 = "development how-do-i relevance"
web_page_categories7 = "architecture development hst about"

similarities_str = cs.similarity_results([(str1)], [('item2', str2), ('item3', str3), ('item4', str4)])
#similarities_web = cs.similarity_results([web_page_categories1, web_page_categories6], [web_page_categories2,
#                                                                                        web_page_categories3,
#                                                                                        web_page_categories4,
#                                                                                        web_page_categories5,
#                                                                                        web_page_categories7])