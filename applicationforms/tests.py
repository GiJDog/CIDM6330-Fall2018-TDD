from applicationforms.models import ApplicationFormItem, ApplicationForm
from django.test import TestCase

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ApplicationFormViewTest(TestCase):

    def test_uses_applicationform_template(self):
        applicationform_ = ApplicationForm.objects.create()
        response = self.client.get(f'/applicationforms/{applicationform_.id}/')
        self.assertTemplateUsed(response, 'applicationform.html')


    def test_displays_only_items_for_that_applicationform(self):
        correct_applicationform = ApplicationForm.objects.create()
        ApplicationFormItem.objects.create(text='itemey 1', applicationform=correct_applicationform)
        ApplicationFormItem.objects.create(text='itemey 2', applicationform=correct_applicationform)
        other_applicationform = ApplicationForm.objects.create()
        ApplicationFormItem.objects.create(text='other applicationform item 1', applicationform=other_applicationform)
        ApplicationFormtem.objects.create(text='other applicationform item 2', applicationform=other_applicationform)

        response = self.client.get(f'/applicationforms/{correct_applicationform.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other applicationform item 1')
        self.assertNotContains(response, 'other applicationform item 2')

    def test_passes_correct_applicationform_to_template(self):
        other_applicationform = ApplicationForm.objects.create()
        correct_applicationform = ApplicationForm.objects.create()
        response = self.client.get(f'/applicationforms/{correct_applicationform.id}/')
        self.assertEqual(response.context['applicationform'], correct_applicationform)

class ApplicationFormAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        applicationform_ = ApplicationForm()
        applicationform_.save()

        first_item = ApplicationFormItem()
        first_item.text = 'The first (ever) applicationform item'
        first_item.applicationform = applicationform_
        first_item.save()

        second_item = ApplicationFormItem()
        second_item.text = 'Item the second'
        second_item.applicationform = applicationform_
        second_item.save()

        saved_applicationform = ApplicationForm.objects.first()
        self.assertEqual(saved_applicationform, applicationform_)

        saved_items = ApplicationFormItem.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) applicationform item')

        self.assertEqual(first_saved_item.applicationform, applicationform_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.applicationform, applicationform_)

class NewApplicationFormTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/applicationforms/new', data={'item_text': 'A new applicationform item'})
        self.assertEqual(ApplicationFormItem.objects.count(), 1)
        new_item = ApplicationFormItem.objects.first()
        self.assertEqual(new_item.text, 'A new applicationform item')


    def test_redirects_after_POST(self):
        response = self.client.post('/applicationforms/new', data={'item_text': 'A new applicationform item'})
        new_applicationform = ApplicationForm.objects.first()
        self.assertRedirects(response, f'/applicationforms/{new_applicationform.id}/')

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_applicationform(self):
        other_applicationform = ApplicationForm.objects.create()
        correct_applicationform = ApplicationForm.objects.create()

        self.client.post(
            f'/applicationforms/{correct_applicationform.id}/add_item',
            data={'item_text': 'A new item for an existing applicationform'}
        )

        self.assertEqual(ApplicationFormItem.objects.count(), 1)
        new_item = ApplicationFormItem.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing applicationform')
        self.assertEqual(new_item.applicationform, correct_applicationform)


    def test_redirects_to_applicationform_view(self):
        other_applicationform = ApplicationForm.objects.create()
        correct_applicationform = ApplicationForm.objects.create()

        response = self.client.post(
            f'/applicationforms/{correct_applicationform.id}/add_item',
            data={'item_text': 'A new item for an existing applicationform'}
        )

        self.assertRedirects(response, f'/applicationforms/{correct_applicationform.id}/')
# Create your tests here testds.
