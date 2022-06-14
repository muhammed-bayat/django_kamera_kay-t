
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as e:
        print('ERR====>', e)

    except classmodel.DoesNotExist:
        return None