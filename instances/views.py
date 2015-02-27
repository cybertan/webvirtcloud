from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from computes.models import Compute
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.connection import connection_manager
from libvirt import libvirtError


def index(request):
    """
    :param request:
    :return:
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('instances'))


def instances(request):
    """
    :param request:
    :return:
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    computes = Compute.objects.filter()
    all_host_vms = {}

    for compute in computes:
        if connection_manager.host_is_up(compute.type, compute.hostname):
            try:
                conn = wvmHostDetails(compute, compute.login, compute.password, compute.type)
                all_host_vms[compute.id, compute.name] = conn.get_host_instances()
                conn.close()
            except libvirtError:
                pass

    return render(request, 'instances.html', locals())


def instance(request, comptes_id, vname):
    """
    :param request:
    :return:
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'instances.html', locals())