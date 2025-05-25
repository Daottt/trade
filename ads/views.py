from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad, ExchangeProposal
from ads.serializers import AdSerializer, ProposalSerializer
from ads.permissions import IsAdOwnerOrReadOnly, IsExchangeOwnerOrReadOnly

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["category", "condition"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsExchangeOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["ad_sender", "ad_sender", "status"]
