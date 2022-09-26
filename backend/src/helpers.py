import json
from flask import abort


def validate_create_drink_request(request):
    '''Validates the request body for a create drink request.

    Args:
        request (obj):  The request object
    Returns:
        bool: True if successfull.
    '''
    # checks that the request body has the expected shape
    expected_request_body = [
            'title',
            'recipe'
    ]
    for field in expected_request_body:
        if field not in json.loads(request.data).keys():
            abort(400)
        if field == 'title' and json.loads(request.data)['title'] == '':
            abort(400)
    # checks that the recipe list is not empty and that
    #  the ingredients in the list have the expected shape
    validate_recipe_body(request)
    return True


def validate_recipe_body(request):
    '''Checks the body of a recipe in a request is the correct format.

    Args:
        request (obj):  The request object
    Returns:
        bool: True if successfull.
    '''
    recipe = json.loads(request.data)['recipe']
    if not isinstance(recipe, list) or len(recipe) == 0:
        abort(400)
    validate_ingredient(recipe)
    return True


def validate_ingredient(recipe):
    '''Checks the body of each ingredient in a recipe is the correct format.

    Args:
        request (obj):  The recipe list
    Returns:
        bool: True if successfull.
    '''
    expected_ingredient_fields = [
            'name',
            'color',
            'parts'
        ]
    string_fields = [
        'name',
        'color'
    ]
    for ingredient in recipe:
        for field in expected_ingredient_fields:
            if field not in ingredient.keys():
                abort(400)
            if field in string_fields and isEmptyString(ingredient[field]):
                abort(400)
            if field == 'parts' and ingredient[field] <= 0:
                abort(400)
    return True


def isEmptyString(word):
    '''Checks whether a string is empty.

    Args:
        word (str):  The string.
    Returns:
        bool: True/False.
    '''
    if word == '':
        return True
    return False


def isValidTitle(request):
    '''Checks whether a title string in an edit drink request is empty.

    It aborts with a 400 error if the string is empty.

    Args:
        request (obj):  The request object.
    Returns:
        bool: True.
    '''
    if json.loads(request.data)['title'] == '':
        abort(400)
    return True