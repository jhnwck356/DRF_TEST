from django.test import TestCase
from django.urls import reverse
from TODO.factories import TodoFactory, UserFactory
from TODO.models import Todo
from django.contrib.auth.models import User
from TODO.serializers import TodoSerializer, UserSerializer

#Positives test cases
#---------------------------
class TodoListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.client.force_login(self.user)  # Log in the user
        self.todo = TodoFactory(user=self.user)  # Create a todo instance for the user

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo-list')) 
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # print(response.context)
        # Assert that the todo object is present in the view's context
        self.assertIn('todos', response.context)
        self.assertEqual(list(response.context['todos']), [self.todo])

        # Assert that the template used is 'todo/list_todo.html'
        self.assertTemplateUsed(response, 'todo/list_todo.html')
#-----------------------------
class TodoDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.client.force_login(self.user)  # Log in the user
        self.todo = TodoFactory(user=self.user)  # Create a todo instance for the user

    def test_todo_detail_view(self):
        url = reverse('todo-detail', kwargs={'pk': self.todo.pk})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # Assert that the template used is 'todo/todo_detail.html'
        self.assertTemplateUsed(response, 'todo/todo_detail.html')

        # Assert that the correct todo object is present in the view's context
        self.assertEqual(response.context['object'], self.todo)
# ---------------------------
class TodoCreateViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.client.force_login(self.user)  # Log in the user

    def test_todo_create_view(self):
        url = reverse('todo-create')  # 
        data = {
            'Task_name': 'Test Task',
            'status': 'incomplete',
            'priority': 'high',
            'remaining_days': 5,
            'desc': 'Test description',
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect

        # Assert that a new todo object is created
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()

        # Assert that the todo object has the correct values
        self.assertEqual(todo.Task_name, 'Test Task')
        self.assertEqual(todo.status, 'incomplete')
        self.assertEqual(todo.priority, 'high')
        self.assertEqual(todo.remaining_days, 5)
        self.assertEqual(todo.desc, 'Test description')
        self.assertEqual(todo.user, self.user)
#   ------------------

class TodoupdateViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.client.force_login(self.user)  # Log in the user
        self.todo = TodoFactory(user=self.user)  # Create a todo instance for the user

    def test_todo_update_view(self):
        url = reverse('todo-update', kwargs={'pk': self.todo.pk}) 
        data = {
            'Task_name': 'Updated Task',
            'status': 'Completed',
            'priority': 'low',
            'remaining_days': 2,
            'desc': 'Updated description',
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect

        # Refresh the todo object from the database
        self.todo.refresh_from_db()

        # Assert that the todo object has been updated with the new values
        self.assertEqual(self.todo.Task_name, 'Updated Task')
        self.assertEqual(self.todo.status, 'Completed')
        self.assertEqual(self.todo.priority, 'low')
        self.assertEqual(self.todo.remaining_days, 2)
        self.assertEqual(self.todo.desc, 'Updated description')
        self.assertEqual(self.todo.user, self.user)
        
# ----------------------------
class TodoDeleteViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.client.force_login(self.user)  # Log in the user
        self.todo = TodoFactory(user=self.user)  # Create a todo instance for the user

    def test_todo_delete_view(self):
        url = reverse('todo-delete', kwargs={'pk': self.todo.pk})  
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect

        # Assert that the todo object has been deleted
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())

# ----------------------------
# negative testcases


class TodoListViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory

    def test_todo_list_view_unauthenticated(self):
        url = reverse('todo-list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + url)  # Assert that it redirects to the login page

    def test_todo_list_view_authenticated(self):
        self.client.force_login(self.user)  # Log in the user
        url = reverse('todo-list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # Assert that the template used is 'todo/list_todo.html'
        self.assertTemplateUsed(response, 'todo/list_todo.html')


class TodoDetailViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.todo = TodoFactory()  # Create a todo instance using the factory

    def test_todo_detail_view_unauthenticated(self):
        url = reverse('todo-detail', kwargs={'pk': self.todo.pk})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + url)  # Assert that it redirects to the login page

class TodoCreateViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory

    def test_todo_create_view_unauthenticated(self):
        url = reverse('todo-create')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + url)  # Assert that it redirects to the login page

class TodoupdateViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.todo = TodoFactory()  # Create a todo instance using the factory

    def test_todo_update_view_unauthenticated(self):
        url = reverse('todo-update', kwargs={'pk': self.todo.pk})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + url)  # Assert that it redirects to the login page

class TodoDeleteViewTest1(TestCase):
    def setUp(self):
        self.user = UserFactory()  # Create a user instance using the factory
        self.todo = TodoFactory(user=self.user)  # Create a todo instance for the user

    def test_todo_delete_view_unauthenticated(self):
        url = reverse('todo-delete', kwargs={'pk': self.todo.pk})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + url)  # Assert that it redirects to the login page 

#----------------------------------------------
#serializer
class TodoSerializerTestCase(TestCase):
    def setUp(self):
        self.todo_data = {
            'Task_name': 'Task 1',
            'status': 'Completed',
            'priority': 'High',
            'remaining_days': 3,
            'desc': 'Sample task description',
            'created_at': '2023-07-06T10:00:00Z',
            'updated_at': '2023-07-06T12:00:00Z',
        }
        self.serializer = TodoSerializer(data=self.todo_data)

    def test_todo_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_todo_serializer_invalid(self):
        invalid_data = {
            'Task_name': '',
            'status': 'Completed',
            'priority': 'High',
            'remaining_days': 3,
            'desc': 'Sample task description',
            'created_at': '2023-07-06T10:00:00Z',
            'updated_at': '2023-07-06T12:00:00Z',
        }
        serializer = TodoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.serializer = UserSerializer(data=self.user_data)

    def test_user_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_user_serializer_invalid(self):
        invalid_data = {
            'email': 'invalid_email',
            'username': 'testuser',
            'password': 'testpassword',
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_create_user(self):
        self.assertTrue(self.serializer.is_valid())  # Call is_valid() before accessing validated_data
        user = self.serializer.create(self.serializer.validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])

#     def test_todo_update_view_authenticated(self):
#         self.client.force_login(self.user)  # Log in the user
#         url = reverse('todo-update', kwargs={'pk': self.todo.pk})  
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 403)  # Assert that the response is forbidden