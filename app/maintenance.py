from absl import logging
from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required

import grpc
from steward import registry_pb2_grpc
from steward import maintenance_pb2 as m

from app.forms import MaintenanceForm

bp = Blueprint("maintenance", __name__)

logging.set_verbosity(logging.INFO)

channel = grpc.insecure_channel('localhost:50051')
maintenances = registry_pb2_grpc.MaintenanceServiceStub(channel)

@bp.route('/maintenances')
@login_required
def list_maintenances():
    return render_template('maintenances.html', maintenances=maintenances.ListMaintenances(m.ListMaintenancesRequest()))

@bp.route('/maintenance/create', methods=['GET', 'POST'])
@login_required
def maintenance_create():
    form = MaintenanceForm()
    if form.validate_on_submit():
        maintenance = m.Maintenance()
        maintenance.name = form.name.data
        maintenance.description = form.description.data
        new_maintenance = maintenances.CreateMaintenance(maintenance)
        flash('Maintenace \'{}\' Created!'.format(form.name.data))
        return redirect('/maintenance/{}'.format(new_maintenance._id))
    return render_template('maintenance_edit.html', form=form, view="Create Maintenance")

@bp.route('/maintenance/<maintenance_id>')
@login_required
def maintenance(maintenance_id=None):
    return render_template('maintenance.html', maintenance=maintenances.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id)))

@bp.route('/maintenance/edit/<maintenance_id>', methods=['GET', 'POST'])
@login_required
def maintenance_edit(maintenance_id=None):
    form = MaintenanceForm()

    if form.validate_on_submit():
        logging.error('edit form checks out, pushing updates')
        maintenance = m.Maintenance()
        maintenance.name = form.name.data
        maintenance.description = form.description.data
        maintenance.enabled = form.enabled.data
        maintenance.asset.name = form.asset.data
        maintenance.schedule.description = form.schedule.data

        new_maintenance = maintenances.UpdateMaintenance(m.UpdateMaintenanceRequest(_id=maintenance_id, maintenance=maintenance))
        flash('Maintenace \'{}\' Updated!'.format(form.name.data))
        return redirect('/maintenance/{}'.format(new_maintenance._id))
    else:
        logging.info('loading current values because: {}'.format(form.errors))
        old_maintenance = maintenances.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id))
        form = MaintenanceForm(obj=old_maintenance)

    return render_template('maintenance_edit.html', form=form, view='Edit Maintenance')