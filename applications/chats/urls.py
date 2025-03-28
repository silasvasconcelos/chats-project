from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet, FileViewSet

# Create the main router
router = DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chat")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"files", FileViewSet, basename="file")

# Combine the URL patterns
urlpatterns = router.urls
