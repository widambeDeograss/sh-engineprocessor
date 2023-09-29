from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .elasticsearch import ElasticSearchProcessor
from .mongoCrud import MongoDB
from .Trend_Search_Processor import TrendDetection
# Create your views here.

ignorewords = {'the': 1, 'mama': 1, 'this': 1, 'of': 1, 'to': 1, 'and': 1, 'in': 1, 'is': 1, 'it': 1,
               'lakini': 1, 'ingawa': 1, 'ingawaje': 1, 'sababu': 1, 'hadi': 1, 'hata': 1, 'kama': 1,
               'ambapo': 1, 'ambamo': 1,
               'ambako': 1, 'ambacho': 1, 'ambao': 1, 'ambaye': 1, 'ilhali': 1, 'yake': 1,
               'yangu': 1, 'vya': 1, 'vyao': 1, 'vyake': 1, 'vyangu': 1, 'vyenu': 1, 'vyetu': 1,
               'yako': 1, 'yao': 1, 'hizo': 1, 'yenu': 1, 'sisi': 1, 'wewe': 1, 'nyinyi': 1, 'yeye': 1,
               'nao': 1, 'nasi': 1, 'nanyi': 1, 'alikuwa': 1, 'hii': 1, 'hizi': 1,
               'ile': 1, 'hivi': 1, 'za': 1, 'zake': 1, 'zao': 1, 'zenu': 1, 'kwenye': 1,
               'katika': 1, 'kwao': 1, 'kwenu': 1, 'kwetu': 1, 'dhidi': 1, 'kati': 1, 'miongoni': 1,
               'katikati': 1,
               'wakati': 1, 'kabla': 1, 'baada': 1, 'baadaye': 1, 'mbali': 1, 'halafu': 1,
               'hapa': 1, 'yoyote': 1, 'wowote': 1, 'chochote': 1, 'yeyote': 1,
               'lolote': 1,
               'mwenye': 1, 'mwenyewe': 1, 'lenyewe': 1, 'lenye': 1, 'wote': 1, 'lote': 1, 'vyote': 1, 'nyote': 1,
               'zaidi': 1, 'hapana': 1, 'ndiyo': 1, 'au': 1, 'ama': 1, 'sio': 1, 'siye': 1, 'tu': 1,
               'budi': 1, 'nyingi': 1,
               'nyingine': 1, 'wengine': 1, 'mwingine': 1, 'zingine': 1, 'lingine': 1, 'kingine': 1, 'chote': 1,
               'sasa': 1, 'basi': 1, 'bila': 1, 'cha': 1, 'hapo': 1, 'pale': 1, 'kule': 1,
               'humu': 1, 'hivyohivyo': 1, 'vivyo': 1, 'palepale': 1, 'fauka': 1, 'hiyohiyo': 1, 'zile': 1,
               'zilezile': 1, 'hao': 1, 'haohao': 1, 'huku': 1, 'hukuhuku': 1, 'humuhumu': 1, 'huko': 1, 'hukohuko': 1,
               'huo': 1, 'huohuo': 1,
               'hili': 1, 'hilihili': 1, 'ilikuwa': 1, 'karibu': 1, 'kila': 1, 'kima': 1,
               'kutoka': 1, 'kwenda': 1, 'kubwa': 1, 'ndogo': 1, 'kwamba': 1, 'kuwa': 1, 'lao': 1, 'lo': 1,
               'mara': 1, 'na': 1, 'mdogo': 1,
               'mkubwa': 1, 'ng’o': 1, 'pia': 1, 'aidha': 1, 'vilevile': 1, 'kadhalika': 1,
               'halikadhalika': 1, 'ni': 1, 'sana': 1, 'pamoja': 1, 'tafadhali': 1, 'tena': 1, 'wake': 1,
               'wao': 1, 'yule': 1, 'wale': 1,
               'zangu': 1, 'nje': 1, 'afanaleki': 1, 'salale': 1, 'yupi': 1, 'ipi': 1, 'lipi': 1, 'ngapi': 1,
               'yetu': 1, 'si': 1, 'angali': 1, 'wangali': 1, 'loo': 1, 'la': 1, 'ohoo': 1, 'barabara': 1, 'oyee': 1,
               'ewaa': 1, 'walahi': 1,
               'masalale': 1, 'duu': 1, 'toba': 1, 'mh': 1, 'kumbe': 1, 'ala': 1, 'ebo': 1, 'haraka': 1, 'pole': 1,
               'polepole': 1, 'harakaharaka': 1, 'hiyo': 1, 'vyovyote': 1, 'atakuwa': 1, 'itakuwa': 1,
               'mtakuwa': 1, 'tutakuwa': 1,
               'labda': 1, 'yumkini': 1, 'haiyumkini': 1, 'yapata': 1, 'takribani': 1, 'hususani': 1, 'yawezekana': 1,
               'nani': 1, 'juu': 1, 'chini': 1, 'ndani': 1, 'baadhi': 1, 'kuliko': 1, 'vile': 1, 'mwa': 1, 'kwa': 1,
               'hasha': 1, 'hivyo': 1,
               'moja': 1, 'kisha': 1, 'pili': 1, 'kwanza': 1, 'ili': 1, 'je': 1, 'jinsi': 1, 'ila': 1, 'a': 1, 'b': 1,
               'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'wa': 1, 'ya': 1, 'nini': 1, 'hasa': 1,
               'huu': 1, 'zako': 1, 'mimi': 1, 'akasema': 1, 'alisema': 1, }


class WebSearchProcessor(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        query_data = request.data['search_query']
        query_data_list = query_data.split()
        for word in query_data_list:
            if word in ignorewords:
                query_data_list.remove(word)
        search_term = " ".join(tuple(query_data_list))
        elastic_search_obj = ElasticSearchProcessor()
        mongo_search_obj = MongoDB()
        m_query_results = mongo_search_obj.get_contents('spider_web_page', search_term)
        m_query_images = mongo_search_obj.get_image('page_images', search_term)
        query_results = elastic_search_obj.search_page_keywords('page_images', search_term, 15)
        date = request.random_date
        print(query_results)
        # if query_results:
        #     response = {
        #         'status': 'success',
        #         'code': status.HTTP_200_OK,
        #         'query_search_results': m_query_results,
        #         'query_search_related_images':query_results
        #     }
        #     return Response(response)

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'query_search_results': m_query_results,
            'query_search_related_images': m_query_images,
            'reference_date': date
        }
        return Response(response)
#
# {
# "search_query": "query"
# }


class TrendAnalyser(APIView):

    @staticmethod
    def post(request):
        data = request.data['trend_query']
        mydata = data.replace('_', ' ')
        data_to_list = mydata.split()
        keywords = data_to_list
        timeSelection = 2
        sFilter = ''
        trenddata = TrendDetection(
            kw_list=keywords,
            selection=timeSelection,
            gprop=sFilter
        )
        path = trenddata.relative_comparison()
        region = trenddata.int_per_reg()
        # yearTrend = trenddata.yearly_topCharts(2023)
        related_queries = trenddata.rel_queries()
        # print(yearTrend)
        context = {
            'graphpath': path,
            'regions': region,
            'related_queries': related_queries
        }
        print(context)
        return Response(context)
#
# {
# "trend_query":"yanga_zuchu"
# }