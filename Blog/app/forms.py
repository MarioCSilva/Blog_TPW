from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email', "class": "form-control"}))
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control"}))
    password1 = forms.CharField(min_length=5, max_length=50, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-control"}))
    password2 = forms.CharField(min_length=5, max_length=50, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control"}))
    password = forms.CharField(min_length=5, max_length=50, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "password1"]


class PostCreationForm(forms.Form):
    title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={"placeholder": "Title"}))
    image = forms.ImageField(allow_empty_file=True, required=False)
    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "Write your message..."}))


class BlogCreationForm(forms.Form):
    name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={"placeholder": "Name"}))
    isPublic = forms.ChoiceField(choices=[("1", "Public"), ("2", "Private")])
    data = tuple([(x.id, x.name) for x in Topic.objects.all() if x.name != "Personal"])
    topic = forms.TypedMultipleChoiceField(choices=data, required=True)
    description = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"placeholder": "Description"}))
    image = forms.ImageField(allow_empty_file=True, required=False)


class EditProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=70, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=300, required=False)
    profile_pic = forms.ImageField(allow_empty_file=True, required=False)
    birthdate = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1920, 2020)))
    sex = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], required=False)

    class Meta:
        model = Client
        fields = ["name", "description", "birthdate", "profile_pic", "sex"]


class EditBlogOwners(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))


class EditBlogTopics(forms.Form):
    def __init__(self, *args, **kwargs):
        blog_topics = kwargs.pop('blog_topics')
        super(EditBlogTopics, self).__init__(*args, **kwargs)
        topics_unselect = tuple(
            [(x.id, x.name) for x in Topic.objects.all() if x.name != "Personal" and x not in blog_topics.all()])
        topics_select = tuple([(x.id, x.name) for x in blog_topics.all() if x.name != "Personal"])
        self.fields['topics_unselect'] = forms.TypedMultipleChoiceField(choices=topics_unselect, required=False,
                                                                        widget=forms.CheckboxSelectMultiple)
        self.fields['topics_select'] = forms.TypedMultipleChoiceField(choices=topics_select, required=False,
                                                                      widget=forms.CheckboxSelectMultiple)


class EditBlogSubs(forms.Form):
    def __init__(self, *args, **kwargs):
        blog_id = kwargs.pop('blog_id')
        blog_user = kwargs.pop('blog_user')
        blog = Blog.objects.get(id=blog_id)
        super(EditBlogSubs, self).__init__(*args, **kwargs)
        data = tuple([(x.user.id, x.user.username) for x in blog.subs.all() if x.user.username != blog_user])
        self.fields['subs'] = forms.TypedMultipleChoiceField(choices=data, required=False,
                                                             widget=forms.CheckboxSelectMultiple)


class EditBlog(forms.Form):
    def __init__(self, *args, **kwargs):
        blog_name = kwargs.pop('blog_name')
        blog_description = kwargs.pop('blog_description')
        super(EditBlog, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True, max_length=100, initial=blog_name)
        self.fields['description'] = forms.CharField(required=False, max_length=500, initial=blog_description)


class EditBlogInvites(forms.Form):
    def __init__(self, *args, **kwargs):
        blog_id = kwargs.pop('blog_id')
        blog = Blog.objects.get(id=blog_id)
        super(EditBlogInvites, self).__init__(*args, **kwargs)
        data = tuple([(x.id, x.user.username) for x in blog.invites.all()])
        self.fields['invites'] = forms.TypedMultipleChoiceField(choices=data, required=False,
                                                                widget=forms.CheckboxSelectMultiple)


class EditBlogPic(forms.Form):
    blog_pic = forms.ImageField(allow_empty_file=True, required=True)


class FilterPostForm(forms.Form):
    search_post = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'placeholder':'Search...',"class":"rounded-pill"}))
    order_choice_post = forms.ChoiceField(choices=[("recent","Recent"),("likes","Likes"),("comments","Comments")])
    order_by_post  = forms.ChoiceField(choices=[("desc","Descending"),("asc","Ascending")])


class FilterBlogForm(forms.Form):
    search_blog = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'placeholder':'Search...',"class":"form-control", 'size':'60%'}))
    order_choice_blog = forms.ChoiceField(required=False,choices=[("","Order by..."),("subs", "Subs"), ("posts", "Nº of Posts")])
    data = tuple([(x.id,x.name) for x in Topic.objects.all() if x.name!="Personal"])
    topic_choice_blog = forms.TypedMultipleChoiceField(required=False, choices=data)
    order_by_blog = forms.ChoiceField(choices=[("desc","Descending"),("asc","Ascending")])


