from django import forms
from .models import Post, Ingredients, Instructions


class postCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generateFields(Ingredients.objects.filter(post=self.instance), Instructions.objects.filter(post=self.instance))

    class Meta:
        model = Post
        fields = ['title']

    def clean(self):
        ingredients = set()
        i = 0
        field_name = f'ingredients{i}'
        duplicate = False
        duplicateFieldName = []
        while self.data.get(field_name):
            ingredient = self.data[field_name]
            if ingredient in ingredients:
                duplicate = True
            else:
                ingredients.add(ingredient)
            i += 1
            field_name = f'ingredients{i}'
        self.cleaned_data["ingredients"] = ingredients
        instructions = set()
        i = 0
        field_name = f'instructions{i}'
        while self.data.get(field_name):
            instruction = self.data[field_name]
            if instruction in instructions:
                duplicateFieldName.append(field_name)
                duplicate = True
            else:
                instructions.add(instruction)
            i += 1
            field_name = f'instructions{i}'
        self.cleaned_data["instructions"] = instructions
        if duplicate:
            print(self.cleaned_data["instructions"])
            print(self.cleaned_data["ingredients"])
            self.generateFields(self.cleaned_data["ingredients"], self.cleaned_data["instructions"])

            self.add_error('instructions0', 'Duplicado')

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
        self.fields['title']= forms.CharField(max_length=100, required=True)
        print(ingredients, instructions)
        # Gerar campos de ingredientes
        self.fields['ingredients0'] = forms.CharField(max_length=100, label='Ingredientes', required=True)
        # ingredients = Ingredients.objects.filter(post=self.instance)
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
        if not self.initial['ingredients0'] == '':
            field_name = f'ingredients{i + 1}'
            self.fields[field_name] = forms.CharField(required=False, label='')

        # Gerar campos de instrucoes
        self.fields['instructions0'] = forms.CharField(max_length=100, label='Instruções', required=True)
        # instructions = Instructions.objects.filter(post=self.instance)
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
        if not self.initial['instructions0'] == '':
            field_name = f'instructions{i + 1}'
            self.fields[field_name] = forms.CharField(required=False, label='')
        print(self.fields)

class postUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Post
        fields = ['title']
