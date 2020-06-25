from user_agents import parse

class DataStreamQueue:
    def process_response(self, request, response):
        user_agent = parse(request.request.META['HTTP_USER_AGENT'])
        return response
