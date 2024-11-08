from rest_framework.pagination import PageNumberPagination

class BlogPostPagination(PageNumberPagination):
    page_size = 2  # Set the page size for blog posts

class BlogCommentPagination(PageNumberPagination):
    page_size = 2  # Set the page size for comments
