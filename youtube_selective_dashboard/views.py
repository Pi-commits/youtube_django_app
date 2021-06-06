import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .tasks import youtube_background_calls
from .models import YoutubeFeed
from django.core.paginator import Paginator
from background_task.models import Task
from django.urls import reverse


class Index(APIView):

    def get(self, request):
        '''
            A Get API to get all the stored youtube feed in paginated and reversed published time order
        :param request:
        :return:
        '''

        page_number = self.request.GET.get('page_number', 1)
        page_number = int(page_number)

        # Clean background task table and start new background process
        clean_task_and_call()

        youtube_feed_ins = YoutubeFeed.objects.all().order_by('-published_at').values()
        if youtube_feed_ins.count() > 0:
            paged_data = Paginator(youtube_feed_ins, settings.PAGINATOR_SIZE)
            max_page = paged_data.page_range[-1]
            if page_number in paged_data.page_range:
                current_page = paged_data.get_page(page_number)
                current_page_number = page_number
            else:
                current_page = paged_data.get_page(paged_data.page_range[-1])
                current_page_number = paged_data.page_range[-1]

            data = {
                'prev_link': (request.build_absolute_uri(reverse('index', )) + '?page_number=' + str(page_number - 1)) if current_page_number > 1 else '',
                'next_link': (request.build_absolute_uri(reverse('index', )) + '?page_number=' + str(page_number + 1)) if current_page_number < max_page else '',
                'total_result_count': len(list(current_page)),
                'Feed': list(current_page)
            }

            return Response(data)

        data = {
            'message': "Data Not Found!"
        }
        return Response(data)


def clean_task_and_call():
    # Call background task for calling Youtube API
    Task.objects.all().delete()
    youtube_background_calls(repeat=settings.REPEAT_FREQUENCY)


class SearchApi(APIView):

    def get(self, request):

        '''
            A Get API to search the saved feeds according to title and description
        :param request:
        :return:
        '''

        title = self.request.GET.get('title', '')
        description = self.request.GET.get('description', '')
        page_number = self.request.GET.get('page_number', 1)
        page_number = int(page_number)

        if not title and not description:
            data = {
                'message': "Provide at least one parameter"
            }
            return Response(data)

        youtube_feed_ins = YoutubeFeed.objects.filter(title__icontains=title if title is not None else '', description__icontains=description if description is not None else '').order_by('-published_at').values()
        if youtube_feed_ins.count() > 0:
            paged_data = Paginator(youtube_feed_ins, settings.PAGINATOR_SIZE)
            max_page = paged_data.page_range[-1]
            if page_number in paged_data.page_range:
                current_page = paged_data.get_page(page_number)
                current_page_number = page_number
            else:
                current_page = paged_data.get_page(paged_data.page_range[-1])
                current_page_number = paged_data.page_range[-1]

            data = {
                'prev_link': (request.build_absolute_uri(reverse('search_api', )) + '?title=' + title + '&description=' + description + '&page_number=' + str(page_number - 1)) if current_page_number > 1 else '',
                'next_link': (request.build_absolute_uri(reverse('search_api', )) + '?title=' + title + '&description=' + description + '&page_number=' + str(page_number + 1)) if current_page_number < max_page else '',
                'total_result_count':len(list(current_page)),
                'Feed': list(current_page)
            }

            return Response(data)


