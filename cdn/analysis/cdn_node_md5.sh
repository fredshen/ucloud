#!/bin/bash
#####################################################################################################
#                                                                                                   #
# Author: F.Shen                                                                                    #
# Version: 1.1                                                                                      #
# Release Date: 02/02/2021                                                                          #
# Features:                                                                                         #
# 1.Sort URLs in the original log                                                                   #
# 2.Sort the top three URLs by IP                                                                   #
# Export:                                                                                           #
# a/Original log<initial.log>, b/URL sorting log<url_sort_top20.log>,                               #
# c/IP sorting of the top three URLs <top3url_ip_sort_top20.log>,                                   #
#                                                                                                   #
# ** Let me know if there're any BUGs | fred.shen@ucloud.cn                                         #
#                                                                                                   #
#####################################################################################################

#####################################################################################################
# ------------Release Note------------                                                              #
# Version:1.0                                                                                       #
# 1.Sort URLs in the original log                                                                   #
# 2.Sort the top three URLs by IP                                                                   #
# Export:                                                                                           #
# a/Original log<initial.log>, b/URL sorting log<url_sort_top20.log>,                               #
# c/IP sorting of the top three URLs <top3url_ip_sort_top20.log>,                                   #
#                                                                                                   #
# Version:1.1                                                                                       #
# 1.Added Progress and Notifications functions                                                      #
# 2.Changed Full sort to Sorted top 20                                                              #
# 3.Added Time stamp and Task overview                                                              #
#                                                                                                   #
#####################################################################################################
