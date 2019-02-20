from django.test import TestCase
from materials.models import Item, ItemClass, ItemImages, Genre, Attribute, \
    AttributeValue, Icon, Group, ItemImages, ItemAttributeRelationship
from django.contrib.auth.models import User


class ItemTestCase(TestCase):

    def setUp(self):
        group = Group.objects.create(title="group-1", slug='group-1')
        user = User.objects.create(username='user-1')
        Item.objects.create(
            title='item-1',
            tags=['tag-1', 'tag-2'],
            creator=user,
            main_group=group,
            slug='item-1')

    def test_get_absolute_url(self):
        """Correct link creation."""
        item = Item.objects.get(title="item-1")
        self.assertEqual(item.get_absolute_url(),
                         '/materials/item/group-1/item-1/')

    def test_get_play_url(self):
        """Proper creation of links to view PlayVideo."""
        item = Item.objects.get(title="item-1")
        self.assertEqual(item.get_play_url(),
                         '/materials/play_video/group-1/item-1/')

    def test_genres_to_string(self):
        """Correct creation of a string of genres through a separator."""
        item = Item.objects.get(title="item-1")
        item.genres.create(title='genre-1')
        item.genres.create(title='genre-2')
        item.save()
        self.assertEqual(item.genres_to_string(), 'genre-1, genre-2')


class GroupTestCase(TestCase):

    def setUp(self):
        Group.objects.create(title="group-1", slug='group-1')

    def test_get_absolute_url(self):
        """Correct link creation."""
        group = Group.objects.get(title="group-1")
        self.assertEqual(group.get_absolute_url(), '/materials/group/group-1/')

    def test_slug_to_string(self):
        """Correct creation of a string of slug parents."""
        group = Group.objects.get(title="group-1")
        group.parent = Group.objects.create(title="group", slug='group')
        group.save()
        self.assertEqual(group.slug_to_string(), 'group/group-1')

    def test_get_tree_group(self):
        """Correct creation of a list of parents."""
        group = Group.objects.get(title="group-1")
        group_3 = Group.objects.create(title="group-3", slug='group-3')
        group_2 = Group.objects.create(title="group-2", slug='group-2')
        group_2.parent = group_3
        group_2.save()
        group.parent = group_2
        group.save()
        self.assertListEqual(
            list(group.get_tree_group([])), [group_3, group_2])
