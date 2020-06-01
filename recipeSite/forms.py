from django import forms
from .models import Post, Ingredients, Instructions
from users.models import Favorites

class favoriteForm(forms.ModelForm):
    post = forms.IntegerField(required=False)
    class Meta:
        model = Favorites
        fields = ['post']

class postCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=60, required=True)
    description = forms.CharField(max_length=150)
    picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generateFields(Ingredients.objects.filter(post=self.instance), Instructions.objects.filter(post=self.instance))

    class Meta:
        model = Post
        fields = ['title', 'description', 'picture']

    def clean(self):
        ingredients = []
        i = 0
        field_name = f'ingredients{i}'
        duplicate = False
        duplicateFieldName = set()
        while self.data.get(field_name):
            ingredient = self.data[field_name]
            if ingredient in ingredients:
                duplicateFieldName.add(field_name)
                duplicate = True
            ingredients.append(ingredient)
            i += 1
            field_name = f'ingredients{i}'
        self.cleaned_data["ingredients"] = ingredients
        instructions = []
        i = 0
        field_name = f'instructions{i}'
        while self.data.get(field_name):
            instruction = self.data[field_name]
            if instruction in instructions:
                duplicateFieldName.add(field_name)
                duplicateFieldName.add(list(self.data.keys())[list(self.data.values()).index(instruction)])
                duplicate = True
            instructions.append(instruction)
            i += 1
            field_name = f'instructions{i}'
        self.cleaned_data["instructions"] = instructions
        # self.cleaned_data['picture']
        print (self.cleaned_data, self.data)
        if duplicate:
            self.generateFields(self.cleaned_data["ingredients"], self.cleaned_data["instructions"])
            print(duplicateFieldName)
            for field in duplicateFieldName:
                if field.find('ingredients') != -1:
                    warning = 'Ingredientes repetidos'
                elif field.find('instructions') != -1:
                    warning = 'Instrução repetida'
                self.add_error(field, warning)
        return self.cleaned_data

    def save(self, **kwargs):
        post = self.instance
        post.title = self.cleaned_data['title']
        post.ingredients_set.all().delete()
        post.instructions_set.all().delete()
        super().save(**kwargs)
        for ingredient in self.cleaned_data['ingredients']:
            Ingredients.objects.create(
                post=post,
                ingredients=ingredient,
            )
        for instruction in self.cleaned_data['instructions']:
            Instructions.objects.create(
                post=post,
                instructions=instruction,
            )
        return self.instance

    def generateFields(self, ingredients, instructions):
        self.fields = {}
        self.fields['title']= forms.CharField(max_length=60, required=True)
        self.fields['description'] = forms.CharField(max_length=150)
        self.fields['picture'] = forms.ImageField(required=False, )
        # Gerar campos de ingredientes
        self.fields['ingredients0'] = forms.CharField(max_length=100, label='Ingredientes', required=True)
        i = 0
        for i in range(len(ingredients) + 1):
            if i == 0:
                label = 'Ingredientes'
                required = True
            else:
                label = ''
                required = False
            field_name = f'ingredients{i}'
            self.fields[field_name] = forms.CharField(max_length=100, required=required, label=label)
            try:
                if(type(ingredients)==list):
                    self.initial[field_name] = ingredients[i]
                else:
                    self.initial[field_name] = ingredients[i].ingredients
            except:
                self.initial[field_name] = ''
            # create an extra blank field

        # Gerar campos de instrucoes
        self.fields['instructions0'] = forms.CharField(max_length=100, label='Instruções', required=True)
        i = 0
        for i in range(len(instructions) + 1):
            if i == 0:
                label = 'Instruções'
                required = True
            else:
                label = ''
                required = False
            field_name = f'instructions{i}'
            self.fields[field_name] = forms.CharField(required=required, label=label)
            try:
                if (type(instructions) == list):
                    self.initial[field_name] = instructions[i]
                else:
                    self.initial[field_name] = instructions[i].instructions
            except:
                self.initial[field_name] = ''
            # create an extra blank field

class postUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Post
        fields = ['title']
