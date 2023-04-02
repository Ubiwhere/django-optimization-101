from .views import Ex1Viewset, Ex2Viewset, Ex3Viewset, Ex4Viewset, Ex5Viewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register("ex1/database-vs-python-operations", Ex1Viewset)
router.register("ex2/queryset-optimization/prefetch-related", Ex2Viewset)
router.register("ex3/queryset-optimization/select-related", Ex3Viewset)
router.register("ex4/queryset-optimization/advanced-prefetch", Ex4Viewset)
router.register("ex5/caching", Ex5Viewset)

urlpatterns = router.urls
