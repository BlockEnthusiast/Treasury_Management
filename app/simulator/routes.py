from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import pandas as pd

from .forms import ActionForm, InitialLiquidityForm, SimulationForm
from .models import Simulation, db
from ..amm.models import AMM
from ..amm.routes import apply_volume

from ..plotter.plotter import Plotter

# Blueprint Configuration
simulator_bp = Blueprint(
    'simulator_bp', __name__,
    url_prefix='/simulator',
    template_folder='templates',
    static_folder='static'
)

# user_bp.route('/', methods=['GET'])(index)
# user_bp.route('/', methods=['POST'])(store)
# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)


"""Logged-in page routes."""
@simulator_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    active_sim = current_user.active_sim()
    # action_form = SimulationForm()
    # ilf_form1 = InitialLiquidityForm()
    # ilf_form2 = InitialLiquidityForm()
    # if ilf_form1.validate_on_submit():
    #     current_user,
    print(active_sim.sim_name)
    return render_template(
        'mainsim.jinja2',
        title='Main Simulator',
        template='simulator-template',
        current_user=current_user,
        active_sim=active_sim,
        body=""
    )

"""Logged-in page routes."""
@simulator_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = SimulationForm()
    if form.validate_on_submit():
        new_sim = Simulation(user_id=current_user.id,
                            sim_name=form.name.data,
                            days =form.days.data
                                )
        current_active_sims = Simulation.query.filter_by(active=True).all()
        for sim in current_active_sims:
            sim.active = False
        db.session.add(new_sim)
        db.session.commit()
        print(new_sim)
        current_active_sims = Simulation.query.filter_by(active=True).all()
        print(current_active_sims)
        return redirect(url_for('simulator_bp.dashboard'))
    return render_template(
        'newsim.jinja2',
        title='New Simulation.',
        form=form,
        template='new-simulation-page',
        body="Sign up for a user account."
    )
#
"""Logged-in page routes."""
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

"""Logged-in page routes."""
@simulator_bp.route('/activate/<int:id>', methods=['GET'])
@login_required
def activate(id):
    target_sim = Simulation.query.get(id)
    if target_sim:
        active_sim = current_user.active_sim()
        active_sim.active = False
        target_sim.active = True
        db.session.commit()
    return redirect(url_for('simulator_bp.dashboard'))

"""Logged-in page routes."""
@simulator_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    target_sim = Simulation.query.get(id)
    if target_sim:
        for amm in target_sim.amms:
            for record in amm.records:
                db.session.delete(record)
            db.session.delete(amm)
        # target_sim = Simulation.query.filter_by(id=id).delete()
        db.session.delete(target_sim)
        db.session.commit()
    return redirect(url_for('simulator_bp.dashboard'))
#     balancer = AMM_Dynamic("Balancer")
#     balancer.seed(251,3450473)
#     balancer.set_weight_x(.20)
#
#     sushi = AMM_Classic("Sushi")
#     sushi.seed(483.9, 1658000)
#
#     pools = [balancer, sushi]
#     data
#
#     move_size = 100
#     d = 0
#     sets = []
#     while d < days:
#         d +=1
#         sets = [[]]
#         sets_map = {}
#         remainder = y_volume
#         while remainder > 0:
#             best_priced_pool = None
#             for pool in pool:
#                 if best_priced_pool == None:
#                     best_priced_pool = pool
#                 elif best_priced_pool.y_price() < pool.y_price():
#                     best_priced_pool = pool
#             if remainder > move_size:
#                 pool.apply_volume(move_size)
#                 remainder -= move_size
#             else:
#                 pool.apply_volume(remainder)
#                 remainder -= remainder
#
#
#
#                 }
    # p = balancer.plot_curve(p)
    # p = balancer.plot_current(p, True)
    # balancer.apply_volume(280000)
    # p.iterate_plot()
    # p = sushi.plot_curve(p)
    # p = sushi.plot_current(p, True)
    # return p.fig
