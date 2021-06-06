from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from .forms import ActionForm, InitialLiquidityForm, SimulationForm
from .models import Simulation, db

from ...mechanisms.amm.models import AMM
from ...mechanisms.amm.routes import apply_volume

from ...interpreters.plotter.plotter import Plotter

# Blueprint Configuration
simulator_bp = Blueprint(
    'simulator_bp', __name__,
    url_prefix='/simulator',
    template_folder='templates',
    static_folder='static'
)


"""Main Simulation Dashboard Page"""
@simulator_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    active_sim = current_user.active_sim()
    # Bypass if user is logged in
    if not active_sim:
        return redirect(url_for('simulator_bp.new'))
    return render_template(
        'mainsim.jinja2',
        title='Main Simulator',
        template='simulator-template',
        current_user=current_user,
        active_sim=active_sim,
        body=""
    )

"""Create New Simulation."""
@simulator_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = SimulationForm()
    if form.validate_on_submit():

        new_sim = Simulation(user_id=current_user.id,
                            sim_name=form.name.data,
                            days =form.days.data
                                )
        # Adjust active sim so that only one is active at a time.
        # New Sims become active by default.
        current_active_sims = Simulation.query.filter_by(active=True).all()
        for sim in current_active_sims:
            sim.active = False

        db.session.add(new_sim)
        db.session.commit()
        return redirect(url_for('simulator_bp.dashboard'))
    return render_template(
        'generalform.jinja2',
        title='New Simulation.',
        form=form,
        template='new-simulation-page',
        body="Sign up for a user account."
    )
#
"""Run Active Simulation.
Currently:
    * apply_volume
    * to do: add more stuffs
    """
@simulator_bp.route('/run/<int:y_volume>', methods=['GET'])
@login_required
def run(y_volume):
    active_sim = current_user.active_sim()
    i = 0
    while i < active_sim.days:
        apply_volume(0,y_volume,5000)
        i+=1
    db.session.commit()
    return redirect(url_for('simulator_bp.dashboard'))

"""Activates a target simulation
Deactivates previously active simulation"""
@simulator_bp.route('/activate/<int:id>', methods=['GET'])
@login_required
def activate(id):
    target_sim = Simulation.query.get(id)
    if target_sim:
        current_active_sims = Simulation.query.filter_by(active=True).all()
        for sim in current_active_sims:
            sim.active = False
        target_sim.active = True
        db.session.commit()
    return redirect(url_for('simulator_bp.dashboard'))

"""Delete Simulation Instance
    In order to deal with the large amount of links
    Each simulation contains all its own links
    To delete, must cascade through all child tables and delete first.
    """
@simulator_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    target_sim = Simulation.query.get(id)
    if target_sim:
        for amm in target_sim.amms:
            for record in amm.records:
                db.session.delete(record)

            db.session.delete(amm)

        db.session.delete(target_sim)
        db.session.commit()
    return redirect(url_for('simulator_bp.dashboard'))
#
