from math import sqrt
from pytrends.request import TrendReq
from time import sleep  # be nice
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd


# search trend in a given population
# def zscore(obs, pop):
#     # Size of population.
#     number = float(len(pop))
#     # Average population value.
#     avg = sum(pop) / number
#     # Standard deviation of population.
#     std = sqrt(sum(((c - avg) ** 2) for c in pop) / number)
#     # Zscore Calculation.
#     return (obs - avg) / std
#
#
# # pop = average number of searches of different days & obs = current number of searches
# print(f'{zscore(9, [1, 1, 1, 1, 9, 9, 9, 9]):.5f}')

class FazScore:
    def __init__(self, decay, pop=None):
        if pop is None:
            pop = []
        self.sqrAvg = self.avg = 0
        # The rate at which the historic dat'score effect will diminish.
        self.decay = decay
        for x in pop:
            self.update(x)

    def update(self, value):
        # Set initial averages to the first value in the sequence.
        if self.avg == 0 and self.sqrAvg == 0:
            self.avg = float(value)
            self.sqrAvg = float((value ** 2))
        # Calculate the average of the rest of the values using a
        # floating average.
        else:
            self.avg = self.avg * self.decay + value * (1 - self.decay)
            self.sqrAvg = self.sqrAvg * self.decay + (value ** 2) * (1 - self.decay)
        return self

    def std(self):
        # Somewhat ad-hoc standard deviation calculation.
        return sqrt(self.sqrAvg - self.avg ** 2)

    def score(self, obs):
        if self.std() == 0:
            return obs - self.avg
        else:
            return (obs - self.avg) / self.std()


# score = FazScore(0.8, [5, 9, 13, 17, 21, 25]).score(29)
# print(score)

"""
for more info about the algo
"""


# https://stackoverflow.com/questions/787496/what-is-the-best-way-to-compute-trending-topics-or-tags
# https://www.isixsigma.com/tools-templates/statistical-analysis/improved-forecasting-moving-averages-and-z-scores/
# https://www.investopedia.com/terms/z/zscore.asp
# https://moz.com/blog/reddit-stumbleupon-delicious-and-hacker-news-algorithms-exposed


# using pytrend google api
class TrendDetection:
    def __init__(self, kw_list, selection, gprop):
        self.pytrend = TrendReq(hl='en-US', timeout=(10, 25), retries=2, backoff_factor=0.1)
        self.kw_list = kw_list # for kw in kw_list:
        #     print(kw + ' top queries:')
        #     if data[kw]['top'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['top'].head(5))
        #     print('')
        #     print('\n' + kw + ' rising queries:')
        #     if data[kw]['rising'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['rising'].head(5))
        #     print('')= kw_list
        self.keyword = []
        self.selection = int(selection)
        self.gprop = gprop
        self.cat = '0'
        self.geo = 'TZ'
        self.timeframes = ['all', 'today 5-y', 'today 12-m', 'today 3-m', 'today 1-m',
                           'now 7-d', 'now 4-H', '2022-04-01 2022-04-30']

    def execute_check_trends(self):
        for word in self.kw_list:
            self.keyword.append(word)
            self.check_trends()
            sleep(10)
            self.keyword.pop()

    # Get realtime Google Trends data
    def check_trends(self):
        self.pytrend.build_payload(
            self.keyword,
            self.cat,  # all categories
            timeframe=self.timeframes[self.selection],
            geo=self.geo,
            gprop=self.gprop  # can be images, news, YouTube or froogle (for Google Shopping results)
        )

        sleep(10)
        data = self.pytrend.interest_over_time()
        print(data)
        # mean = round(dat.mean(), 2)
        # avg = round(data[word][-52:].mean(), 2)  # the previous year from the present day
        # avg2 = round(data[word][:52].mean(), 2)  # Yearly average 5 years ago.
        # trend = round(((avg / mean[word]) - 1) * 100, 2)
        # trend2 = round(((avg / avg2) - 1) * 100, 2)
        # print('The average 5 years interest on ' + word + ' is ' + str(mean[word]) + '%.')
        # print('For the previous year, the interest on ' + word + ' has changed by ' + str(
        #     trend) + '% in comparison to the interest in the last 5 years.')
        # print('')
        #
        # # Stable trend
        # if mean[word] > 75 and abs(trend) <= 5:
        #     print('The interest for ' + word + ' is stable in the last 5 years.')
        # elif mean[word] > 75 and trend > 5:
        #     print('The interest for ' + word + ' is stable and increasing in the last 5 years.')
        # elif mean[word] > 75 and trend < -5:
        #     print('The interest for ' + word + ' is stable and decreasing in the last 5 years.')
        #
        # # Relatively stable
        # elif mean[word] > 60 and abs(trend) <= 15:
        #     print('The interest for ' + word + ' is relatively stable in the last 5 years.')
        # elif mean[word] > 60 and trend > 15:
        #     print('The interest for ' + word + ' is relatively stable and increasing in the last 5 years.')
        # elif mean[word] > 60 and trend < -15:
        #     print('The interest for ' + word + ' is relatively stable and decreasing in the last 5 years.')
        #
        # # Seasonal
        # elif mean[word] > 20 and abs(trend) <= 15:
        #     print('The interest for ' + word + ' is seasonal.')
        #
        # # New keyword
        # elif mean[word] > 20 and trend > 15:
        #     print(word + ' is trending.')
        #
        # # Declining keyword
        # elif mean[word] > 20 and trend < -15:
        #     print('The interest for ' + word + ' is significantly decreasing.')
        #
        # # Cyclical
        # elif mean[word] > 5 and abs(trend) <= 15:
        #     print('The interest for ' + word + ' is cyclical.')
        #
        # # New
        # elif mean[word] > 0 and trend > 15:
        #     print(word + ' is new and trending.')
        #
        # # Declining
        # elif mean[word] > 0 and trend < -15:
        #     print('The interest for ' + word + ' is declining and not comparable to its peak.')
        #
        # # Other
        # else:
        #     print('This is something to be checked.')
        #
        # # Comparison last year vs. 5 years ago
        # if avg2 == 0:
        #     print('This didn\'t exist 5 years ago.')
        # elif trend2 > 15:
        #     print('The last year interest is quite higher compared to 5 years ago.'
        #           + ' It has increased by ' + str(trend2) + '% when comparing the two years')
        # elif trend2 < -15:
        #     print('The last year interest is quite lower compared to 5 years ago.'
        #           + ' It has decreased by ' + str(trend2) + '% when comparing the two years')
        # else:
        #     print('The last year interest is comparable to 5 years ago. '
        #           + ' It has changed by ' + str(trend2) + '% when comparing the two years')
        #
        # print('')

    def relative_comparison(self):
        plt.figure(figsize=(10, 8))
        x_pos = np.arange(len(self.kw_list))

        # Last 5-years
        self.pytrend.build_payload(
            self.kw_list,
            self.cat,  # all categories
            timeframe=self.timeframes[1],  # check how to automate this!!!
            geo=self.geo,
            gprop=self.gprop  # can be images, news, YouTube or froogle (for Google Shopping results)
        )

        sleep(10)
        data = self.pytrend.interest_over_time()
        mean = data.mean()
        mean = round(mean / mean.max() * 100, 2)
        jObj = data.to_json()
        # df = pd.read_json(jObj)
        # print(df)
        # print('For last 5 years', jObj)
        ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=1, colspan=1)
        ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=1, colspan=1)
        for kw in self.kw_list:
            ax1.plot(data[kw], label=kw)
        ax2.bar(x_pos, mean[0:len(self.kw_list)], align='center')
        plt.xticks(x_pos, self.kw_list)
        #
        # Last 12-months
        self.pytrend.build_payload(
            self.kw_list,
            self.cat,  # all categories
            timeframe=self.timeframes[2],
            geo=self.geo,
            gprop=self.gprop  # can be images, news, YouTube or froogle (for Google Shopping results)
        )

        sleep(5)
        data = self.pytrend.interest_over_time()
        mean = data.mean()
        mean = round(mean / mean.max() * 100, 2)
        jObj = data.to_json()
        # df = pd.read_json(jObj)
        # print(df)
        # print('For the last 12 months', jObj)
        ax3 = plt.subplot2grid((3, 2), (1, 0), rowspan=1, colspan=1)
        ax4 = plt.subplot2grid((3, 2), (1, 1), rowspan=1, colspan=1)
        for kw in self.kw_list:
            ax3.plot(data[kw], label=kw)
        ax4.bar(x_pos, mean[0:len(self.kw_list)], align='center')
        plt.xticks(x_pos, self.kw_list)
        #
        # Last 3-months
        self.pytrend.build_payload(
            self.kw_list,
            self.cat,  # all categories
            timeframe=self.timeframes[3],
            geo=self.geo,
            gprop=self.gprop  # can be images, news, YouTube or froogle (for Google Shopping results)
        )

        sleep(5)
        data = self.pytrend.interest_over_time()
        mean = data.mean()
        mean = round(mean / mean.max() * 100, 2)
        jObj = data.to_json()
        # df = pd.read_json(jObj)
        # print(df)
        # print('For the last 3 months', jObj)
        ax5 = plt.subplot2grid((3, 2), (2, 0), rowspan=1, colspan=1)
        ax6 = plt.subplot2grid((3, 2), (2, 1), rowspan=1, colspan=1)
        for kw in self.kw_list:
            ax5.plot(data[kw], label=kw)
        # print(mean)
        ax6.bar(x_pos, mean[0:len(self.kw_list)], align='center')
        plt.xticks(x_pos, self.kw_list)

        ax1.set_ylabel('Last 5 years')
        ax3.set_ylabel('Last year')
        ax5.set_ylabel('Last 3 months')
        ax1.set_title('Relative interest over time', fontsize=14)
        ax2.set_title('Relative interest for the period', fontsize=14)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
        ax5.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        ax1.legend(loc='upper left')
        ax3.legend(loc='upper left')
        ax5.legend(loc='upper left')
        plt.savefig(f'/home/egovridc/Documents/Search Engine(spider web)/spider_web_back_ens/spider_web_backend/spiderweb/TrendGraphs/{self.kw_list[0]}.png', orientation='landscape')

        # return data.reset_index().to_json(orient='records')
        return data
        # f'/home/egovridc/Documents/Search Engine(spider web
        # )/spider_web_back_ens/spider_web_backend/spiderweb/TrendGraphs/{self.kw_list[0]}.png'
    # Interest per region
    def int_per_reg(self):
        self.pytrend.build_payload(self.kw_list,
                                   self.cat,
                                   self.timeframes[self.selection],
                                   self.geo,
                                   self.gprop)

        data = self.pytrend.interest_by_region(resolution='COUNTRY',  # can be by 'CITY', 'COUNTRY', 'DMA', 'REGION'
                                               inc_low_vol=True,
                                               inc_geo_code=True)
        # return data
        return data.reset_index().to_json(orient='records')
        # for kw in kw_list:
        #     print(kw)
        #     data = data.sort_values(by=kw, ascending=False)
        #     print(data.head())
        #     print('')

    # Related queries summary
    def rel_queries(self):
        # Last 3-months related queries
        self.pytrend.build_payload(self.kw_list,
                                   self.cat,
                                   self.timeframes[3],  # also automate this
                                   self.geo,
                                   self.gprop)

        three_month_data = self.pytrend.related_queries()
        print('################   LAST 3 MONTHS RELATED QUERIES.   ################')
        print(three_month_data)
        # for kw in kw_list:
        #     print(kw + ' top queries:')
        #     if data[kw]['top'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['top'].head(5))
        #     print('')
        #     print('\n' + kw + ' rising queries:')
        #     if data[kw]['rising'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['rising'].head(5))
        #     print('')

        # Last month related queries
        self.pytrend.build_payload(self.kw_list,
                                   self.cat,
                                   self.timeframes[4],  # don't forget this is supposed to be automated
                                   self.geo,
                                   self.gprop)

        sleep(5)
        data = self.pytrend.related_queries()
        print('################   LAST MONTH RELATED QUERIES   ################')

        related_queries = {
            "last_three_month": three_month_data,
            "last_month": data
        }
        print(data)
        return related_queries
        # for kw in kw_list:
        #     print(kw + ' top queries:')
        #     if data[kw]['top'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['top'].head(5))
        #     print('')
        #     print('\n' + kw + ' rising queries:')
        #     if data[kw]['rising'] is None:
        #         print('There isn\'t enough data.')
        #     else:
        #         print(data[kw]['rising'].head(5))
        #     print('')

    def yearly_topCharts(self, year):  # needs automation
        trend = self.pytrend.top_charts(year, hl='en-US', tz=300, geo='GLOBAL')  # pytrend.suggestions('tanzania')
        # print(trend)
        return trend.to_json()