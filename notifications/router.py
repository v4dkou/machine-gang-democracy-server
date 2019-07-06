from . import viewsets as v


def register(router):
    router.register('user-devices', v.UserDeviceViewSet, base_name='user-devices')
