from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password456')

        self.ad1 = Ad.objects.create(user=self.user1, title='Ad 1', description='Description 1',
                                     category=Ad.AdCategory.ELECTRONICS, condition=Ad.ProductStatus.New)
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad 2', description='Description 2',
                                     category=Ad.AdCategory.CLOTHING, condition=Ad.ProductStatus.Used)
        self.ad3 = Ad.objects.create(user=self.user1, title='Ad 3', description='Description 3',
                                     category=Ad.AdCategory.FURNITURE, condition=Ad.ProductStatus.New)

        self.list_url = reverse('ad-list')

    def test_list_ads(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_create_ad_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'New Ad', 'description': 'New Description', 'category': Ad.AdCategory.OTHER,
                'condition': Ad.ProductStatus.New}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 4)
        self.assertEqual(Ad.objects.last().user, self.user1)

    def test_create_ad_unauthenticated(self):
        data = {'title': 'New Ad', 'description': 'New Description', 'category': Ad.AdCategory.OTHER,
                'condition': Ad.ProductStatus.New}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ad_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('ad-detail', args=[self.ad1.pk])
        data = {'title': 'Updated Ad Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Updated Ad Title')

    def test_update_ad_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('ad-detail', args=[self.ad1.pk])
        data = {'title': 'Updated Ad Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_ads(self):
        url = self.list_url + f'?category={Ad.AdCategory.ELECTRONICS}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_delete_ad_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('ad-detail', args=[self.ad1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ad.objects.count(), 3)

    def test_delete_ad_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('ad-detail', args=[self.ad1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 2)

class ExchangeAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password456')

        self.ad1 = Ad.objects.create(user=self.user1, title='Ad 1', description='Description 1')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad 2', description='Description 2')
        self.ad3 = Ad.objects.create(user=self.user1, title='Ad 3', description='Description 3')

        self.proposal1 = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Proposal 1')
        self.proposal2 = ExchangeProposal.objects.create(ad_sender=self.ad2, ad_receiver=self.ad3, comment='Proposal 2',
                                                         status=ExchangeProposal.ExchangeStatus.ACCEPTED)

        self.list_url = reverse('exchangeproposal-list')

    def test_list_proposals(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_create_proposal_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {'ad_sender': self.ad1.pk, 'ad_receiver': self.ad2.pk, 'comment': 'New Proposal'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 3)
        self.assertEqual(ExchangeProposal.objects.last().ad_sender, self.ad1)

    def test_create_proposal_unauthenticated(self):
        data = {'ad_sender': self.ad1.pk, 'ad_receiver': self.ad2.pk, 'comment': 'New Proposal'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_proposal_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('exchangeproposal-detail', args=[self.proposal1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_filter_proposals(self):
        self.client.force_authenticate(user=self.user1)
        url = self.list_url + f'?ad_sender={self.ad1.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_validation_same_user(self):
        self.client.force_authenticate(user=self.user1)
        data = {'ad_sender': self.ad1.pk, 'ad_receiver': self.ad3.pk, 'comment': 'Invalid Proposal'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validation_wrong_sender(self):
        self.client.force_authenticate(user=self.user2)
        data = {'ad_sender': self.ad1.pk, 'ad_receiver': self.ad2.pk, 'comment': 'Invalid Proposal'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
